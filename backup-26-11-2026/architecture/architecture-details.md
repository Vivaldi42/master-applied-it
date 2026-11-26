# System architecture: details

Background to `system-architecture.md`: data contracts, full decision log, gaps and experiment history. Read it only when needed.

Status: 25-11-2026 (commit `f00b60d` plus uncommitted changes).

## 1. Purpose of this document

1. This document describes the architecture and data flow of the asset reconstruction pipeline. It is the shared reference between the architect (Vladislav) and the development assistant (Claude).
2. The architect makes the architecture decisions (Section 8). The assistant implements them and reports gaps between this document and the code (Section 9).
3. A change to a stage interface, the run folder layout or an environment is recorded here before or together with the code change.
4. Stage details (settings, results, open issues of one method) are in the stage documents, for example `code/stages/detect/sam3.md`. This document does not repeat them.

Status labels used in this document:

| Label | Meaning |
|---|---|
| Implemented | Code exists in `code/` and was used in at least one run. |
| Manual | The step was done by hand or with a command that is not stored as a script. |
| Planned | The step is designed but has no code. |
| Paused | The step has code but is not used in the current experiments. |

## 2. Context

1. Goal: convert a video walkthrough of a room into a list of assets per room (requirement R1) and, later, asset positions (R2). Requirements R1 to R5 and criteria C1 to C7 are defined in `research-mind-map/background-research-document.md`.
2. Current stakeholder need (19-11-2026): asset counts per room and per floor. Positions are not required for now.
3. Current target (23-11-2026): a simple end-to-end MVP (D9). Robustness and count accuracy are improved after the MVP runs end to end.
4. Current research question of the experiments: can SAM 3 alone, without a 3D model, count the assets in a room video? Result so far: no. Most prompts over-count (see `sam3.md`, Section 5).
5. Constraint R3: all processing runs on local hardware.
6. The background research document still assumes a 3D model. It is not updated to the 2D path yet.

## 3. Architecture principles

These principles are decided. They are stated in `code/README.md`.

1. **Stage isolation.** Each stage runs as a separate process in its own environment (system, Docker or conda). Methods with conflicting dependencies can therefore be exchanged per stage.
2. **File-based interfaces.** Stages exchange data only through files in the run folder. No stage calls another stage in memory.
3. **Immutable runs.** A run never overwrites an earlier run. Each run has its own folder in `runs/`.
4. **Run identity.** A run is identified by its counter `exp<NNN>`. The rest of the name describes the input and methods. Failed runs keep their number.

## 4. Pipeline overview

```
        data/<room>/video.mp4          asset list (CSV)
                 |                           |
          [1. Frames] FFmpeg                 |
                 |                           |
            frames/*.jpg                     |
                 +-------------+             |
                 |             |             |
   ACTIVE PATH   |             |   PAUSED PATH (3D)
   (run_mvp.sh)  v             v             |
        [4. Detect] SAM 3 <----|-------------+
                 |             |             |
   detect/<asset>/detections.csv             |
                 |      [2. Reconstruct] COLMAP
                 |             |             |
        [Count] distinct IDs  [3. Scale] (Planned)
                 |             |             |
            counts.csv  <------|-------------+
                 |      [5. Localise] (Planned)
                 v
        [6. Evaluate] <-- data/<room>/ground-truth.csv
                 |
          evaluation.csv
```

1. Active path: `code/run_mvp.sh` runs Frames, Detect, Count and Evaluate with one command (first used in exp006).
2. Paused path (run `exp001`): Reconstruct was run once. Scale and Localise have no code. The path was paused on 19-11-2026 because PatchMatch stereo took more than 2 h.

## 5. Stage specifications

| Stage | Status | Input | Output | Implementation | Environment |
|---|---|---|---|---|---|
| 1. Frames | Implemented | `video.mp4` | `frames/NNNNN.jpg` (10 fps, 1920 px wide) | FFmpeg command in `code/run_mvp.sh` | System |
| 2. Reconstruct | Paused | `frames/` | `database.db`, `sparse/`, `dense/fused.ply`, logs | `code/stages/reconstruct/colmap.sh` | Docker `colmap/colmap` |
| 3. Scale | Planned | Model, one measured distance | Model in metres | None | Not decided |
| 4. Detect | Implemented | `frames/`, asset list | `detect/<asset>/detections.csv`, `detect/<asset>/overlays/`, `detect/<asset>.log` | `code/stages/detect/run_sam3.sh` calls `sam3_detect.py` once per asset | Conda `sam3` |
| Count | Implemented | `detect/`, asset list | `counts.csv` | `code/stages/count/count.py` | Python standard library |
| 5. Localise | Planned | Model, masks | `assets.csv` | None | Not decided |
| 6. Evaluate | Implemented | `counts.csv`, `ground-truth.csv` | `evaluation.csv` | `code/stages/evaluate/evaluate.py` | Python standard library |

### 5.1 Data contracts

| File | Producer | Format |
|---|---|---|
| `frames/NNNNN.jpg` | Frames | JPEG, five-digit index starting at 0. Required by `sam3_detect.py`. |
| `frames/frame_NNNNNN.jpg` | Frames (exp001 only) | JPEG, six-digit index starting at 1. Used by COLMAP. |
| Asset list | Architect | CSV with a header row. The first column holds the asset types. Each asset type is also the SAM 3 text prompt. For room001: `data/room001/asset-list.csv`. |
| `ground-truth.csv` | Architect (hand count) | Columns `prompt,count`. One row per asset type. It was reduced to 3 rows on 24-11-2026 (exp006) and contains 11 rows again on 25-11-2026. |
| `detections.csv` | Detect | Columns `prompt,frame,obj_id,prob,x,y,w,h`. One row per object per frame. Box in coordinates relative to image size. |
| `overlays/NNNNN.jpg` | Detect | Frame with masks and IDs, saved only when a new ID appears. For visual checks. |
| `<asset>.log` | Detect | GPU memory every 100 frames and, only after a completed run, a final line `=== <asset>: <N> distinct IDs, peak GPU memory <X> GB`. |
| `counts.csv` | Count | Columns `asset,count`. The count is the number of distinct `obj_id` values (D7). The count is empty if the final log line is missing, that is, if detection failed. |
| `evaluation.csv` | Evaluate | Columns `asset,truth,predicted,error`. `error = predicted - truth` with sign. Empty if the count is empty. Assets are matched by name. |

## 6. Data and storage

| Location | Content | In git | Size (23-11-2026) |
|---|---|---|---|
| `code/` | Stage scripts and stage documents | Yes | Small |
| `data/<room>/video.mp4` | Raw capture | No | 716 MB (room001) |
| `data/<room>/ground-truth.csv` | Hand count | Yes | Small |
| `runs/<run-id>/` | All outputs of one run | No | exp001: 23 GB, exp002 to exp005: 0.4 GB |
| `external/` | Downloaded method code (`sam3`) | No | Not measured |

1. Raw data storage (decided 23-11-2026): videos stay outside git on the SSD with a copy on the external disk. A per-room manifest (file, SHA-256, size, capture date, device) is committed to git. The manifest does not exist yet.
2. The data model has no floor attribute. A per-floor count requires a mapping from room to floor.

## 7. Runtime environment

| Item | Value |
|---|---|
| GPU | 2 x NVIDIA RTX 4090, 24 GB each. Both GPUs are shared with services of another user. On 24-11-2026 these services held about 8.2 GB on GPU 0 and about 3.7 GB on GPU 1. `run_sam3.sh` runs one prompt per GPU (default: both). |
| SAM 3 | `external/sam3` commit `31cb7e6`, conda env `sam3`, Python 3.12, PyTorch 2.10.0 cu128, `setuptools<81` |
| COLMAP | 4.3.0.dev0 with CUDA, Docker image digest recorded in `colmap.md` Sec. 2 |
| FFmpeg | System installation, version not recorded |

### 7.1 SAM 3 GPU memory

1. Cause of the high memory use: SAM 3 copies all frames to the GPU even with `offload_video_to_cpu`. For 1725 frames this takes 10.5 GB.
2. Fix (25-11-2026): `sam3_detect.py` keeps the frames in CPU memory and moves one frame at a time to the GPU. `external/sam3` is not modified.
3. Check (exp007, "monitor"): `detections.csv` is identical to exp005. Peak GPU memory fell from 21.1 GB to 10.6 GB.
4. Memory still grows with the number of frames and tracked objects.

## 8. Decision log

| ID | Date | Decision | Reason | Source |
|---|---|---|---|---|
| D1 | 18-11-2026 or earlier | Stages run as separate processes and exchange files only. | Methods have conflicting dependencies. | `code/README.md` |
| D2 | 18-11-2026 or earlier | Runs are immutable and numbered `exp<NNN>`. | Repeatability and traceability of results. | `code/README.md` |
| D3 | 19-11-2026 | COLMAP runs in Docker. | Keeps its dependencies separate. | `colmap.md` Sec. 1 |
| D4 | 19-11-2026 | Pause the 3D path. Test SAM 3 alone for counting. | PatchMatch stereo took more than 2 h. Stakeholder needs counts, not positions. | `activity-log.md` |
| D5 | 19-11-2026 | Frames for detection at 10 fps, 1920 px wide. | Smaller motion between frames helps the tracker. SAM 3 resizes internally. | `sam3.md` Sec. 3 |
| D6 | 19-11-2026 | One process per prompt. | Original reason: GPU memory is not released between prompts in one process. The exp004 log does not support this reason (Section 11). The decision is kept but its reason is not re-evaluated. | `sam3.md` Sec. 4 |
| D7 | 19-11-2026 | Count rule: number of distinct track IDs per prompt over the whole video. | Simplest rule. Known to over-count. | `sam3.md` Sec. 4 |
| D8 | 23-11-2026 | Raw data outside git with a manifest in git. | GitHub rejects large files. | `activity-log.md` |
| D9 | 23-11-2026 | MVP: input is a room video and a given list of asset types. Output is a CSV with columns `asset,count`. | Heijmans needs only the asset types in its asset table. SAM 3 needs a text prompt per type. | Architect decision |
| D10 | 23-11-2026 | Count is a separate stage that reads `detections.csv`. | The count rule can change without running SAM 3 again. | Architect decision |
| D11 | 24-11-2026 | Evaluation measure: signed count error per asset type. | The sign separates over-counting (duplicates, false positives) from under-counting (missed objects). Per-asset results show which asset types can be trusted. An error of 0 can still hide a false positive and a missed object that cancel out. | Architect decision |
| D12 | 24-11-2026 | One command runs the whole active path (`code/run_mvp.sh`). Each run extracts its own frames. | End-to-end MVP. Runs become self-contained. | Architect decision |

## 9. Gaps between design and implementation

These are facts found in the code and run folders. Each gap affects robustness or repeatability. Fixed gaps are listed at the end of this section.

1. **Two frame naming conventions exist.** exp001 uses `frame_%06d.jpg` from 1, `run_mvp.sh` uses `%05d.jpg` from 0. `sam3_detect.py` hard-codes `%05d.jpg`. COLMAP is not part of `run_mvp.sh`, so the conflict appears only if the 3D path is resumed.
2. **No run record.** `code/README.md` states that each run folder stores its settings. No run folder contains a settings file. The command, commit, input checksum and environment of a run are not stored. Example: the change of `ground-truth.csv` between exp003 and exp005 is not traceable.
3. **Detect output differs from the design.** `code/README.md` specifies `masks/` (PNG per frame) as output. The code writes boxes to `detections.csv` and masks only into overlay images. Stage 5 (Localise) needs masks, so the detection would have to run again.
4. **Overwrite protection is incomplete.** `run_mvp.sh` refuses an existing run folder. A direct call of `run_sam3.sh` on an existing folder still truncates `<asset>.log` with `>` before Python starts. `colmap.sh` checks only `database.db`.
5. **COLMAP image is not pinned.** `colmap.sh` uses `colmap/colmap:latest` and records the digest after the fact. A later `docker pull` changes the method without a change in the script.
6. **`colmap.sh` assumes `sparse/0` is the main model.** COLMAP does not guarantee this order (`colmap.md` Sec. 7).
7. **SAM 3 environment is not reproducible from git.** No environment file (`environment.yml` or `requirements.txt`) is committed.
8. **CSV parsing in `run_sam3.sh` uses `cut -d,`.** An asset type that contains a comma or quotes is split incorrectly.
9. **Exploration code is mixed with stage code.** `sam3_smoke.py` writes outside the run contract (`exist_ok=True`, folder next to `frames/`).
10. **No GPU memory check.** The pipeline does not check free GPU memory before it starts.
11. **Asset list and ground truth are one file.** `run_mvp.sh` takes them as two arguments, but both were `ground-truth.csv` until exp007. exp008 uses `data/room001/asset-list.csv`, which git ignores. An asset name that differs between the two files gives an empty result in `evaluation.csv`.

Fixed:

- Frames stage had no script. Fixed by `run_mvp.sh` (D12).
- Runs were not self-contained (exp005 read frames from exp002). Fixed for runs started with `run_mvp.sh` (D12).
- Count and Evaluate were not stages. Fixed by `count.py` and `evaluate.py` (D10, D11).

## 10. Open architecture decisions

These questions are open. The architect decides them.

1. Closed on 25-11-2026: GPU memory (Section 7.1).
2. Does the next experiment stay on the 2D path, or does it use camera poses (paused 3D path) to merge duplicate IDs? This depends on the error classification of exp005 (`sam3.md`, open issue 1).
3. What does a run record contain (command, git commit, input checksums, environment, start and end time, peak GPU memory) and in which format?
4. Should the asset type be separated from the model prompt, so that one asset type can use several prompts or another detector?
5. Where are room-to-floor mapping and capture metadata stored?
6. Is D6 (one process per prompt) kept? A possible new reason: a failed prompt cannot stop the other prompts.

## 11. Experiment history

Runs exp001 to exp008 use the `room001` video, exp009 and exp010 use `room002`. Details and result tables are in `colmap.md` and `sam3.md`.

| Run | What was done and the result | Change for the next run |
|---|---|---|
| exp001 | COLMAP sparse and dense reconstruction on 345 frames (2 fps, full resolution). It took 168 min, of which PatchMatch stereo took 155 min. The dense model has holes and is upside down. SAM 3 was not run despite the run name. | The 3D path was paused (D4). The next run tests SAM 3 alone on new frames (10 fps, 1920 px). |
| exp002 | SAM 3 with the single prompt "monitor" in one process. It found 4 IDs for 2 monitors (1 false positive, 1 duplicate). A second run gave identical IDs. The folder also contains the smoke test output. | All 11 prompts of `ground-truth.csv` in one process. |
| exp003 | All prompts in one process with one SAM 3 session. "monitor" and "radiator" completed. The GPU ran out of memory during the third prompt, "window". "window" is not in the current `ground-truth.csv`. | A new SAM 3 session per prompt within the same process. |
| exp004 | All prompts in one process with a new session per prompt. "monitor" and "radiator" completed. After each of them, reserved GPU memory returned to 5.16 GB. The GPU ran out of memory during the third prompt, "door". | One process per prompt (`run_sam3.sh`, D6). |
| exp005 | One process per prompt. 9 of 11 prompts completed. "door" and "cardboard box" ran out of memory. 3 of 9 counts are correct and most others over-count. On 24-11-2026, `count.py` and `evaluate.py` were run on this output and reproduce the counts in `sam3.md`. | First run of `run_mvp.sh`. `ground-truth.csv` reduced to monitor, radiator and door. |
| exp006 | Full pipeline with `run_mvp.sh` (3 assets). All 3 prompts ran out of memory before the first logged frame, with SAM 3 at 15.2 GB. Another user's services held about 8.2 GB on GPU 0. `counts.csv` and `evaluation.csv` contain empty values, as designed for failed detections. | Frames stay in CPU memory (Section 7.1). |
| exp007 | "monitor" on GPU 1 with the memory fix. Detections identical to exp005 (4 IDs), peak 10.6 GB. | 9 assets in parallel on both GPUs, without "door" and "cardboard box". |
| exp008 | 9 assets in parallel in 19 min. Detections identical to exp005. 3 of 9 counts are correct. | New video: room002. |
| exp009 | room002. Stopped by the architect during the first two prompts. No results. | Input files corrected. |
| exp010 | room002, 10 assets in 9 min. "door" and "window" crashed on an empty mask. 8 completed. | Empty masks are skipped in the overlay. Power sockets in the hand count corrected from 2 to 3. |
