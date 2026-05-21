import json
import csv
import time
import statistics
from pathlib import Path

import numpy as np


input_dir = Path("./classification_results_restoration")
out_csv = Path("./ordering_ours_fps_30runs.csv")

REPEAT = 30


def json_data_to_text(data) -> str:
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
        reverse=True,
    )

    output_chars = []

    for col in columns:
        items = sorted(
            col["items"],
            key=lambda r: r["cy"],
        )

        output_chars.extend(
            item["char"] for item in items
        )

    return "".join(output_chars)


def load_all_json():
    json_paths = sorted(input_dir.glob("*.json"))

    if len(json_paths) == 0:
        raise RuntimeError(f"No JSON files found in: {input_dir}")

    all_data = []

    for json_path in json_paths:
        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        all_data.append({
            "name": json_path.stem,
            "data": data,
            "num_chars": len(data),
        })

    return all_data


def run_once(all_data):
    total_pages = len(all_data)
    total_chars = 0

    t0 = time.perf_counter()

    for item in all_data:
        text = json_data_to_text(item["data"])
        total_chars += len(text)

    total_time = time.perf_counter() - t0

    page_fps = total_pages / total_time if total_time > 0 else 0.0
    char_fps = total_chars / total_time if total_time > 0 else 0.0
    page_latency_s = total_time / total_pages if total_pages > 0 else 0.0
    char_latency_ms = total_time / total_chars * 1000 if total_chars > 0 else 0.0

    return {
        "total_time_s": total_time,
        "pages": total_pages,
        "chars": total_chars,
        "page_fps": page_fps,
        "char_fps": char_fps,
        "page_latency_s": page_latency_s,
        "char_latency_ms": char_latency_ms,
    }


def main():
    all_data = load_all_json()

    records = []

    for run_idx in range(1, REPEAT + 1):
        result = run_once(all_data)
        result["run"] = run_idx
        records.append(result)

    with open(out_csv, "w", newline="", encoding="utf-8") as f:
        fieldnames = [
            "run",
            "total_time_s",
            "pages",
            "chars",
            "page_fps",
            "char_fps",
            "page_latency_s",
            "char_latency_ms",
        ]

        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(records)

    time_list = [r["total_time_s"] for r in records]
    page_fps_list = [r["page_fps"] for r in records]
    char_fps_list = [r["char_fps"] for r in records]

    print("=" * 60)
    print("Ours ordering pure processing benchmark")
    print(f"Runs: {REPEAT}")
    print(f"Pages per run: {records[0]['pages']}")
    print(f"Chars per run: {records[0]['chars']}")
    print(f"Total time: {statistics.mean(time_list):.6f} ± {statistics.stdev(time_list):.6f} s")
    print(f"Page FPS: {statistics.mean(page_fps_list):.2f} ± {statistics.stdev(page_fps_list):.2f} pages/s")
    print(f"Char FPS: {statistics.mean(char_fps_list):.2f} ± {statistics.stdev(char_fps_list):.2f} chars/s")
    print(f"CSV saved to: {out_csv}")
    print("=" * 60)


if __name__ == "__main__":
    main()
