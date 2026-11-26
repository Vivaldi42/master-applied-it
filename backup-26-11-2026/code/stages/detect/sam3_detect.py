# Stage 4 (detect): run SAM 3 with one text prompt on a frame folder.
#
# Usage:  python sam3_detect.py <frames-dir> <prompt> <out-dir>
# Output: <out-dir>/<prompt>/detections.csv  one row per object per frame
#         <out-dir>/<prompt>/overlays/id<NNN>/  every frame in which the object is visible
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
from sam3.model.sam3_video_inference import Sam3VideoInference


class CpuFrames:
    """Keeps all frames in CPU memory and moves one frame to the GPU when it is read.

    SAM 3 copies the whole frame batch to the GPU even with offload_video_to_cpu.
    Its copy function skips objects without a .to() method, so this class has none.
    """

    def __init__(self, frames):
        self.frames = frames

    def __len__(self):
        return len(self.frames)

    def __getitem__(self, idx):
        return self.frames[idx].cuda()


# Replace the frame batch at runtime, so that external/sam3 stays unmodified
original_construct = Sam3VideoInference._construct_initial_input_batch
Sam3VideoInference._construct_initial_input_batch = (
    lambda self, state, images: original_construct(self, state, CpuFrames(images)))

frames_dir, prompt, out_dir = sys.argv[1], sys.argv[2], sys.argv[3]

FPS = 10  # frame rate of the extracted frames (run_mvp.sh)

prompt_dir = os.path.join(out_dir, prompt.replace(" ", "_"))
overlay_dir = os.path.join(prompt_dir, "overlays")
os.makedirs(overlay_dir, exist_ok=False)  # a run never overwrites an earlier run
det_file = open(os.path.join(prompt_dir, "detections.csv"), "w", newline="")
det = csv.writer(det_file)
det.writerow(["prompt", "frame", "obj_id", "prob", "x", "y", "w", "h"])


def save_overlays(frame_idx, obj_ids, masks, boxes):
    """Save the frame once per visible object, in one folder per object ID.

    The object of the folder has a thick box, so that small objects can be found.
    """
    img = cv2.imread(os.path.join(frames_dir, f"{frame_idx:05d}.jpg"))
    height, width = img.shape[:2]
    colors = [((i * 70) % 256, (i * 150) % 256, 255 - (i * 40) % 256) for i in obj_ids]
    for m, color in zip(masks, colors):
        img[m] = (0.5 * img[m] + 0.5 * np.array(color)).astype(np.uint8)

    for obj_id, m, box, color in zip(obj_ids, masks, boxes, colors):
        if not m.any():  # SAM 3 can return an object with an empty mask
            continue
        x, y, w, h = (int(v * s) for v, s in zip(box, (width, height, width, height)))
        out = img.copy()
        cv2.rectangle(out, (x, y), (x + w, y + h), color, 4)
        cv2.putText(out, f"{prompt} ID {obj_id}  {frame_idx / FPS:.1f} s", (20, 60),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.8, (0, 255, 255), 4)
        id_dir = os.path.join(overlay_dir, f"id{obj_id:03d}")
        os.makedirs(id_dir, exist_ok=True)
        cv2.imwrite(os.path.join(id_dir, f"{frame_idx:05d}.jpg"),
                    cv2.resize(out, (1280, int(height * 1280 / width))))


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

    seen_ids |= set(obj_ids)
    if obj_ids:
        save_overlays(f, obj_ids, np.asarray(out["out_binary_masks"]), boxes)

det_file.close()
peak = torch.cuda.max_memory_allocated() / 1e9
print(f"=== {prompt}: {len(seen_ids)} distinct IDs, peak GPU memory {peak:.1f} GB",
      flush=True)

predictor.handle_request(dict(type="close_session", session_id=sid))
predictor.shutdown()
