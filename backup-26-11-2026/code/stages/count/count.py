# Count stage: number of distinct track IDs per asset type.
#
# Usage:  python count.py <detect-run-dir> <asset-list.csv> <out.csv>
# Input:  <detect-run-dir>/<asset>/detections.csv and <asset>.log (from run_sam3.sh)
#         <asset-list.csv>: asset types in the first column, header row skipped
# Output: <out.csv> with columns asset,count. The count is empty if detection failed.
import csv
import os
import sys

run_dir, asset_list, out_path = sys.argv[1], sys.argv[2], sys.argv[3]

with open(asset_list, newline="") as f:
    assets = [row[0] for row in list(csv.reader(f))[1:] if row]

with open(out_path, "x", newline="") as f:  # "x": never overwrite an earlier result
    out = csv.writer(f)
    out.writerow(["asset", "count"])
    for asset in assets:
        name = asset.replace(" ", "_")
        log_path = os.path.join(run_dir, name + ".log")
        log = open(log_path, errors="replace").read() if os.path.exists(log_path) else ""
        if f"=== {asset}:" not in log:  # no final line: detection failed or did not run
            out.writerow([asset, ""])
            continue
        with open(os.path.join(run_dir, name, "detections.csv"), newline="") as d:
            ids = {row["obj_id"] for row in csv.DictReader(d)}
        out.writerow([asset, len(ids)])
