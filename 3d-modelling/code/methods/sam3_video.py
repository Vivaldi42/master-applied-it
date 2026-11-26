"""Method 1: SAM 3 detection and tracking, count = number of distinct IDs.

Usage:  python sam3_video.py <frames-dir> <asset-types.csv> <run-dir>     (conda env sam3)
Output: <run-dir>/counts.csv                         asset,count (empty: detection failed)
        <run-dir>/method-stats.csv                   asset,seconds,peak_gpu_gb per asset type
        <run-dir>/detect/<asset>/detections.csv      one row per object per frame
        <run-dir>/detect/<asset>/overlays/id<NNN>/   every frame in which the object is visible
        <run-dir>/detect/<asset>.log                 output of SAM 3 for this asset type

Each asset type runs in its own process, so that a failure stops only that asset type.
One asset type runs per GPU at a time. Set the GPUs with the variable GPUS, for example GPUS=1.
"""
import csv
import os
import subprocess
import sys
import time

FPS = 10  # frame rate of the extracted frames (run_pipeline.py)


def file_name(asset):
    return asset.replace(" ", "_")


def detect(frames_dir, prompt, detect_dir):
    """Run SAM 3 with one text prompt on all frames. Runs in its own process."""
    import cv2
    import numpy as np
    import torch
    from sam3.model.sam3_video_inference import Sam3VideoInference
    from sam3.model_builder import build_sam3_video_predictor

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
    original = Sam3VideoInference._construct_initial_input_batch
    Sam3VideoInference._construct_initial_input_batch = (
        lambda self, state, images: original(self, state, CpuFrames(images)))

    asset_dir = os.path.join(detect_dir, file_name(prompt))
    overlay_dir = os.path.join(asset_dir, "overlays")
    os.makedirs(overlay_dir)

    def save_overlays(frame_idx, obj_ids, masks, boxes):
        """Save the frame once per visible object, in one folder per ID, with a box."""
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
    predictor.handle_request(dict(type="add_prompt", session_id=sid, frame_index=0, text=prompt))

    seen_ids = set()
    with open(os.path.join(asset_dir, "detections.csv"), "w", newline="") as f:
        det = csv.writer(f)
        det.writerow(["prompt", "frame", "obj_id", "prob", "x", "y", "w", "h"])
        for resp in predictor.handle_stream_request(dict(
                type="propagate_in_video", session_id=sid, evict_cached_frame_outputs=True)):
            frame_idx = resp["frame_index"]
            out = resp["outputs"]
            obj_ids = out["out_obj_ids"].tolist()
            probs = np.asarray(out["out_probs"]).tolist()
            boxes = np.asarray(out["out_boxes_xywh"]).tolist()  # relative to image size
            for obj_id, p, b in zip(obj_ids, probs, boxes):
                det.writerow([prompt, frame_idx, obj_id, f"{p:.3f}"] + [f"{v:.4f}" for v in b])
            if frame_idx % 100 == 0:
                gb = torch.cuda.memory_allocated() / 1e9
                print(f"frame {frame_idx}: GPU memory allocated {gb:.1f} GB", flush=True)
            seen_ids |= set(obj_ids)
            if obj_ids:
                save_overlays(frame_idx, obj_ids, np.asarray(out["out_binary_masks"]), boxes)

    peak = torch.cuda.max_memory_allocated() / 1e9
    print(f"=== {prompt}: {len(seen_ids)} distinct IDs, peak GPU memory {peak:.1f} GB", flush=True)
    with open(os.path.join(asset_dir, "peak_gpu_gb.txt"), "w") as f:
        f.write(f"{peak:.1f}\n")
    predictor.handle_request(dict(type="close_session", session_id=sid))
    predictor.shutdown()


def main(frames_dir, assets_path, run_dir):
    with open(assets_path, newline="") as f:
        assets = [row[0].strip() for row in list(csv.reader(f))[1:] if row and row[0].strip()]
    detect_dir = os.path.join(run_dir, "detect")
    os.makedirs(detect_dir)
    gpus = os.environ.get("GPUS", "0 1").split()

    # Start one process per asset type, one per GPU at a time
    waiting, running, completed, seconds = list(assets), {}, set(), {}
    while waiting or running:
        for gpu in gpus:
            if gpu not in running and waiting:
                asset = waiting.pop(0)
                log = open(os.path.join(detect_dir, file_name(asset) + ".log"), "w")
                env = dict(os.environ, CUDA_VISIBLE_DEVICES=gpu,
                           PYTORCH_ALLOC_CONF="expandable_segments:True")
                proc = subprocess.Popen(
                    [sys.executable, os.path.abspath(__file__), "--detect", frames_dir, asset, detect_dir],
                    stdout=log, stderr=subprocess.STDOUT, env=env)
                running[gpu] = (asset, proc, log, time.time())
                print(f"{asset}: started on GPU {gpu}", flush=True)
        for gpu, (asset, proc, log, started) in list(running.items()):
            if proc.poll() is not None:
                log.close()
                del running[gpu]
                seconds[asset] = time.time() - started
                if proc.returncode == 0:
                    completed.add(asset)
                    print(f"{asset}: finished in {seconds[asset] / 60:.1f} min", flush=True)
                else:
                    print(f"{asset}: FAILED, see {log.name}", flush=True)
        time.sleep(1)

    # Time and peak GPU memory per asset type (time includes loading the model and the frames)
    with open(os.path.join(run_dir, "method-stats.csv"), "x", newline="") as f:
        out = csv.writer(f)
        out.writerow(["asset", "seconds", "peak_gpu_gb"])
        for asset in assets:
            peak_file = os.path.join(detect_dir, file_name(asset), "peak_gpu_gb.txt")
            peak = open(peak_file).read().strip() if os.path.exists(peak_file) else ""
            out.writerow([asset, f"{seconds[asset]:.1f}", peak])

    # Asset list: number of distinct IDs per asset type, empty if detection failed
    with open(os.path.join(run_dir, "counts.csv"), "x", newline="") as f:
        out = csv.writer(f)
        out.writerow(["asset", "count"])
        for asset in assets:
            if asset not in completed:
                out.writerow([asset, ""])
                continue
            with open(os.path.join(detect_dir, file_name(asset), "detections.csv"), newline="") as d:
                out.writerow([asset, len({row["obj_id"] for row in csv.DictReader(d)})])


if __name__ == "__main__":
    if sys.argv[1] == "--detect":
        detect(*sys.argv[2:5])
    else:
        main(*sys.argv[1:4])
