from pathlib import Path
import argparse
import pandas as pd

def levenshtein_distance(s1, s2):
    m, n = len(s1), len(s2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    for i in range(m + 1):
        dp[i][0] = i

    for j in range(n + 1):
        dp[0][j] = j

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            cost = 0 if s1[i - 1] == s2[j - 1] else 1
            dp[i][j] = min(
                dp[i - 1][j] + 1,
                dp[i][j - 1] + 1,
                dp[i - 1][j - 1] + cost
            )

    return dp[m][n]


def compute_cer(gt, pred):
    if len(gt) == 0:
        return 0.0 if len(pred) == 0 else 1.0

    dist = levenshtein_distance(gt, pred)
    return dist / len(gt)


def main(args):
    gt_dir = Path(args.gt_dir)
    pred_dir = Path(args.pred_dir)
    out_csv = args.out_csv

    gt_files = {f.name: f for f in gt_dir.glob("*.txt")}
    pred_files = {f.name: f for f in pred_dir.glob("*.txt")}
    common_files = sorted(set(gt_files.keys()) & set(pred_files.keys()))

    print(f"GT txt files: {len(gt_files)}")
    print(f"Pred txt files: {len(pred_files)}")
    print(f"Common files: {len(common_files)}")

    if not common_files:
        raise RuntimeError("No common txt files found between gt_dir and pred_dir.")

    results = []

    total_gt_chars = 0
    total_edit_distance = 0

    for fname in common_files:
        gt_path = gt_files[fname]
        pred_path = pred_files[fname]

        with open(gt_path, "r", encoding="utf-8") as f:
            gt_text = f.read().strip()

        with open(pred_path, "r", encoding="utf-8") as f:
            pred_text = f.read().strip()

        cer = compute_cer(gt_text, pred_text)
        edit_distance = levenshtein_distance(gt_text, pred_text)

        total_gt_chars += len(gt_text)
        total_edit_distance += edit_distance

        results.append({
            "File": fname,
            "GT_Length": len(gt_text),
            "Pred_Length": len(pred_text),
            "Edit_Distance": edit_distance,
            "CER": cer
        })

        print(f"{fname} | CER: {cer:.4f}")

    overall_cer = (
        total_edit_distance / total_gt_chars
        if total_gt_chars > 0 else 0
    )

    print(f"Total Files: {len(common_files)}")
    print(f"Total GT Characters: {total_gt_chars}")
    print(f"Total Edit Distance: {total_edit_distance}")
    print(f"Overall CER: {overall_cer:.4f}")
    print(f"Overall 1-CER: {1 - overall_cer:.4f}")

    df = pd.DataFrame(results)

    df.loc[len(df)] = {
        "File": "OVERALL",
        "GT_Length": total_gt_chars,
        "Pred_Length": "",
        "Edit_Distance": total_edit_distance,
        "CER": overall_cer
    }

    out_csv_path = Path(out_csv)
    out_csv_path.parent.mkdir(parents=True, exist_ok=True)

    df.to_csv(out_csv_path, index=False, encoding="utf-8-sig")

    print(f"\nSaved CSV: {out_csv_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--gt_dir", type=str, required=True, help="Directory containing ground-truth txt files")
    parser.add_argument("--pred_dir", type=str, required=True, help="Directory containing predicted txt files")
    parser.add_argument("--out_csv", type=str, required=True, help="Path to save output CSV file")
    args = parser.parse_args()
    main(args)