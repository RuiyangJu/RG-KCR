import os
import glob
import cv2

image_dir = "./Kuzushiji_Character_Detection_Dataset/images/test_r90_rg1.3_rb1.3"
label_dir = "./runs/detect/test_yolo12m/labels"
save_root = "./visual_crop"
vis_dir   = os.path.join(save_root, "vis_with_label")
crop_dir  = os.path.join(save_root, "crops")

os.makedirs(vis_dir, exist_ok=True)
os.makedirs(crop_dir, exist_ok=True)

default_color = (0, 255, 0)
thickness = 4
font = cv2.FONT_HERSHEY_SIMPLEX
font_scale = 0.6
font_thickness = 2

CONF_THRES = None

TOPK = None

IMG_EXTS = [".jpg", ".jpeg", ".png", ".tif", ".tiff", ".bmp", ".webp"]

def find_image_by_stem(image_folder: str, stem: str):
    for ext in IMG_EXTS:
        p = os.path.join(image_folder, stem + ext)
        if os.path.isfile(p):
            return p
    return None

def yolo_xywh_to_xyxy(xc, yc, w, h, W, H):
    x1 = (xc - w / 2.0) * W
    y1 = (yc - h / 2.0) * H
    x2 = (xc + w / 2.0) * W
    y2 = (yc + h / 2.0) * H

    x1 = int(max(0, min(W - 1, round(x1))))
    y1 = int(max(0, min(H - 1, round(y1))))
    x2 = int(max(0, min(W - 1, round(x2))))
    y2 = int(max(0, min(H - 1, round(y2))))

    if x2 < x1:
        x1, x2 = x2, x1
    if y2 < y1:
        y1, y2 = y2, y1

    return x1, y1, x2, y2

def parse_yolo_line(line: str):
    parts = line.strip().split()
    if len(parts) < 5:
        return None

    try:
        cls_id = int(float(parts[0]))
        xc = float(parts[1])
        yc = float(parts[2])
        bw = float(parts[3])
        bh = float(parts[4])
        conf = float(parts[5]) if len(parts) >= 6 else None
        return cls_id, xc, yc, bw, bh, conf
    except ValueError:
        return None

def safe_crop(img, x1, y1, x2, y2):
    H, W = img.shape[:2]
    x1 = max(0, min(W - 1, x1))
    x2 = max(0, min(W - 1, x2))
    y1 = max(0, min(H - 1, y1))
    y2 = max(0, min(H - 1, y2))
    if x2 <= x1 or y2 <= y1:
        return None
    return img[y1:y2, x1:x2].copy()

txt_files = sorted(glob.glob(os.path.join(label_dir, "*.txt")))
if not txt_files:
    raise RuntimeError(f"No .txt files found in: {label_dir}")

missing_images = 0
processed = 0
total_crops = 0

for txt_path in txt_files:
    stem = os.path.splitext(os.path.basename(txt_path))[0]
    img_path = find_image_by_stem(image_dir, stem)

    if img_path is None:
        print(f"[WARN] Image not found for label: {stem}  (searched in {image_dir})")
        missing_images += 1
        continue

    img = cv2.imread(img_path)
    if img is None:
        print(f"[WARN] Failed to read image: {img_path}")
        continue

    H, W = img.shape[:2]
    img_vis = img.copy()

    dets = []
    with open(txt_path, "r", encoding="utf-8") as f:
        for ln in f:
            ln = ln.strip()
            if not ln:
                continue
            parsed = parse_yolo_line(ln)
            if parsed is None:
                continue
            cls_id, xc, yc, bw, bh, conf = parsed

            if (CONF_THRES is not None) and (conf is not None) and (conf < CONF_THRES):
                continue

            x1, y1, x2, y2 = yolo_xywh_to_xyxy(xc, yc, bw, bh, W, H)
            dets.append((cls_id, conf, x1, y1, x2, y2))

    if not dets:
        continue

    dets_sorted = sorted(dets, key=lambda x: (-x[1] if x[1] is not None else 0.0))
    if TOPK is not None:
        dets_sorted = dets_sorted[:TOPK]

    per_img_crop_root = os.path.join(crop_dir, stem)
    os.makedirs(per_img_crop_root, exist_ok=True)

    for i, (cls_id, conf, x1, y1, x2, y2) in enumerate(dets_sorted):
        cv2.rectangle(img_vis, (x1, y1), (x2, y2), default_color, thickness)

        if conf is None:
            label_text = f"{cls_id}"
        else:
            label_text = f"{cls_id}:{conf:.3f}"

        text_y = y1 - 6
        if text_y < 10:
            text_y = y1 + 20
        cv2.putText(img_vis, label_text, (x1, text_y), font, font_scale, default_color, font_thickness)

        patch = safe_crop(img, x1, y1, x2, y2)
        if patch is None:
            continue

        cls_folder = os.path.join(per_img_crop_root, f"cls_{cls_id}")
        os.makedirs(cls_folder, exist_ok=True)

        conf_str = "NA" if conf is None else f"{conf:.4f}"
        crop_name = f"{stem}_box{i:04d}_cls{cls_id}_conf{conf_str}_x{x1}_y{y1}_w{x2-x1}_h{y2-y1}.png"
        crop_path = os.path.join(cls_folder, crop_name)
        cv2.imwrite(crop_path, patch)
        total_crops += 1

    out_vis_path = os.path.join(vis_dir, os.path.basename(img_path))
    cv2.imwrite(out_vis_path, img_vis)
    processed += 1
    print(f"Saved vis: {out_vis_path}")

print(f"Finished! processed={processed}, missing_images={missing_images}, label_files={len(txt_files)}, total_crops={total_crops}")
