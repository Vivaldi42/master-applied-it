# Background Research Document

## Introduction

### 1. Domain
- Building maintenance requires data on installed components and equipment, including their exact location [1, Sec. 1].
- In many existing buildings this information is incomplete, obsolete, or fragmented [1, Sec. 1].
- Most existing buildings are not maintained with BIM [1].
- Creating a model of an existing building from captured data (scan-to-BIM) is costly and mainly manual [1, Sec. 2], [2].
- Camera-based reconstruction has traditionally been cheaper but less accurate than laser scanning [3, Sec. 2.2.2].
- Recent technological advances may allow camera-based reconstruction to reach higher accuracy. This is the main research gap.

### 2. Problem
- Heijmans maintains large buildings (e.g., offices, hospitals, educational institutions, and airports) under fixed-term contracts.
- Most of these buildings are older and have no BIM.
- At contract handover the previous maintainer provides an asset list (Excel, sometimes annotated floor plans). These records are often incomplete or outdated.
- Heijmans then performs an inventory inspection: an inspector records every asset and its condition according to NEN 2767 [4]. The inspection takes days to weeks and is monotonous.
- Current mitigations (combining data sources, AR) depend on a BIM model, which most buildings lack.

### 3. Goal and research questions
- Goal: a person walks through the building with a wearable camera. The captured data is converted into a 3D model of the building. An asset list can be extracted from the model.
- Requirements from stakeholders:
    - 3D model: location accuracy of 10 to 15 cm.
    - Asset list: floor and room per asset, as complete and correct as possible.
    - Data processing on premise is preferred (esp. relevant for secret projects).
- Gap that motivates SQ1: no standard method exists to assess and compare model quality [1, Sec. 4.3.4]. Benchmark datasets are lacking [3, Sec. 3.5], [2, Sec. 4].
- **Main research question:** How can a 3D model of indoor space be developed to support building inventory inspection based on visual input?
- subquestions:
    - SQ1. Which metrics evaluate methods for generating a 3D model?
    - SQ2. What methods exist and how do they compare on these metrics in literature?
    - SQ3. How do the selected methods perform in experiments and which factors affect the results?
    - SQ4. How can assets of one type and their condition be identified in the 3D model?

## Background/Related work

### 1. Concepts and definitions
- Building maintenance: asset, inventory inspection, BIM (IFC), Level of Detail (LoD), COBie (optional: what an asset list should contain).
- Localisation: camera pose, SLAM, drift, loop closure, sensor fusion (e.g., camera and IMU).
- Geometry reconstruction: depth, scale ambiguity of a single camera, 3D representations (point cloud, mesh, Gaussian splats).
- Semantic identification: semantic segmentation, object detection, semantic mapping.
- Building information modelling: scan-to-BIM, as-built (as-is) model.
- 3D world models:
    - (a) a measured 3D model of the building (the goal of this project).
    - (b) learned or generative world models, which can be used as a means to reach (a).
    - Measured vs. generated content: generated parts may look plausible without being correct, which matters for the accuracy requirement.

### 2. Reconstruction pipeline
- Capture, camera poses and geometry, 3D representation, semantics, asset list or BIM.

### 3. Method families per pipeline stage
- Photogrammetry: structure from motion (SfM) and multi-view stereo (MVS).
- Robotics: simultaneous localisation and mapping (SLAM) and semantic mapping.
- Neural and learning-based methods: Gaussian splatting, feed-forward reconstruction models.
- Short history: from photogrammetry and laser scanning to SLAM to learning-based methods.

### 4. Robotics assumptions vs. building inspection
- Typical assumptions of robotics methods (e.g., calibrated sensors on a robot, static scenes).
- Conditions in this project: a person with a wearable camera, long corridors, glass, repetitive rooms.
- Which assumptions remain valid and which do not.

### 5. Available hardware for testing
Methods section of the final paper.
- Capture devices (specifications from datasheets: TODO):

| Device | Type | Provided by |
|---|---|---|
| Samsung Galaxy S25 | Smartphone | personal device |
| Ray-Ban Meta glasses Gen 2 (Wayfarer) | Smart glasses | Heijmans |
| Insta360 X6 | 360° camera | Heijmans |
| DJI Osmo Pocket 3 | Handheld gimbal camera | ISSD |
| GoPro Fusion | 360° camera | ISSD |
| Ricoh Theta S | 360° camera | ISSD |

- Computing hardware:

| Component | Specification |
|---|---|
| Operating system | Ubuntu 24.04.4 LTS |
| CPU | AMD Ryzen 9 7950X, 16 cores, 32 threads |
| RAM | Approximately 128 GB |
| GPUs | Two NVIDIA RTX 4090, approximately 24 GB VRAM each |
| Free storage | Approximately 42 GB on the project filesystem when checked |

- Note: GPU memory does not combine across cards, so experiments should fit on one GPU.

### 6. Research gap
- Image-based reconstruction using recent advancements in technology has not been evaluated against the requirements of inventory inspection.
- No standard method exists to assess and compare model quality [1, Sec. 4.3.4]. Benchmark datasets are lacking [3, Sec. 3.5].

## Relevant results from other papers
- Reported accuracy and completeness of each method family on indoor scenes, compared with the 10 to 15 cm requirement (input for SQ2).
- Factors known to cause failures (e.g., glass, low-texture surfaces, occlusion) (input for SQ3 test conditions).
- (optional) Results of object detection in 3D models (input for SQ4).

## Inspiring methodologies from other papers
- Evaluation metrics and protocols used for 3D reconstruction (input for SQ1). Criteria: geometric accuracy, reconstruction completeness, robustness, computational performance, and suitability for downstream asset modelling.
- Ground truth: how reference data is obtained (e.g., a laser scan as reference).
- Benchmark datasets for indoor reconstruction.

# Research process
This research uses the following ICT research methods from the DOT framework [5]:

| Method | DOT strategy | Activity |
|---|---|---------|
| Expert interview | Library | Heijmans stakeholders were interviewed about the maintenance process and its problems. An interview was conducted also with a maintenance expert. Fontys ICT Game Design and Video Production experts were interviewed about 3D reconstruction of physical spaces used for gaming and video production. |
| Problem analysis | Field | The interview results were documented in a problem analysis, which was discussed with and approved by the stakeholders. |
| Literature study | Library | Review papers on BIM for existing buildings, scan-to-BIM, and condition assessment were studied to describe the domain and the research gap. |
| Available product analysis | Library | Existing reconstruction software and commercial capture products were reviewed for their output, licence, and hardware requirements. |
| Benchmark test | Showroom | [TODO] Selected methods are compared on the same captured data using the metrics from SQ1. |
| Decomposition | Workshop | [TODO] The reconstruction process was decomposed into pipeline stages (capture, localisation, geometry, semantics, BIM) to compare methods per stage. |
| Prototyping | Workshop | [TODO] A prototype was built to investigate what different algorithms can do using Samsung Galaxy S25 video. |
| Requirements prioritization | Workshop | [TODO] |

## Conclusion
- What is known: summary of the method families and their reported performance.
- What is missing: the research gap.
- how each SQ addresses the gap.

## References
[1] R. Volk, J. Stengel, and F. Schultmann, "Building information modeling (BIM) for existing buildings: Literature review and future needs," *Automation in Construction*, vol. 38, pp. 109-127, 2014, doi: 10.1016/j.autcon.2013.10.023.

[2] N. Montás-Laracuente *et al.*, "A systematic review of artificial intelligence for capturing real-world structures into building information modelling," *Journal of Building Engineering*, vol. 113, Art. no. 114093, 2025, doi: 10.1016/j.jobe.2025.114093.

[3] N. Abreu, A. Pinto, A. Matos, and M. Pires, "Procedural point cloud modelling in scan-to-BIM and scan-vs-BIM applications: A review," *ISPRS International Journal of Geo-Information*, vol. 12, no. 7, Art. no. 260, 2023, doi: 10.3390/ijgi12070260.

[4] *Conditiemeting gebouwde omgeving - Deel 1: Methodiek*, NEN 2767-1+C1:2019, NEN, Delft, The Netherlands, 2019.

[5] HBO-i, "ICT research methods: Methods pack for research in ICT," 2018. [Online]. Available: https://ictresearchmethods.nl/
