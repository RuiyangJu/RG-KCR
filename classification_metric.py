import os
import json
import argparse
from typing import List, Dict, Tuple

def load_json_list(path: str) -> List[Dict]:
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    if not isinstance(data, list):
        raise ValueError(f"JSON root is not a list: {path}")
    return data

def xywh_to_xyxy(b: List[float]) -> Tuple[float, float, float, float]:
    x, y, w, h = b
    return (x, y, x + w, y + h)

def iou_xywh(a: List[float], b: List[float]) -> float:
    ax1, ay1, ax2, ay2 = xywh_to_xyxy(a)
    bx1, by1, bx2, by2 = xywh_to_xyxy(b)

    inter_x1 = max(ax1, bx1)
    inter_y1 = max(ay1, by1)
    inter_x2 = min(ax2, bx2)
    inter_y2 = min(ay2, by2)

    inter_w = max(0.0, inter_x2 - inter_x1)
    inter_h = max(0.0, inter_y2 - inter_y1)
    inter_area = inter_w * inter_h

    a_area = max(0.0, ax2 - ax1) * max(0.0, ay2 - ay1)
    b_area = max(0.0, bx2 - bx1) * max(0.0, by2 - by1)
    denom = a_area + b_area - inter_area
    if denom <= 0:
        return 0.0
    return inter_area / denom

def safe_first_char(x) -> str:
    if isinstance(x, list) and len(x) > 0:
        return str(x[0])
    return str(x) if x is not None else ""


def safe_pred_list(x) -> List[str]:
    if isinstance(x, list):
        return [str(t) for t in x]
    if x is None:
        return []
    return [str(x)]


def match_by_iou_greedy(
    gt_items: List[Dict],
    pred_items: List[Dict],
    iou_thr: float
) -> List[Tuple[int, int, float]]:
    
    candidates = []
    for gi, g in enumerate(gt_items):
        gb = g.get("bbox", None)
        if not (isinstance(gb, list) and len(gb) == 4):
            continue
        for pi, p in enumerate(pred_items):
            pb = p.get("bbox", None)
            if not (isinstance(pb, list) and len(pb) == 4):
                continue
            v = iou_xywh(gb, pb)
            if v >= iou_thr:
                candidates.append((v, gi, pi))

    candidates.sort(reverse=True, key=lambda x: x[0])

    used_g = set()
    used_p = set()
    matches = []
    for v, gi, pi in candidates:
        if gi in used_g or pi in used_p:
            continue
        used_g.add(gi)
        used_p.add(pi)
        matches.append((gi, pi, v))

    return matches

def eval_one_file(gt_path: str, pred_path: str, iou_thr: float) -> Dict:
    gt = load_json_list(gt_path)
    pred = load_json_list(pred_path)

    gt_items = [x for x in gt if isinstance(x, dict)]
    pred_items = [x for x in pred if isinstance(x, dict)]

    matches = match_by_iou_greedy(gt_items, pred_items, iou_thr)

    top1_ok = 0
    top5_ok = 0

    for gi, pi, _ in matches:
        gt_char = safe_first_char(gt_items[gi].get("char"))
        pred_list = safe_pred_list(pred_items[pi].get("char"))
        if len(pred_list) >= 1 and pred_list[0] == gt_char:
            top1_ok += 1
        if gt_char in pred_list[:5]:
            top5_ok += 1

    denom = len(matches)
    return {
        "matches": denom,
        "top1_ok": top1_ok,
        "top5_ok": top5_ok,
        "top1_acc": (top1_ok / denom) if denom > 0 else None,
        "top5_acc": (top5_ok / denom) if denom > 0 else None,
        "gt_count": len(gt_items),
        "pred_count": len(pred_items),
    }

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--gt_dir", type=str, default="./classification_gt", help="Folder of classification_gt jsons")
    ap.add_argument("--pred_dir", type=str, default="./classification_results_raw", help="Folder of classification_results jsons")
    ap.add_argument("--iou", type=float, default=0.5, help="IoU threshold for matching (default 0.5)")
    ap.add_argument("--ext", type=str, default=".json", help="File extension (default .json)")
    ap.add_argument("--per_file", action="store_true", help="Print per-file stats")
    args = ap.parse_args()

    gt_dir = args.gt_dir
    pred_dir = args.pred_dir
    iou_thr = args.iou
    ext = args.ext

    gt_files = {f for f in os.listdir(gt_dir) if f.endswith(ext)}
    pred_files = {f for f in os.listdir(pred_dir) if f.endswith(ext)}
    common = sorted(gt_files & pred_files)

    if len(common) == 0:
        raise RuntimeError("No common json filenames found between gt_dir and pred_dir.")

    total_matches = 0
    total_top1_ok = 0
    total_top5_ok = 0
    total_gt = 0
    total_pred = 0
    files_used = 0

    for fn in common:
        gt_path = os.path.join(gt_dir, fn)
        pred_path = os.path.join(pred_dir, fn)

        res = eval_one_file(gt_path, pred_path, iou_thr)
        files_used += 1
        total_matches += res["matches"]
        total_top1_ok += res["top1_ok"]
        total_top5_ok += res["top5_ok"]
        total_gt += res["gt_count"]
        total_pred += res["pred_count"]

        if args.per_file:
            t1 = "NA" if res["top1_acc"] is None else f"{res['top1_acc']*100:.2f}%"
            t5 = "NA" if res["top5_acc"] is None else f"{res['top5_acc']*100:.2f}%"
            print(f"{fn} | matches={res['matches']} gt={res['gt_count']} pred={res['pred_count']} | top1={t1} top5={t5}")

    overall_top1 = (total_top1_ok / total_matches) if total_matches > 0 else 0.0
    overall_top5 = (total_top5_ok / total_matches) if total_matches > 0 else 0.0

    print(f"Files evaluated: {files_used}")
    print(f"Total GT labels: {total_gt}")
    print(f"Total Pred labels: {total_pred}")
    print(f"Total matched pairs (IoU>={iou_thr}): {total_matches}")
    print(f"Top-1: {total_top1_ok}/{total_matches} = {overall_top1*100:.2f}%")
    print(f"Top-5: {total_top5_ok}/{total_matches} = {overall_top5*100:.2f}%")

if __name__ == "__main__":
    main()