import re
import json
import time
import argparse
from pathlib import Path

import torch
from PIL import Image
from tqdm import tqdm
from transformers import AutoModel, AutoImageProcessor
from huggingface_hub import snapshot_download


repo_name = "SakanaAI/Metom"
local_model_dir = Path("./classification/models/Metom")

device = "cuda" if torch.cuda.is_available() else "cpu"
torch_dtype = torch.float32

IMG_EXTS = {".jpg", ".jpeg", ".png", ".bmp", ".tif", ".tiff", ".webp"}
BBOX_RE = re.compile(r"_X(\d+)_Y(\d+)_W(\d+)_H(\d+)", re.IGNORECASE)


def prepare_model_path():
    if local_model_dir.exists() and any(local_model_dir.iterdir()):
        print(f"Using local model: {local_model_dir}")
        return str(local_model_dir)

    print(f"Local model not found. Downloading {repo_name} to {local_model_dir} ...")

    snapshot_download(
        repo_id=repo_name,
        local_dir=str(local_model_dir),
        local_dir_use_symlinks=False,
    )

    print(f"Model downloaded to: {local_model_dir}")
    return str(local_model_dir)


def get_image(image_path: Path) -> Image.Image:
    with Image.open(image_path) as im:
        return im.convert("RGB")


def parse_bbox_from_name(name: str):
    m = BBOX_RE.search(name)
    if not m:
        return None

    x, y, w, h = map(int, m.groups())
    return [x, y, w, h]


def extract_topk_labels_only(out):
    labels = None

    if isinstance(out, dict):
        labels = out.get("labels", None)
        if labels is None:
            raise ValueError(f"Unexpected dict output keys: {list(out.keys())}")

    elif isinstance(out, (tuple, list)):
        if len(out) == 2 and isinstance(out[0], (list, tuple)):
            labels = out[0]
        else:
            labels = out

    else:
        labels = out

    if isinstance(labels, (list, tuple)) and len(labels) > 0 and isinstance(labels[0], (list, tuple)):
        if len(labels) == 1:
            labels = labels[0]

    if isinstance(labels, (list, tuple)) and len(labels) > 0:
        first = labels[0]
        if isinstance(first, (list, tuple)) and len(first) == 2:
            labels = [x[0] for x in labels]

    if not isinstance(labels, (list, tuple)):
        labels = [labels]

    return [str(x) for x in labels]


def split_batch_output(out, batch_size):
    if isinstance(out, dict):
        labels = out.get("labels", None)
        if labels is None:
            raise ValueError(f"Unexpected dict output keys: {list(out.keys())}")

        if isinstance(labels, (list, tuple)) and len(labels) == batch_size:
            return labels

        if batch_size == 1:
            return [labels]

        raise ValueError(
            f"Cannot split dict output. batch_size={batch_size}, labels_len={len(labels)}"
        )

    if isinstance(out, (tuple, list)) and len(out) == 2:
        labels = out[0]

        if isinstance(labels, (list, tuple)) and len(labels) == batch_size:
            return labels

        if batch_size == 1:
            return [labels]

    if isinstance(out, (list, tuple)) and len(out) == batch_size:
        return out

    if batch_size == 1:
        return [out]

    raise ValueError(f"Cannot split batch output. type={type(out)}, batch_size={batch_size}")


def dump_json_one_item_per_line(path: Path, items: list):
    with open(path, "w", encoding="utf-8") as f:
        f.write("[\n")
        for i, item in enumerate(items):
            line = json.dumps(item, ensure_ascii=False, separators=(",", ":"))
            f.write(line)
            f.write(",\n" if i < len(items) - 1 else "\n")
        f.write("]\n")


def load_model():
    model_path = prepare_model_path()

    processor = AutoImageProcessor.from_pretrained(
        model_path,
        use_fast=False,
    )

    model = AutoModel.from_pretrained(
        model_path,
        dtype=torch_dtype,
        attn_implementation="sdpa",
        trust_remote_code=True,
    ).to(device=device)

    model.eval()

    if device == "cuda":
        torch.backends.cuda.matmul.allow_tf32 = True
        torch.backends.cudnn.allow_tf32 = True

    return processor, model


def process_batch(batch_items, processor, model, results, failed):
    if len(batch_items) == 0:
        return 0, 0

    images = []
    valid_items = []

    for item in batch_items:
        try:
            image = get_image(item["path"])
            images.append(image)
            valid_items.append(item)
        except Exception as e:
            failed.append({
                "file": item["path"].name,
                "err": f"Image loading failed: {str(e)}",
            })

    if len(images) == 0:
        return 0, len(batch_items)

    try:
        pixel_values = processor(
            images=images,
            return_tensors="pt",
        )["pixel_values"].to(
            device=device,
            dtype=torch_dtype,
        )

        with torch.inference_mode():
            out = model.get_topk_labels(
                pixel_values,
                k=5,
                return_probs=True,
            )

        batch_outputs = split_batch_output(out, batch_size=len(images))

        processed = 0
        local_failed = 0

        for item, one_out in zip(valid_items, batch_outputs):
            try:
                char_top5 = extract_topk_labels_only(one_out)

                if len(char_top5) != 5:
                    char_top5 = (char_top5 + [""] * 5)[:5]
                    failed.append({
                        "file": item["path"].name,
                        "err": f"Returned labels != 5 (padded). raw={one_out}",
                    })
                    local_failed += 1

                results.append({
                    "char": char_top5,
                    "bbox": item["bbox"],
                })

                processed += 1

            except Exception as e:
                failed.append({
                    "file": item["path"].name,
                    "err": f"Output parsing failed: {str(e)}",
                })
                local_failed += 1

        return processed, local_failed

    except Exception as e:
        for item in valid_items:
            failed.append({
                "file": item["path"].name,
                "err": f"Batch inference failed: {str(e)}",
            })

        return 0, len(valid_items)


def main(args):
    root_dir = Path(args.root_dir)
    out_dir = Path(args.out_dir)
    batch_size = args.batch_size

    out_dir.mkdir(parents=True, exist_ok=True)

    processor, model = load_model()

    subdirs = sorted([p for p in root_dir.iterdir() if p.is_dir()])
    if not subdirs:
        raise RuntimeError(f"No subfolders found under: {root_dir}")

    total_processed = 0
    total_skipped = 0
    total_failed = 0

    page_latency_list = []
    page_fps_list = []
    page_patch_count_list = []

    if device == "cuda":
        torch.cuda.synchronize()

    t0_all = time.perf_counter()

    for folder in tqdm(subdirs, desc="Folders", unit="folder"):
        t0_folder = time.perf_counter()

        img_paths = sorted([
            p for p in folder.iterdir()
            if p.suffix.lower() in IMG_EXTS
        ])

        results = []
        skipped = []
        failed = []
        batch_items = []

        for img_path in tqdm(
            img_paths,
            desc=f"Images in {folder.name}",
            unit="img",
            leave=False
        ):
            bbox = parse_bbox_from_name(img_path.name)

            if bbox is None:
                skipped.append(img_path.name)
                total_skipped += 1
                continue

            batch_items.append({
                "path": img_path,
                "bbox": bbox,
            })

            if len(batch_items) >= batch_size:
                processed, failed_count = process_batch(
                    batch_items,
                    processor,
                    model,
                    results,
                    failed,
                )
                total_processed += processed
                total_failed += failed_count
                batch_items = []

        if len(batch_items) > 0:
            processed, failed_count = process_batch(
                batch_items,
                processor,
                model,
                results,
                failed,
            )
            total_processed += processed
            total_failed += failed_count

        out_path = out_dir / f"{folder.name}.json"
        dump_json_one_item_per_line(out_path, results)

        if skipped:
            skipped_path = out_dir / f"{folder.name}_skipped.txt"
            with open(skipped_path, "w", encoding="utf-8") as f:
                for name in skipped:
                    f.write(name + "\n")

        if failed:
            failed_path = out_dir / f"{folder.name}_failed.json"
            with open(failed_path, "w", encoding="utf-8") as f:
                json.dump(failed, f, ensure_ascii=False, indent=2)

        if device == "cuda":
            torch.cuda.synchronize()

        folder_time = time.perf_counter() - t0_folder

        page_latency_list.append(folder_time)
        page_fps_list.append(1.0 / folder_time if folder_time > 0 else 0.0)
        page_patch_count_list.append(len(results))

    if device == "cuda":
        torch.cuda.synchronize()

    total_time = time.perf_counter() - t0_all

    if page_latency_list:
        avg_page_latency = sum(page_latency_list) / len(page_latency_list)
        avg_page_fps = sum(page_fps_list) / len(page_fps_list)
    else:
        avg_page_latency = 0.0
        avg_page_fps = 0.0

    print(f"Device: {device}")
    print(f"Model dir: {local_model_dir}")
    print(f"Root dir: {root_dir}")
    print(f"Output dir: {out_dir}")
    print(f"Batch size: {batch_size}")
    print(f"Processed folders/pages: {len(subdirs)}")
    print(f"Processed patches/images: {total_processed}")
    print(f"Skipped patches/images: {total_skipped}")
    print(f"Failed patches/images: {total_failed}")
    print(f"Total Inference Time: {total_time:.2f}s")
    print(f"Average Inference Time: {avg_page_latency:.2f} sec")
    print(f"Average Inference Speed: {avg_page_fps:.2f} fps")
    print(f"JSON saved to: {out_dir}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--root_dir", type=str, required=True, help="Root directory containing cropped image subfolders")
    parser.add_argument("--out_dir", type=str, required=True, help="Directory to save classification JSON results")
    parser.add_argument("--batch_size", type=int, default=1280, help="Batch size for classification inference")
    args = parser.parse_args()
    main(args)
