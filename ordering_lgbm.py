import json
from pathlib import Path
import numpy as np
import joblib

input_dir = Path("./classification_results_restoration")
output_dir = Path("./order_results_lgbm")
output_dir.mkdir(parents=True, exist_ok=True)
model = joblib.load("./lgbm_ordering_model.pkl")


def make_pair_features(a, b):
    return [[
        a["cx"] - b["cx"],
        a["cy"] - b["cy"],
        abs(a["cx"] - b["cx"]),
        abs(a["cy"] - b["cy"]),

        a["w"] - b["w"],
        a["h"] - b["h"],
        abs(a["w"] - b["w"]),
        abs(a["h"] - b["h"]),

        a["cx"],
        a["cy"],
        b["cx"],
        b["cy"],

        a["w"],
        a["h"],
        b["w"],
        b["h"],
    ]]


def refine_with_lgbm(ordered_rows, max_iter=3, threshold=0.5):
    rows = ordered_rows[:]

    for _ in range(max_iter):
        changed = False

        for i in range(len(rows) - 1):
            a = rows[i]
            b = rows[i + 1]

            prob_a_before_b = model.predict_proba(
                make_pair_features(a, b)
            )[0][1]

            if prob_a_before_b < threshold:
                rows[i], rows[i + 1] = rows[i + 1], rows[i]
                changed = True

        if not changed:
            break

    return rows


def json_to_text(json_path: Path) -> str:
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    rows = []

    for item in data:
        char = item["char"][0]
        x, y, w, h = item["bbox"]

        rows.append({
            "char": char,
            "x": x,
            "y": y,
            "w": w,
            "h": h,
            "cx": x + w / 2,
            "cy": y + h / 2,
        })

    if len(rows) == 0:
        return ""

    avg_w = sum(r["w"] for r in rows) / len(rows)
    column_thresh = avg_w * 0.8

    rows = sorted(rows, key=lambda r: r["cx"], reverse=True)

    columns = []

    for r in rows:
        matched_col = None
        min_dist = float("inf")

        for col in columns:
            dist = abs(r["cx"] - col["median_cx"])

            if dist < min_dist:
                min_dist = dist
                matched_col = col

        if matched_col is not None and min_dist <= column_thresh:
            matched_col["items"].append(r)
            matched_col["median_cx"] = np.median(
                [item["cx"] for item in matched_col["items"]]
            )
        else:
            columns.append({
                "median_cx": r["cx"],
                "items": [r],
            })

    columns = sorted(
        columns,
        key=lambda c: c["median_cx"],
        reverse=True
    )

    ordered_rows = []

    for col in columns:
        items = sorted(col["items"], key=lambda r: r["cy"])
        ordered_rows.extend(items)

    ordered_rows = refine_with_lgbm(
        ordered_rows,
        max_iter=3,
        threshold=0.5
    )

    return "".join(r["char"] for r in ordered_rows)


for json_path in sorted(input_dir.glob("*.json")):
    text = json_to_text(json_path)

    txt_path = output_dir / f"{json_path.stem}.txt"

    with open(txt_path, "w", encoding="utf-8") as f:
        f.write(text)

    print(f"Saved: {txt_path} | Characters: {len(text)}")