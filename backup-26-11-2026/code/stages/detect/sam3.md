# SAM 3 detection (stage 4)

This document describes the SAM 3 detection stage, the settings used in runs `exp002` to `exp005` and the results of these runs. The commands are in `sam3_detect.py` and `run_sam3.sh` in this folder.

## 1. Purpose

The stage detects and tracks the objects that match a text prompt in a room video. The number of distinct track IDs per prompt is the asset count of the room.

Question of the first experiment: is SAM 3 alone (without a 3D model) sufficient to count the assets in a room video? The stakeholder currently needs counts per room and per floor. Positions are not required for now. A per-floor count is the sum of the per-room counts if every video is tagged with room and floor (one video per room, see R4).

## 2. Environment

| Item | Value |
|---|---|
| SAM 3 | `external/sam3`, commit `31cb7e6`, checkpoint `facebook/sam3` (Hugging Face, gated) |
| Conda env | `sam3`, Python 3.12, PyTorch 2.10.0 cu128 |
| Extra dependency | `setuptools<81`. SAM 3 imports `pkg_resources`, which newer versions of setuptools no longer contain. |
| GPU | NVIDIA RTX 4090 (GPU 0). GPU 1 was in use by other users. |

## 3. Input

| Item | Value |
|---|---|
| Room | `room001` (same video as `exp001`) |
| Frames | 10 fps, 1920 x 1080, 1725 frames in `runs/exp002-room001-none-sam3/frames/` |
| Ground truth | `data/room001/ground-truth.csv`, one row per prompt with the hand count |

```
ffmpeg -i data/room001/video.mp4 -vf "fps=10,scale=1920:-2" -q:v 2 -start_number 0 <run>/frames/%05d.jpg
```

- 10 fps was selected over the 2 fps of `exp001` because smaller motion between frames gives the tracker its best input.
- SAM 3 resizes frames internally, so 4K input adds only decoding time and memory.

## 4. Procedure

- One text prompt is added at frame 0. SAM 3 detects all matching objects and tracks them through the video. New objects receive new IDs.
- Count rule: number of distinct IDs per prompt over the whole video.
- Each prompt runs in a separate process (`run_sam3.sh`), because GPU memory is not fully released between prompts in one process.
- Memory settings: `offload_video_to_cpu`, `offload_state_to_cpu` and `evict_cached_frame_outputs` are enabled.
- Output per prompt: `detections.csv` (frame, ID, score, box), an overlay image for each frame in which a new ID appears and a log with GPU memory every 100 frames.

```
code/stages/detect/run_sam3.sh runs/exp002-room001-none-sam3/frames data/room001/ground-truth.csv runs/<run>
```

## 5. Results

### 5.1 Runs

| Run | Content | Outcome |
|---|---|---|
| exp002 | Prompt "monitor", single process | Completed |
| exp003 | All prompts in one process | GPU out of memory during the third prompt |
| exp004 | All prompts in one process, new session per prompt | GPU out of memory during the third prompt |
| exp005 | One process per prompt | 9 of 11 prompts completed. "door" and "cardboard box" failed with GPU out of memory. |

### 5.2 Prompt "monitor" (exp002, checked visually)

| Measure | Value |
|---|---|
| Ground truth | 2 |
| Distinct IDs | 4 |
| False positives | 1 (picture frame) |
| Duplicates | 1 (monitor 1 received a new ID) |

- An ID that returned after a gap of 2 min was attached to a wrong object. A returning ID cannot be trusted without a check.
- Two runs with the same input gave identical IDs. The stage is deterministic.
- Conclusion for this video: SAM 3 alone does not give correct counts.

### 5.3 Other prompts (exp005, not yet checked visually)

| Prompt | Ground truth | Distinct IDs | Count error | Peak GPU memory (GB) |
|---|---|---|---|---|
| monitor | 2 | 4 | +2 | 21.1 |
| radiator | 1 | 2 | +1 | 18.6 |
| door | 1 | Failed (out of memory at frame 1199) | | |
| power socket | 6 | 3 | -3 | 17.9 |
| light switch | 1 | 5 | +4 | 21.6 |
| office chair | 1 | 3 | +2 | 18.8 |
| wardrobe | 1 | 1 | 0 | 17.8 |
| bed | 1 | 1 | 0 | 17.9 |
| sofa | 1 | 2 | +1 | 18.5 |
| cardboard box | 11 | Failed (out of memory at frame 737) | | |
| potted plant | 3 | 3 | 0 | 20.6 |

- 3 of 9 completed prompts give the correct count. 5 prompts over-count and 1 prompt under-counts.
- A correct count does not prove correct detection: a false positive and a missed object cancel out. The overlays must be checked before the counts are used as results.
- The prompts that failed track many objects or large objects. Memory growth per frame depends on the number of tracked objects.

### 5.4 GPU memory

SAM 3 keeps tracking information of every past frame on the GPU. Memory starts at about 16 GB and grows with the number of frames and tracked objects:

| Prompt | Growth |
|---|---|
| monitor | about 0.3 GB per 100 frames |
| door | about 1 GB per 100 frames |

The 24 GB GPU therefore limits the video length per room. This is relevant for criterion C5 and for long walkthroughs. The internal option `offload_output_to_cpu_for_eval` was tested and fails in SAM 3 (`KeyError: 'maskmem_features'`).

## 6. Open issues

1. Check the exp005 overlays per prompt and classify every error as a false positive, a duplicate or a missed object.
2. Decide how to handle prompts that run out of memory (for example 5 fps input).
3. The ground-truth file has no definitions for edge cases (window panes, partly hidden boxes).
4. Decide whether to test camera poses (COLMAP) for merging duplicate IDs.
