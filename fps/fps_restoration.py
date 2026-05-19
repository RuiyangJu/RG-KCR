import os
import cv2
import csv
import time
import argparse
import statistics
import numpy as np


parser = argparse.ArgumentParser(description="Benchmark pure red seal removal processing FPS")
parser.add_argument("--input_dir", type=str, default="../yolov12/dataset/images/test_aug",help="Input image directory")
parser.add_argument("--r_min", type=int, default=90)
parser.add_argument("--rg_ratio", type=float, default=1.3)
parser.add_argument("--rb_ratio", type=float, default=1.3)
parser.add_argument("--inpaint_radius", type=int, default=3)
parser.add_argument("--inpaint_method", type=str, default="telea")
parser.add_argument("--dilate_kernel", type=int, default=3)
parser.add_argument("--dilate_iter", type=int, default=1)
parser.add_argument("--repeat", type=int, default=30)
parser.add_argument("--warmup", type=int, default=3)
parser.add_argument("--out_csv", type=str, default="./restoration_run_fps.csv")

args = parser.parse_args()


input_dir = args.input_dir
r_min = args.r_min
rg_ratio = args.rg_ratio
rb_ratio = args.rb_ratio
inpaint_radius = args.inpaint_radius
dilate_kernel = args.dilate_kernel
dilate_iter = args.dilate_iter

if args.inpaint_method.lower() == "telea":
    inpaint_method = cv2.INPAINT_TELEA
else:
    inpaint_method = cv2.INPAINT_NS

exts = {".jpg", ".jpeg", ".png", ".bmp", ".tif", ".tiff"}


def is_image_file(fn: str) -> bool:
    return os.path.splitext(fn.lower())[1] in exts


def remove_red_seal(bgr: np.ndarray) -> np.ndarray:
    rgb = cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB)

    R = rgb[:, :, 0].astype(np.float32)
    G = rgb[:, :, 1].astype(np.float32)
    B = rgb[:, :, 2].astype(np.float32)

    red_candidates = (R >= r_min) & (R >= rg_ratio * G) & (R >= rb_ratio * B)
    seal_mask = red_candidates.astype(np.uint8) * 255

    if dilate_kernel and dilate_kernel > 0:
        kernel = np.ones((dilate_kernel, dilate_kernel), np.uint8)
        seal_mask = cv2.dilate(seal_mask, kernel, iterations=dilate_iter)

    out_bgr = cv2.inpaint(
        bgr,
        seal_mask,
        inpaint_radius,
        inpaint_method,
    )

    return out_bgr


def load_images():
    files = sorted([f for f in os.listdir(input_dir) if is_image_file(f)])

    if len(files) == 0:
        raise RuntimeError(f"No images found in: {input_dir}")

    images = []
    failed = 0

    for fn in files:
        path = os.path.join(input_dir, fn)
        bgr = cv2.imread(path, cv2.IMREAD_COLOR)

        if bgr is None:
            failed += 1
            continue

        images.append(bgr)

    if len(images) == 0:
        raise RuntimeError("No readable images found.")

    return images, failed


def run_once(images):
    num_images = len(images)

    t0 = time.perf_counter()

    for bgr in images:
        _ = remove_red_seal(bgr)

    total_time = time.perf_counter() - t0

    fps = num_images / total_time if total_time > 0 else 0.0
    latency_ms = total_time / num_images * 1000 if num_images > 0 else 0.0

    return {
        "total_time_s": total_time,
        "images": num_images,
        "fps": fps,
        "latency_ms": latency_ms,
    }


def main():
    images, load_failed = load_images()

    print("=" * 60)
    print(f"Input dir: {input_dir}")
    print(f"Loaded images: {len(images)}")
    print(f"Load failed: {load_failed}")
    print(f"Repeat: {args.repeat}")
    print(f"Warmup: {args.warmup}")
    print("=" * 60)

    for _ in range(args.warmup):
        run_once(images)

    records = []

    for run_idx in range(1, args.repeat + 1):
        result = run_once(images)
        result["run"] = run_idx
        records.append(result)

        print(
            f"Run {run_idx:03d}: "
            f"time={result['total_time_s']:.4f}s, "
            f"fps={result['fps']:.2f}, "
            f"latency={result['latency_ms']:.2f} ms/image"
        )

    with open(args.out_csv, "w", newline="", encoding="utf-8") as f:
        fieldnames = [
            "run",
            "total_time_s",
            "images",
            "fps",
            "latency_ms",
        ]

        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(records)

    fps_list = [r["fps"] for r in records]
    latency_list = [r["latency_ms"] for r in records]
    time_list = [r["total_time_s"] for r in records]

    print("=" * 60)
    print("Benchmark summary")
    print(f"Pages per run: {len(images)}")
    print(f"Total time: {statistics.mean(time_list):.4f} ± {statistics.stdev(time_list):.4f} s")
    print(f"FPS: {statistics.mean(fps_list):.2f} ± {statistics.stdev(fps_list):.2f} pages/s")
    print(f"Latency: {statistics.mean(latency_list):.2f} ± {statistics.stdev(latency_list):.2f} ms")
    print(f"CSV saved to: {args.out_csv}")
    print("=" * 60)


if __name__ == "__main__":
    main()
