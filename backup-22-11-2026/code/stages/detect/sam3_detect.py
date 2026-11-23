# Stage 4 (detect): run SAM 3 with one text prompt on a frame folder.
#
# Usage:  python sam3_detect.py <frames-dir> <prompt> <out-dir>
# Output: <out-dir>/<prompt>/detections.csv  one row per object per frame
#         <out-dir>/<prompt>/overlays/       one image per frame in which a new ID appears
#
# One prompt per process: GPU memory is not fully released between prompts inside
# one process, so run_sam3.sh starts a new process for every prompt.
import csv
import os
import sys

import cv2
import numpy as np
import torch
from sam3.model_builder import build_sam3_video_predictor

frames_dir, prompt, out_dir = sys.argv[1], sys.argv[2], sys.argv[3]

prompt_dir = os.path.join(out_dir, prompt.replace(" ", "_"))
overlay_dir = os.path.join(prompt_dir, "overlays")
os.makedirs(overlay_dir, exist_ok=False)  # a run never overwrites an earlier run
det_file = open(os.path.join(prompt_dir, "detections.csv"), "w", newline="")
det = csv.writer(det_file)
det.writerow(["prompt", "frame", "obj_id", "prob", "x", "y", "w", "h"])


def save_overlay(path, frame_idx, obj_ids, masks):
    img = cv2.imread(os.path.join(frames_dir, f"{frame_idx:05d}.jpg"))
    for obj_id, m in zip(obj_ids, masks):
        color = np.array([(obj_id * 70) % 256, (obj_id * 150) % 256,
                          255 - (obj_id * 40) % 256])
        img[m] = (0.5 * img[m] + 0.5 * color).astype(np.uint8)
        ys, xs = np.nonzero(m)
        cv2.putText(img, str(obj_id), (int(xs.mean()), int(ys.mean())),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255, 255, 255), 3)
    cv2.imwrite(path, img)


predictor = build_sam3_video_predictor(gpus_to_use=[0])

# Frames and tracking state are kept in CPU memory to limit GPU memory
session = predictor.handle_request(dict(
    type="start_session", resource_path=frames_dir,
    offload_video_to_cpu=True, offload_state_to_cpu=True))
sid = session["session_id"]
predictor.handle_request(dict(
    type="add_prompt", session_id=sid, frame_index=0, text=prompt))

seen_ids = set()
for resp in predictor.handle_stream_request(dict(
        type="propagate_in_video", session_id=sid,
        evict_cached_frame_outputs=True)):
    f = resp["frame_index"]
    out = resp["outputs"]
    obj_ids = out["out_obj_ids"].tolist()
    probs = np.asarray(out["out_probs"]).tolist()
    boxes = np.asarray(out["out_boxes_xywh"]).tolist()  # relative to image size

    for obj_id, p, b in zip(obj_ids, probs, boxes):
        det.writerow([prompt, f, obj_id, f"{p:.3f}"] + [f"{v:.4f}" for v in b])

    if f % 100 == 0:
        gb = torch.cuda.memory_allocated() / 1e9
        print(f"frame {f}: GPU memory allocated {gb:.1f} GB", flush=True)

    new_ids = set(obj_ids) - seen_ids
    seen_ids |= new_ids
    if new_ids:
        save_overlay(os.path.join(overlay_dir, f"{f:05d}.jpg"), f, obj_ids,
                     np.asarray(out["out_binary_masks"]))

det_file.close()
peak = torch.cuda.max_memory_allocated() / 1e9
print(f"=== {prompt}: {len(seen_ids)} distinct IDs, peak GPU memory {peak:.1f} GB",
      flush=True)

predictor.handle_request(dict(type="close_session", session_id=sid))
predictor.shutdown()
