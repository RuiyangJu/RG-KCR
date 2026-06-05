import json
import argparse
from pathlib import Path
import joblib
import numpy as np

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


def json_to_text(json_path: Path, model) -> str:
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

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

    probs = model.predict_proba(np.array(pair_features))[:, 1]

    for (i, j), prob_a_before_b in zip(pair_indices, probs):
        rows[i]["score"] += prob_a_before_b
        rows[j]["score"] += 1.0 - prob_a_before_b

    ordered = sorted(rows, key=lambda r: r["score"], reverse=True)

    return "".join(r["char"] for r in ordered)


def main(args):
    input_dir = Path(args.input_dir)
    output_dir = Path(args.output_dir)
    model_path = Path(args.model)

    output_dir.mkdir(parents=True, exist_ok=True)

    model = joblib.load(model_path)

    json_paths = sorted(input_dir.glob("*.json"))

    if not json_paths:
        raise RuntimeError(f"No JSON files found in: {input_dir}")

    for json_path in json_paths:
        text = json_to_text(json_path, model)

        txt_path = output_dir / f"{json_path.stem}.txt"

        with open(txt_path, "w", encoding="utf-8") as f:
            f.write(text)

        print(f"Saved: {txt_path} | Characters: {len(text)}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input_dir", type=str, required=True, help="Directory containing classification JSON files")
    parser.add_argument("--output_dir", type=str, required=True, help="Directory to save ordered text files")
    parser.add_argument("--model", type=str, default="./ordering/lgbm_ordering_model.pkl", help="Path to LightGBM ordering model")
    args = parser.parse_args()
    main(args)
