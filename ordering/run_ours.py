import json
import argparse
from pathlib import Path
import numpy as np

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


def main(args):
    input_dir = Path(args.input_dir)
    output_dir = Path(args.output_dir)

    output_dir.mkdir(parents=True, exist_ok=True)

    json_paths = sorted(input_dir.glob("*.json"))

    if not json_paths:
        raise RuntimeError(f"No JSON files found in: {input_dir}")

    for json_path in json_paths:
        text = json_to_text(json_path)

        txt_path = output_dir / f"{json_path.stem}.txt"

        with open(txt_path, "w", encoding="utf-8") as f:
            f.write(text)

        print(f"Saved: {txt_path} | Characters: {len(text)}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input_dir", type=str, required=True, help="Directory containing classification JSON files")
    parser.add_argument("--output_dir", type=str, required=True, help="Directory to save ordered text files")
    args = parser.parse_args()
    main(args)