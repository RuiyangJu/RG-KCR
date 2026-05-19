import re
import csv
import time
import statistics
from pathlib import Path

import torch
from PIL import Image
from transformers import AutoModel, AutoImageProcessor


repo_name = "SakanaAI/Metom"
device = "cuda" if torch.cuda.is_available() else "cpu"
torch_dtype = torch.float32

ROOT_DIR = Path("../visual_crop/crops")
OUT_CSV = Path("./classification_fps_runs.csv")

REPEAT = 30
WARMUP_RUNS = 3

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


def collect_pages():
    subdirs = sorted([p for p in ROOT_DIR.iterdir() if p.is_dir()])
    if not subdirs:
        raise RuntimeError(f"No subfolders found under: {ROOT_DIR}")

    pages = []

    for folder in subdirs:
        img_paths = sorted([
            p for p in folder.iterdir()
            if p.suffix.lower() in IMG_EXTS and parse_bbox_from_name(p.name) is not None
        ])

        pages.append({
            "folder": folder.name,
            "img_paths": img_paths,
        })

    return pages


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


def run_once(pages):
    total_patches = 0
    total_pages = len(pages)
    failed = 0

    if device == "cuda":
        torch.cuda.synchronize()

    t0 = time.perf_counter()

    for page in pages:
        for img_path in page["img_paths"]:
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
                    _ = model.get_topk_labels(
                        pixel_values,
                        k=5,
                        return_probs=True,
                    )

                total_patches += 1

            except Exception:
                failed += 1

    if device == "cuda":
        torch.cuda.synchronize()

    total_time = time.perf_counter() - t0

    patch_fps = total_patches / total_time if total_time > 0 else 0.0
    page_fps = total_pages / total_time if total_time > 0 else 0.0
    patch_latency_ms = total_time / total_patches * 1000 if total_patches > 0 else 0.0
    page_latency_s = total_time / total_pages if total_pages > 0 else 0.0

    return {
        "total_time_s": total_time,
        "pages": total_pages,
        "patches": total_patches,
        "failed": failed,
        "patch_fps": patch_fps,
        "page_fps": page_fps,
        "patch_latency_ms": patch_latency_ms,
        "page_latency_s": page_latency_s,
    }


def main():
    pages = collect_pages()

    print(f"Collected pages: {len(pages)}")
    print(f"Collected patches: {sum(len(p['img_paths']) for p in pages)}")

    print("Warmup...")
    for _ in range(WARMUP_RUNS):
        run_once(pages)

    records = []

    print("Benchmarking...")
    for run_idx in range(1, REPEAT + 1):
        result = run_once(pages)
        result["run"] = run_idx
        records.append(result)

        print(
            f"Run {run_idx:03d}: "
            f"time={result['total_time_s']:.2f}s, "
            f"patch_fps={result['patch_fps']:.2f}, "
            f"page_fps={result['page_fps']:.2f}"
        )

    with open(OUT_CSV, "w", newline="", encoding="utf-8") as f:
        fieldnames = [
            "run",
            "total_time_s",
            "pages",
            "patches",
            "failed",
            "patch_fps",
            "page_fps",
            "patch_latency_ms",
            "page_latency_s",
        ]

        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(records)

    patch_fps_list = [r["patch_fps"] for r in records]
    page_fps_list = [r["page_fps"] for r in records]
    time_list = [r["total_time_s"] for r in records]

    print("=" * 60)
    print("Benchmark summary")
    print(f"Runs: {REPEAT}")
    print(f"Pages per run: {records[0]['pages']}")
    print(f"Patches per run: {records[0]['patches']}")
    print(f"Failed per run: {records[0]['failed']}")

    print()
    print(f"Total time: {statistics.mean(time_list):.2f} ± {statistics.stdev(time_list):.2f} s")
    print(f"Patch FPS: {statistics.mean(patch_fps_list):.2f} ± {statistics.stdev(patch_fps_list):.2f} patches/s")
    print(f"Page FPS: {statistics.mean(page_fps_list):.2f} ± {statistics.stdev(page_fps_list):.2f} pages/s")

    print()
    print(f"CSV saved to: {OUT_CSV}")
    print("=" * 60)


if __name__ == "__main__":
    main()