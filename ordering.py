import json
from pathlib import Path
import numpy as np

input_dir = Path("./classification_results_restoration")
output_dir = Path("./order_results_baseline")
output_dir.mkdir(parents=True, exist_ok=True)


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

    output_chars = []

    for col in columns:

        items = sorted(
            col["items"],
            key=lambda r: r["cy"]
        )

        output_chars.extend(
            item["char"] for item in items
        )

    return "".join(output_chars)


for json_path in sorted(input_dir.glob("*.json")):

    text = json_to_text(json_path)

    txt_path = output_dir / f"{json_path.stem}.txt"

    with open(txt_path, "w", encoding="utf-8") as f:
        f.write(text)

    print(f"Saved: {txt_path} | Characters: {len(text)}")