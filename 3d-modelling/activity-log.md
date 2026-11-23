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
