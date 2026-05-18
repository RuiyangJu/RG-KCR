import re
import json
import time
from pathlib import Path

import torch
from PIL import Image
from tqdm import tqdm
from transformers import AutoModel, AutoImageProcessor


repo_name = "SakanaAI/Metom"
device = "cuda" if torch.cuda.is_available() else "cpu"
torch_dtype = torch.float32

ROOT_DIR = Path("./visual_crop/crops")
OUT_DIR = Path("./classification_results")

IMG_EXTS = {".jpg", ".jpeg", ".png", ".bmp", ".tif", ".tiff", ".webp"}
BBOX_RE = re.compile(r"_X(\d+)_Y(\d+)_W(\d+)_H(\d+)", re.IGNORECASE)


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


def dump_json_one_item_per_line(path: Path, items: list):
    with open(path, "w", encoding="utf-8") as f:
        f.write("[\n")
        for i, item in enumerate(items):
            line = json.dumps(item, ensure_ascii=False, separators=(",", ":"))
            f.write(line)
            f.write(",\n" if i < len(items) - 1 else "\n")
        f.write("]\n")


processor = AutoImageProcessor.from_pretrained(
    repo_name,
    use_fast=False,
)

model = AutoModel.from_pretrained(
    repo_name,
    dtype=torch_dtype,
    attn_implementation="sdpa",
    trust_remote_code=True,
).to(device=device)

model.eval()

if device == "cuda":
    torch.backends.cuda.matmul.allow_tf32 = True
    torch.backends.cudnn.allow_tf32 = True


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    subdirs = sorted([p for p in ROOT_DIR.iterdir() if p.is_dir()])
    if not subdirs:
        raise RuntimeError(f"No subfolders found under: {ROOT_DIR}")

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

        img_paths = sorted([p for p in folder.iterdir() if p.suffix.lower() in IMG_EXTS])

        results = []
        skipped = []
        failed = []

        for img_path in tqdm(img_paths, desc=f"Images in {folder.name}", unit="img", leave=False):
            bbox = parse_bbox_from_name(img_path.name)

            if bbox is None:
                skipped.append(img_path.name)
                total_skipped += 1
                continue

            try:
                image = get_image(img_path)

                pixel_values = processor(
                    images=image,
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

                char_top5 = extract_topk_labels_only(out)

                if len(char_top5) != 5:
                    char_top5 = (char_top5 + [""] * 5)[:5]
                    failed.append({
                        "file": img_path.name,
                        "err": f"Returned labels != 5 (padded). raw={out}",
                    })
                    total_failed += 1

                results.append({
                    "char": char_top5,
                    "bbox": bbox,
                })

                total_processed += 1

            except Exception as e:
                failed.append({
                    "file": img_path.name,
                    "err": str(e),
                })
                total_failed += 1
                continue

        out_path = OUT_DIR / f"{folder.name}.json"
        dump_json_one_item_per_line(out_path, results)

        if skipped:
            skipped_path = OUT_DIR / f"{folder.name}_skipped.txt"
            with open(skipped_path, "w", encoding="utf-8") as f:
                for name in skipped:
                    f.write(name + "\n")

        if failed:
            failed_path = OUT_DIR / f"{folder.name}_failed.json"
            with open(failed_path, "w", encoding="utf-8") as f:
                json.dump(failed, f, ensure_ascii=False, indent=2)

        if device == "cuda":
            torch.cuda.synchronize()

        folder_time = time.perf_counter() - t0_folder

        page_latency_list.append(folder_time)
        page_fps_list.append(1.0 / folder_time)
        page_patch_count_list.append(len(results))

    if device == "cuda":
        torch.cuda.synchronize()

    total_time = time.perf_counter() - t0_all

    if total_processed > 0:
        avg_time_per_patch = total_time / total_processed
        patch_fps = total_processed / total_time
    else:
        avg_time_per_patch = 0.0
        patch_fps = 0.0

    if page_latency_list:
        avg_page_latency = sum(page_latency_list) / len(page_latency_list)
        avg_page_fps = sum(page_fps_list) / len(page_fps_list)
        total_page_fps = len(page_latency_list) / total_time
        avg_patches_per_page = sum(page_patch_count_list) / len(page_patch_count_list)
    else:
        avg_page_latency = 0.0
        avg_page_fps = 0.0
        total_page_fps = 0.0
        avg_patches_per_page = 0.0

    print("=" * 60)
    print("Done.")
    print(f"Processed folders/pages: {len(subdirs)}")
    print(f"Processed patches/images: {total_processed}")
    print(f"Skipped patches/images: {total_skipped}")
    print(f"Failed patches/images: {total_failed}")
    print(f"Total time: {total_time:.2f}s")

    print()
    print("Patch-level speed:")
    print(f"Average latency: {avg_time_per_patch * 1000:.2f} ms/patch")
    print(f"Average FPS: {patch_fps:.2f} patches/s")

    print()
    print("Page-level speed:")
    print(f"Average latency: {avg_page_latency:.2f} s/page")
    print(f"Average FPS: {avg_page_fps:.2f} pages/s")
    print(f"Overall FPS: {total_page_fps:.2f} pages/s")
    print(f"Average patches per page: {avg_patches_per_page:.2f}")

    print()
    print(f"JSON saved to: {OUT_DIR}")
    print("=" * 60)


if __name__ == "__main__":
    main()
