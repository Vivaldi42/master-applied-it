# Activity log

## 02-11-2026

- Reviewed the teacher feedback. Main point: start from the maintenance problem and requirements, not from the available technology.
- Research questions need revision: the main question is broader than the scope and subquestions 1 and 3 overlap. Condition assessment (NEN 2767) moves to future work.
- Direction: a generic core (capture, 3D reconstruction, object recognition and location) evaluated with Heijmans as the primary case.
- Requirements so far: fast model creation (needs a measurable time limit), maximum deviation of 10-15 cm (define what is measured: room geometry or object position) and on-premise processing as a constraint. "Evaluate devices and algorithms" belongs in the methodology, not in the requirements.
- Test object: any home or office object. Record object size and appearance as variables that affect the results.
- Data modality (RGB, RGB + IMU or RGB + depth) determines the applicable methods and benchmarks. Candidate benchmarks: ScanNet++ and ARKitScenes. Metrics: accuracy, completeness, Chamfer distance, F-score and ATE.

## 11-11-2026

- Decision: main research question unchanged. SQ4 (asset identification) is no longer marked "possibly later". Research questions remain a work in progress.
- Requirement for the 3D model: it must allow asset recognition later.
- Next step: define the pipeline stages and the decision criteria for the method longlist.
- Papers renamed to `author-year-short-description.pdf`. The filename equals the key in `papers/index.md`. All 9 papers are listed in the index.

## 19-11-2026

- The 3D reconstruction of my room using COLMAP PatchMatch stereo (the dense depth maps generation) took more than 2 h. Thus, I decided to focus on asset counts per room and per floor using SAM3 directly on video without doing experiments with COLMAP (or 3D reconstruction and modelling) for now. 
- The first experiment tests whether SAM 3 alone (without a 3D model) can count the assets in the `room001` video.
- First SAM 3 experiment: SAM 3 alone does not give correct counts on `room001`. It finds most assets but mostly over-counts them (duplicate IDs and false positives). GPU memory limits the video length.
- Next step: classify the counting errors per prompt.
- Details: `code/stages/detect/sam3.md`.

## 23-11-2026

- Wrote `architecture/system-architecture.md`. It describes the current pipeline, the decisions, the gaps between design and code and the open architecture decisions.
- Decision: raw videos stay outside git on the SSD with a copy on the external disk. A per-room manifest is committed to git.
- Decision: the MVP takes a room video and a given list of asset types as input and gives a CSV with `asset,count` as output. Heijmans needs only the asset types in its asset table.
- Added the count stage (`code/stages/count/count.py`). It counts distinct track IDs per asset type and leaves the count empty if detection failed.

## 24-11-2026

- Added the evaluation stage (`code/stages/evaluate/evaluate.py`). It gives the signed count error per asset type. Both new stages reproduce the exp005 counts in `sam3.md`.
- Added `code/run_mvp.sh`, which runs frames, detection, count and evaluation with one command.
- Reduced `data/room001/ground-truth.csv` to monitor, radiator and door.
- exp006 (first full MVP run): all 3 prompts failed with GPU out of memory. Services of another user hold about 8.2 GB on GPU 0 and SAM 3 needs 18 to 22 GB on the full video. Offloading to CPU memory is already enabled and does not solve it.
- The exp004 log shows that GPU memory is released between prompts. The original reason for one process per prompt is therefore not supported.
- Next step: decide how to get enough GPU memory (free GPU, smaller input or split video).

## 25-11-2026

- Correction to 24-11: offloading was not effective. SAM 3 copied all frames to the GPU (10.5 GB). Fixed in `sam3_detect.py`. In exp007 the peak for "monitor" fell from 21.1 to 10.6 GB with identical detections.
- `run_sam3.sh` runs one prompt per GPU in parallel.
- Shortened `system-architecture.md`. The details moved to `architecture-details.md`.
- First working prototype: video and asset list in, final list out, with one manual check. "door" on room002 (exp011): SAM 3 found 9 objects. The check gave 2 correct, 2 duplicate and 5 wrong, so the final count is 2 (hand count 2).
- Detection test on 43 single images (exp012, "door"): all 8 certain doors found, 15 wrong boxes at a score limit of 0.5 (verdicts by Claude, not checked).
- Limitation: the check cannot add objects that SAM 3 missed, for example the expansion tank in exp010.
- Next step: run all room002 assets and measure the time needed for the check.
