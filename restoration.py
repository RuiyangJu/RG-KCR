import os
import cv2
import argparse
import numpy as np
from tqdm import tqdm

parser = argparse.ArgumentParser(description="Remove red seals from document images using color thresholding and inpainting")
parser.add_argument("--input_dir", type=str, default="./yolo_dataset/images/test", help="Input image directory")
parser.add_argument("--output_dir", type=str, default=None, help="Output image directory (if not set, auto-generated from parameters)")
parser.add_argument("--r_min", type=int, default=90, help="Minimum R channel threshold (e.g., 80, 90)")
parser.add_argument("--rg_ratio", type=float, default=1.3, help="R/G ratio threshold (e.g., 1.2, 1.3, 1.4, 1.5)")
parser.add_argument("--rb_ratio", type=float, default=1.3, help="R/B ratio threshold (e.g., 1.2, 1.3, 1.4, 1.5)")
parser.add_argument("--inpaint_radius", type=int, default=3, help="Inpainting radius")
parser.add_argument("--inpaint_method", type=str, default="telea", choices=["telea", "ns"], help="Inpainting method: telea or ns")
parser.add_argument("--dilate_kernel", type=int, default=3, help="Dilate kernel size (0 to disable)")
parser.add_argument("--dilate_iter", type=int, default=1, help="Dilate iterations")
args = parser.parse_args()
input_dir = args.input_dir

if args.output_dir is None:
    base_dir = os.path.dirname(input_dir.rstrip("/"))
    output_dir = os.path.join(
        base_dir,
        f"test_r{args.r_min}_rg{args.rg_ratio}_rb{args.rb_ratio}"
    )
else:
    output_dir = args.output_dir

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

    out_bgr = cv2.inpaint(bgr, seal_mask, inpaint_radius, inpaint_method)
    return out_bgr

def is_image_file(fn: str) -> bool:
    return os.path.splitext(fn.lower())[1] in exts

def main():
    os.makedirs(output_dir, exist_ok=True)

    files = [f for f in os.listdir(input_dir) if is_image_file(f)]
    files.sort()

    if len(files) == 0:
        raise RuntimeError(f"No images found in: {input_dir}")

    print("======================================")
    print(" Red Seal Removal Preprocessing")
    print("======================================")
    print(f"Input Dir   : {input_dir}")
    print(f"Output Dir  : {output_dir}")
    print(f"r_min       : {r_min}")
    print(f"rg_ratio    : {rg_ratio}")
    print(f"rb_ratio    : {rb_ratio}")
    print(f"inpaint     : {args.inpaint_method} (radius={inpaint_radius})")
    print(f"dilate      : kernel={dilate_kernel}, iter={dilate_iter}")
    print("======================================")

    for fn in tqdm(files, desc="Processing"):
        in_path = os.path.join(input_dir, fn)
        out_path = os.path.join(output_dir, fn)

        bgr = cv2.imread(in_path, cv2.IMREAD_COLOR)
        if bgr is None:
            print(f"[WARN] Skip unreadable: {in_path}")
            continue

        out_bgr = remove_red_seal(bgr)

        ok = cv2.imwrite(out_path, out_bgr)
        if not ok:
            print(f"[WARN] Failed to write: {out_path}")

    print(f"\nDone! Saved to: {output_dir}")

if __name__ == "__main__":
    main()
