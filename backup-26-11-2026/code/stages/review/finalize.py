# Final step: count the objects that a person marked as correct in review.csv.
#
# Usage:  python finalize.py <review.csv> <out.csv>
# Output: <out.csv> with columns asset,count. The count is empty if detection failed.
import csv
import sys

review_path, out_path = sys.argv[1], sys.argv[2]
VERDICTS = {"correct", "duplicate", "wrong", "detection failed", "nothing found"}

counts = {}
with open(review_path, newline="") as f:
    for row in csv.DictReader(f):
        asset, verdict = row["asset"], (row["verdict"] or "").strip().lower()
        if verdict not in VERDICTS:
            sys.exit(f"Error: {asset} {row['id']}: verdict '{verdict}' is missing or unknown")
        if verdict == "detection failed":
            counts[asset] = ""
        else:
            counts[asset] = counts.get(asset, 0) + (verdict == "correct")

with open(out_path, "x", newline="") as f:  # "x": never overwrite an earlier result
    out = csv.writer(f)
    out.writerow(["asset", "count"])
    out.writerows(counts.items())
