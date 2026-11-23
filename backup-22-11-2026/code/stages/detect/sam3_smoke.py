# Smoke test: does SAM 3 load, and what does its video output look like?
import os
import sys

import cv2
import numpy as np
from sam3.model_builder import build_sam3_video_predictor

frames_dir, prompt = sys.argv[1], sys.argv[2]

# An overlay image is saved for each frame in which a new ID appears.
# One folder per prompt, so runs with different prompts do not overwrite each other.
seen_ids = set()
# Extra frames to save for manual checks (e.g. suspected ID swaps)
extra_frames = {1649}
out_dir = os.path.join(os.path.dirname(frames_dir.rstrip("/")),
                       "overlays-" + prompt.replace(" ", "_"))
os.makedirs(out_dir, exist_ok=True)

predictor = build_sam3_video_predictor(gpus_to_use=[0])

session = predictor.handle_request(dict(
    type="start_session", resource_path=frames_dir,
    offload_video_to_cpu=True))
sid = session["session_id"]

predictor.handle_request(dict(
    type="add_prompt", session_id=sid, frame_index=0, text=prompt))

for resp in predictor.handle_stream_request(dict(
        type="propagate_in_video", session_id=sid,
        # Drop each frame's result after it is yielded, to keep GPU memory flat
        evict_cached_frame_outputs=True)):
    out = resp["outputs"]
    print(resp["frame_index"], list(out.keys()), out["out_obj_ids"].tolist())

    f = resp["frame_index"]
    ids = set(out["out_obj_ids"].tolist())
    new_ids = ids - seen_ids
    seen_ids |= ids
    if new_ids or f in extra_frames:
        img = cv2.imread(os.path.join(frames_dir, f"{f:05d}.jpg"))
        masks = np.asarray(out["out_binary_masks"])
        for obj_id, m in zip(out["out_obj_ids"].tolist(), masks):
            # Blend the mask pixels with a colour derived from the ID
            color = np.array([(obj_id * 70) % 256, (obj_id * 150) % 256,
                              255 - (obj_id * 40) % 256])
            img[m] = (0.5 * img[m] + 0.5 * color).astype(np.uint8)
            # Write the ID at the mask centre
            ys, xs = np.nonzero(m)
            cv2.putText(img, str(obj_id), (int(xs.mean()), int(ys.mean())),
                        cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255, 255, 255), 3)
        cv2.imwrite(os.path.join(out_dir, f"{f:05d}.jpg"), img)

predictor.handle_request(dict(type="close_session", session_id=sid))
predictor.shutdown()
