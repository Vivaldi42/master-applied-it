# Review stage: one picture per detected object, for a person to accept or reject.
#
# Usage:  python review.py <frames-dir> <detect-dir> <asset-list.csv> <out-dir>
# Output: <out-dir>/<asset>_id<NNN>.jpg  left: largest view in the first visible period,
#                                        right: largest view in the whole video
#         <out-dir>/review.csv           columns asset,id,picture,verdict (verdict is empty)
import csv
import os
import sys

import cv2
import numpy as np

MAX_GAP = 5  # frames without the object that end the first visible period

frames_dir, detect_dir, asset_list, out_dir = sys.argv[1:5]
os.makedirs(out_dir)  # a run never overwrites an earlier run


def area(row):
    return float(row["w"]) * float(row["h"])


def draw(row, title):
    img = cv2.imread(os.path.join(frames_dir, f"{int(row['frame']):05d}.jpg"))
    height, width = img.shape[:2]
    x, y, w, h = (float(row[k]) * s for k, s in zip("xywh", (width, height, width, height)))
    cv2.rectangle(img, (int(x), int(y)), (int(x + w), int(y + h)), (0, 0, 255), 6)
    img = cv2.resize(img, (960, int(height * 960 / width)))
    bar = np.zeros((50, 960, 3), np.uint8)
    cv2.putText(bar, title, (10, 36), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
    return np.vstack([bar, img])


with open(asset_list, newline="") as f:
    assets = [row[0] for row in list(csv.reader(f))[1:] if row]

with open(os.path.join(out_dir, "review.csv"), "w", newline="") as f:
    out = csv.writer(f)
    out.writerow(["asset", "id", "picture", "verdict"])
    for asset in assets:
        name = asset.replace(" ", "_")
        log_path = os.path.join(detect_dir, name + ".log")
        log = open(log_path, errors="replace").read() if os.path.exists(log_path) else ""
        if f"=== {asset}:" not in log:  # no final line: detection failed or did not run
            out.writerow([asset, "", "", "DETECTION FAILED"])
            continue
        objects = {}
        with open(os.path.join(detect_dir, name, "detections.csv"), newline="") as d:
            for row in csv.DictReader(d):
                objects.setdefault(int(row["obj_id"]), []).append(row)
        if not objects:
            out.writerow([asset, "", "", "NOTHING FOUND"])
        for obj_id, rows in sorted(objects.items()):
            first = [rows[0]]
            for row in rows[1:]:
                if int(row["frame"]) - int(first[-1]["frame"]) > MAX_GAP:
                    break
                first.append(row)
            picture = f"{name}_id{obj_id:03d}.jpg"
            cv2.imwrite(os.path.join(out_dir, picture), np.hstack([
                draw(max(first, key=area), f"{asset} {obj_id}: first period"),
                draw(max(rows, key=area), f"{asset} {obj_id}: largest view")]))
            out.writerow([asset, obj_id, picture, ""])
