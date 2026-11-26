# Detection test: run the SAM 3 image model on single images, without tracking.
#
# Usage:  python sam3_image.py <images-dir> <prompt> <out-dir>
# Output: <out-dir>/boxes.csv    one row per box, verdict column is filled in by hand
#         <out-dir>/overlays/    one image per input image with box numbers and scores
import csv
import glob
import os
import sys

import cv2
import torch
from PIL import Image
from sam3.model.sam3_image_processor import Sam3Processor
from sam3.model_builder import build_sam3_image_model

MIN_SCORE = 0.3  # low, so that other score limits can be tested without a new run

images_dir, prompt, out_dir = sys.argv[1], sys.argv[2], sys.argv[3]
os.makedirs(os.path.join(out_dir, "overlays"))  # a run never overwrites an earlier run

processor = Sam3Processor(build_sam3_image_model(), confidence_threshold=MIN_SCORE)

with open(os.path.join(out_dir, "boxes.csv"), "w", newline="") as f:
    out = csv.writer(f)
    out.writerow(["image", "box", "score", "x1", "y1", "x2", "y2", "verdict"])
    for path in sorted(glob.glob(os.path.join(images_dir, "*.jpg"))):
        name = os.path.splitext(os.path.basename(path))[0]
        with torch.autocast("cuda", dtype=torch.bfloat16):
            state = processor.set_image(Image.open(path).convert("RGB"))
            state = processor.set_text_prompt(prompt, state)
        scores = state["scores"].float().tolist()
        boxes = state["boxes"].float().tolist()

        img = cv2.imread(path)
        order = sorted(range(len(scores)), key=lambda i: -scores[i])
        for n, i in enumerate(order):
            x1, y1, x2, y2 = (int(v) for v in boxes[i])
            out.writerow([name, n, f"{scores[i]:.3f}", x1, y1, x2, y2, ""])
            color = (0, 0, 255) if scores[i] >= 0.5 else (255, 0, 0)  # red: 0.5 or more
            cv2.rectangle(img, (x1, y1), (x2, y2), color, 4)
            cv2.putText(img, f"{n}: {scores[i]:.2f}", (max(x1, 0) + 10, max(y1, 0) + 60),
                        cv2.FONT_HERSHEY_SIMPLEX, 1.8, color, 4)
        cv2.imwrite(os.path.join(out_dir, "overlays", f"{name}.jpg"), img)
        print(f"{name}: {len(scores)} boxes", flush=True)
