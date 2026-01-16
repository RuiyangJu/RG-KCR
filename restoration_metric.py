import os
import csv
from pathlib import Path
import cv2
import numpy as np
from tqdm import tqdm
import metrics 

IMG_EXTS = {".jpg", ".jpeg", ".png", ".bmp", ".tif", ".tiff", ".webp"}

def is_image_file(p: Path) -> bool:
    return p.is_file() and p.suffix.lower() in IMG_EXTS

def collect_images(root: str):
    root = Path(root)
    files = [p for p in root.rglob("*") if is_image_file(p)]
    return {str(p.relative_to(root)).replace("\\", "/"): p for p in files}

def mean_ignore_nan(values):
    vals = [v for v in values if v is not None and not (isinstance(v, float) and np.isnan(v))]
    return float(np.mean(vals)) if len(vals) > 0 else float("nan")

def eval_folders(
    gt_dir: str,
    pred_dir: str,
    out_csv: str = "metrics.csv",
    crop_border: int = 0,
    input_order: str = "HWC",
    test_y_channel: bool = False,
    compute_psnrb: bool = False,
    strict_shape: bool = True,  
):
    gt_map = collect_images(gt_dir)
    pred_map = collect_images(pred_dir)

    common = sorted(set(gt_map.keys()) & set(pred_map.keys()))
    missing_in_pred = sorted(set(gt_map.keys()) - set(pred_map.keys()))
    extra_in_pred = sorted(set(pred_map.keys()) - set(gt_map.keys()))

    if len(common) == 0:
        raise RuntimeError("No matched pairs found. Check folder structure / filenames.")

    rows = []
    psnr_list, ssim_list, psnrb_list = [], [], []

    for key in tqdm(common, desc="Evaluating"):
        gt_path = str(gt_map[key])
        pred_path = str(pred_map[key])

        gt = cv2.imread(gt_path, cv2.IMREAD_COLOR)
        pred = cv2.imread(pred_path, cv2.IMREAD_COLOR)

        if gt is None or pred is None:
            continue

        if gt.shape != pred.shape:
            if strict_shape:
                continue
            pred = cv2.resize(pred, (gt.shape[1], gt.shape[0]), interpolation=cv2.INTER_LINEAR)

        psnr = metrics.calculate_psnr(gt, pred, crop_border=crop_border, input_order=input_order, test_y_channel=test_y_channel)
        ssim = metrics.calculate_ssim(gt, pred, crop_border=crop_border, input_order=input_order, test_y_channel=test_y_channel)

        row = {
            "rel_path": key,
            "gt_path": gt_path,
            "pred_path": pred_path,
            "PSNR": psnr,
            "SSIM": ssim,
        }

        psnr_list.append(psnr)
        ssim_list.append(ssim)

        if compute_psnrb:
            try:
                psnrb = metrics.calculate_psnrb(gt, pred, crop_border=crop_border, input_order=input_order, test_y_channel=test_y_channel)
            except Exception:
                psnrb = float("nan")
            row["PSNRB"] = psnrb
            psnrb_list.append(psnrb)

        rows.append(row)

    avg_psnr = mean_ignore_nan(psnr_list)
    avg_ssim = mean_ignore_nan(ssim_list)
    avg_psnrb = mean_ignore_nan(psnrb_list) if compute_psnrb else None

    os.makedirs(os.path.dirname(out_csv) or ".", exist_ok=True)

    fieldnames = ["rel_path", "gt_path", "pred_path", "PSNR", "SSIM"]
    if compute_psnrb:
        fieldnames.append("PSNRB")

    with open(out_csv, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        for r in rows:
            w.writerow(r)

        avg_row = {
            "rel_path": "__AVERAGE__",
            "gt_path": "",
            "pred_path": "",
            "PSNR": avg_psnr,
            "SSIM": avg_ssim,
        }
        if compute_psnrb:
            avg_row["PSNRB"] = avg_psnrb
        w.writerow(avg_row)

    print(f"[Saved] {out_csv}")
    print(f"[Pairs] matched={len(common)}  evaluated={len(rows)}  missing_in_pred={len(missing_in_pred)}  extra_in_pred={len(extra_in_pred)}")
    print(f"[Average] PSNR={avg_psnr:.6f}, SSIM={avg_ssim:.6f}" + (f", PSNRB={avg_psnrb:.6f}" if compute_psnrb else ""))

    if missing_in_pred:
        print(f"[Warning] Missing in pred (show up to 10): {missing_in_pred[:10]}")
    if extra_in_pred:
        print(f"[Info] Extra in pred (show up to 10): {extra_in_pred[:10]}")


if __name__ == "__main__":
    gt_dir = "./Kuzushiji_Character_Detection_Dataset/images/test_raw"
    pred_dir = "./Kuzushiji_Character_Detection_Dataset/images/test_r90_rg1.3_rb1.3"
    out_csv = "./restoration_results/test/r90_rg1.3_rb1.3.csv"

    eval_folders(
        gt_dir=gt_dir,
        pred_dir=pred_dir,
        out_csv=out_csv,
        crop_border=0,
        input_order="HWC",
        test_y_channel=False, 
        compute_psnrb=False, 
        strict_shape=True
    )
