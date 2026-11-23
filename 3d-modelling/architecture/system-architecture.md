# System Architecture

Status: as implemented on 23-11-2026 (commit `f00b60d`).

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
3. Current research question of the experiments: can SAM 3 alone, without a 3D model, count the assets in a room video? Result so far: no. Most prompts over-count (see `sam3.md`, Section 5).
4. Constraint R3: all processing runs on local hardware.

## 3. Architecture principles

These principles are decided. They are stated in `code/README.md`.

1. **Stage isolation.** Each stage runs as a separate process in its own environment (system, Docker or conda). Methods with conflicting dependencies can therefore be exchanged per stage.
2. **File-based interfaces.** Stages exchange data only through files in the run folder. No stage calls another stage in memory.
3. **Immutable runs.** A run never overwrites an earlier run. Each run has its own folder in `runs/`.
4. **Run identity.** A run is identified by its counter `exp<NNN>`. The rest of the name describes the input and methods. Failed runs keep their number.

## 4. Pipeline overview

```
                     data/<room>/video.mp4
                              |
                       [1. Frames] (Manual, FFmpeg)
                              |
                         frames/*.jpg
                 +------------+-------------+
                 |                          |
   ACTIVE PATH   |                          |   PAUSED PATH (3D)
                 v                          v
        [4. Detect] SAM 3           [2. Reconstruct] COLMAP
                 |                          |
   detections.csv, overlays/       sparse/, dense/fused.ply
                 |                          |
        count = distinct IDs        [3. Scale] (Planned)
        (printed in log)                    |
                 |                  [5. Localise] (Planned)
                 |                   uses masks + model
                 v                          |
        [6. Evaluate] (Manual) <------------+
        compare with data/<room>/ground-truth.csv
                 |
        result tables in sam3.md
```

1. Active path (runs `exp002` to `exp005`): Frames, Detect, manual count comparison.
2. Paused path (run `exp001`): Reconstruct was run once. Scale and Localise have no code. The path was paused on 19-11-2026 because PatchMatch stereo took more than 2 h.

## 5. Stage specifications

| Stage | Status | Input | Output | Implementation | Environment |
|---|---|---|---|---|---|
| 1. Frames | Manual | `video.mp4` | `frames/*.jpg` | FFmpeg command in `sam3.md` Sec. 3 and `colmap.md` Sec. 4.1 | System |
| 2. Reconstruct | Paused | `frames/` | `database.db`, `sparse/`, `dense/fused.ply`, logs | `code/stages/reconstruct/colmap.sh` | Docker `colmap/colmap` |
| 3. Scale | Planned | Model, one measured distance | Model in metres | None | Not decided |
| 4. Detect | Implemented | `frames/`, `ground-truth.csv` (prompt list) | Per prompt: `<prompt>/detections.csv`, `<prompt>/overlays/`, `<prompt>.log` | `code/stages/detect/run_sam3.sh` calls `sam3_detect.py` once per prompt | Conda `sam3` |
| 5. Localise | Planned | Model, masks | `assets.csv` | None | Not decided |
| 6. Evaluate | Manual | Counts, `ground-truth.csv` | Tables in `sam3.md` | None | Not decided |

### 5.1 Data contracts

| File | Producer | Format |
|---|---|---|
| `frames/NNNNN.jpg` | Frames | JPEG, five-digit index starting at 0. Required by `sam3_detect.py`. |
| `frames/frame_NNNNNN.jpg` | Frames (exp001 only) | JPEG, six-digit index starting at 1. Used by COLMAP. |
| `ground-truth.csv` | Architect (hand count) | Columns `prompt,count`. One row per asset type. The `prompt` value is both the asset type and the SAM 3 text prompt. |
| `detections.csv` | Detect | Columns `prompt,frame,obj_id,prob,x,y,w,h`. One row per object per frame. Box in coordinates relative to image size. |
| `overlays/NNNNN.jpg` | Detect | Frame with masks and IDs, saved only when a new ID appears. For visual checks. |
| `<prompt>.log` | Detect | GPU memory every 100 frames and a final line `=== <prompt>: <N> distinct IDs, peak GPU memory <X> GB`. |

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
| GPU | NVIDIA RTX 4090, 24 GB, GPU 0. GPU 1 is shared with other users. |
| SAM 3 | `external/sam3` commit `31cb7e6`, conda env `sam3`, Python 3.12, PyTorch 2.10.0 cu128, `setuptools<81` |
| COLMAP | 4.3.0.dev0 with CUDA, Docker image digest recorded in `colmap.md` Sec. 2 |
| FFmpeg | System installation, version not recorded |

## 8. Decision log

| ID | Date | Decision | Reason | Source |
|---|---|---|---|---|
| D1 | 18-11-2026 or earlier | Stages run as separate processes and exchange files only. | Methods have conflicting dependencies. | `code/README.md` |
| D2 | 18-11-2026 or earlier | Runs are immutable and numbered `exp<NNN>`. | Repeatability and traceability of results. | `code/README.md` |
| D3 | 19-11-2026 | COLMAP runs in Docker. | Keeps its dependencies separate. | `colmap.md` Sec. 1 |
| D4 | 19-11-2026 | Pause the 3D path. Test SAM 3 alone for counting. | PatchMatch stereo took more than 2 h. Stakeholder needs counts, not positions. | `activity-log.md` |
| D5 | 19-11-2026 | Frames for detection at 10 fps, 1920 px wide. | Smaller motion between frames helps the tracker. SAM 3 resizes internally. | `sam3.md` Sec. 3 |
| D6 | 19-11-2026 | One process per prompt. | GPU memory is not released between prompts in one process (exp003, exp004). | `sam3.md` Sec. 4 |
| D7 | 19-11-2026 | Count rule: number of distinct track IDs per prompt over the whole video. | Simplest rule. Known to over-count. | `sam3.md` Sec. 4 |
| D8 | 23-11-2026 | Raw data outside git with a manifest in git. | GitHub rejects large files. | Memory note, not yet in a project document |

## 9. Gaps between design and implementation

These are facts found in the code and run folders on 23-11-2026. Each gap affects robustness or repeatability. None is fixed yet.

1. **Frames stage has no script.** Two different FFmpeg commands were used (exp001: 2 fps, full resolution, `frame_%06d.jpg` from 1; exp002: 10 fps, 1920 px, `%05d.jpg` from 0). `sam3_detect.py` hard-codes `%05d.jpg`, so it cannot read exp001 frames. The frame naming is an undocumented contract between stages.
2. **Runs are not self-contained.** exp005 reads its frames from `runs/exp002-.../frames/`. Deleting or changing exp002 breaks the inputs of exp005.
3. **No run record.** `code/README.md` states that each run folder stores its settings. No run folder contains a settings file. The command, commit, input checksum and environment of a run are known only from the stage documents.
4. **Detect output differs from the design.** `code/README.md` specifies `masks/` (PNG per frame) as output. The code writes boxes to `detections.csv` and masks only into overlay images. Stage 5 (Localise) needs masks, so the detection would have to run again.
5. **Count and Evaluate are not stages.** The count exists only as a printed log line. The comparison with the ground truth was done by hand. Result tables cannot be regenerated from the run folder.
6. **Overwrite protection is incomplete.** `sam3_detect.py` refuses an existing prompt folder, but `run_sam3.sh` truncates `<prompt>.log` with `>` before Python starts. A repeated call on the same run folder therefore destroys the earlier log. `colmap.sh` checks only `database.db`.
7. **COLMAP image is not pinned.** `colmap.sh` uses `colmap/colmap:latest` and records the digest after the fact. A later `docker pull` changes the method without a change in the script.
8. **`colmap.sh` assumes `sparse/0` is the main model.** COLMAP does not guarantee this order (`colmap.md` Sec. 7).
9. **SAM 3 environment is not reproducible from git.** No environment file (`environment.yml` or `requirements.txt`) is committed.
10. **CSV parsing in `run_sam3.sh` uses `cut -d,`.** A prompt that contains a comma or quotes is split incorrectly.
11. **Exploration code is mixed with stage code.** `sam3_smoke.py` writes outside the run contract (`exist_ok=True`, folder next to `frames/`).

## 10. Open architecture decisions

These questions are open. The architect decides them.

1. Does the next experiment stay on the 2D path, or does it use camera poses (paused 3D path) to merge duplicate IDs? This depends on the error classification of exp005 (`sam3.md`, open issue 1).
2. Should counting be a separate stage that reads `detections.csv` and writes a count file, so that the count rule (D7) can change without running SAM 3 again?
3. What does a run record contain (command, git commit, input checksums, environment, start and end time, peak GPU memory) and in which format?
4. Are frames a per-run output or a shared, versioned product of the video (for example `data/<room>/frames-10fps/`)? This affects gap 2 and the disk usage.
5. Should the asset type be separated from the model prompt in `ground-truth.csv`, so that one asset type can use several prompts or another detector?
6. Where are room-to-floor mapping and capture metadata stored?
7. Is one entry script per run required (all stages, one command), or are stages started by hand?
8. How does the pipeline handle a prompt that runs out of GPU memory: fail, retry at a lower frame rate, or split the video?
