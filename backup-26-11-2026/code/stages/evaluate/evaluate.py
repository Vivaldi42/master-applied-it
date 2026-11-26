# Evaluate stage: count error per asset type.
#
# Usage:  python evaluate.py <counts.csv> <ground-truth.csv> <out.csv>
# Input:  <counts.csv> from count.py (asset,count), <ground-truth.csv> (prompt,count)
# Output: <out.csv> with columns asset,truth,predicted,error.
#         error = predicted - truth. Empty if detection failed.
import csv
import sys

counts_path, truth_path, out_path = sys.argv[1], sys.argv[2], sys.argv[3]

with open(counts_path, newline="") as f:
    predicted = {row[0]: row[1] for row in list(csv.reader(f))[1:]}

with open(truth_path, newline="") as f, open(out_path, "x", newline="") as o:
    out = csv.writer(o)
    out.writerow(["asset", "truth", "predicted", "error"])
    for asset, truth in list(csv.reader(f))[1:]:
        pred = predicted.get(asset, "")  # missing or failed asset: empty
        error = int(pred) - int(truth) if pred else ""
        out.writerow([asset, truth, pred, f"{error:+d}" if pred else ""])
