import json
import csv
import time
import statistics
from pathlib import Path

import joblib
import numpy as np


input_dir = Path("./classification_results_restoration")
model_path = Path("./lgbm_ordering_model.pkl")
out_csv = Path("./ordering_lgbm_pairwise_fps_30runs.csv")

REPEAT = 30

model = joblib.load(model_path)


def make_pair_features(a, b):
    return [
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
    ]


def json_data_to_text(data) -> str:
    rows = []

    for idx, item in enumerate(data):
        char = item["char"][0]
        x, y, w, h = item["bbox"]

        rows.append({
            "id": idx,
            "char": char,
            "x": x,
            "y": y,
            "w": w,
            "h": h,
            "cx": x + w / 2,
            "cy": y + h / 2,
            "score": 0.0,
        })

    if len(rows) == 0:
        return ""

    n = len(rows)

    pair_features = []
    pair_indices = []

    for i in range(n):
        for j in range(i + 1, n):
            pair_features.append(make_pair_features(rows[i], rows[j]))
            pair_indices.append((i, j))

    if len(pair_features) == 0:
        return rows[0]["char"]

    probs = model.predict_proba(
        np.array(pair_features)
    )[:, 1]

    for (i, j), prob_a_before_b in zip(pair_indices, probs):
        rows[i]["score"] += prob_a_before_b
        rows[j]["score"] += 1.0 - prob_a_before_b

    ordered = sorted(rows, key=lambda r: r["score"], reverse=True)

    return "".join(r["char"] for r in ordered)


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
    total_pairs = 0

    t0 = time.perf_counter()

    for item in all_data:
        data = item["data"]
        text = json_data_to_text(data)

        n = len(data)
        total_pairs += n * (n - 1) // 2
        total_chars += len(text)

    total_time = time.perf_counter() - t0

    page_fps = total_pages / total_time if total_time > 0 else 0.0
    char_fps = total_chars / total_time if total_time > 0 else 0.0
    pair_fps = total_pairs / total_time if total_time > 0 else 0.0

    page_latency_s = total_time / total_pages if total_pages > 0 else 0.0
    char_latency_ms = total_time / total_chars * 1000 if total_chars > 0 else 0.0

    return {
        "total_time_s": total_time,
        "pages": total_pages,
        "chars": total_chars,
        "pairs": total_pairs,
        "page_fps": page_fps,
        "char_fps": char_fps,
        "pair_fps": pair_fps,
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
            "pairs",
            "page_fps",
            "char_fps",
            "pair_fps",
            "page_latency_s",
            "char_latency_ms",
        ]

        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(records)

    time_list = [r["total_time_s"] for r in records]
    page_fps_list = [r["page_fps"] for r in records]
    char_fps_list = [r["char_fps"] for r in records]
    pair_fps_list = [r["pair_fps"] for r in records]

    print("=" * 60)
    print("LGBM pairwise ordering pure processing benchmark")
    print(f"Runs: {REPEAT}")
    print(f"Pages per run: {records[0]['pages']}")
    print(f"Chars per run: {records[0]['chars']}")
    print(f"Pairs per run: {records[0]['pairs']}")
    print(f"Total time: {statistics.mean(time_list):.6f} ± {statistics.stdev(time_list):.6f} s")
    print(f"Page FPS: {statistics.mean(page_fps_list):.2f} ± {statistics.stdev(page_fps_list):.2f} pages/s")
    print(f"Char FPS: {statistics.mean(char_fps_list):.2f} ± {statistics.stdev(char_fps_list):.2f} chars/s")
    print(f"Pair FPS: {statistics.mean(pair_fps_list):.2f} ± {statistics.stdev(pair_fps_list):.2f} pairs/s")
    print(f"CSV saved to: {out_csv}")
    print("=" * 60)


if __name__ == "__main__":
    main()
