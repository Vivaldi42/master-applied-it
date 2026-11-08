# Background research contents

## Introduction

### Story
1. Domain: maintenance needs reliable asset data, but in existing buildings this data is poor and BIM is mostly absent. Creating models of existing buildings is manual and costly. Cameras are a cheap alternative to laser scanners but have traditionally been less accurate. Due to the technological advances in the last years theoretically higher accuracy could be achived (the main research gap).
2. Problem: Heijmans receives incomplete asset lists at contract handover and must inspect buildings manually, which takes days to weeks.
3. Goal and RQs: a wearable camera walkthrough produces a 3D model and an asset list. The RQs ask how to evaluate, select and test methods for this purpose.

### 1. Domain
- Building maintenance requires data on installed components and equipment, including their exact location [1, Sec. 1].
    - Quote: "detailed data on installed components and equipment is needed such as [...] geometries and exact location [...] as well as maintenance history since completion"
- In many existing buildings this information is incomplete or outdated [1, Sec. 1].
    - Quote: "In many existing buildings, incomplete, obsolete or fragmented building information is predominating"
- Most existing buildings are not maintained with BIM [1].
    - Quote: "the majority of existing buildings is not maintained, refurbished or deconstructed with BIM yet"
- Creating a model of an existing building from captured data (scan-to-BIM) is costly and mainly manual [1, Sec. 2], [2].
    - Quote [1]: "costly and mainly manual reverse engineering processes ('points-to-BIM', 'scan-to-BIM')"
    - Quote [2]: "traditional Scan-to-Building Information Modelling (Sc2BIM) workflows remain time-consuming and require many resources"
- Camera-based reconstruction has traditionally been cheaper but less accurate than laser scanning [3, Sec. 2.2.2]. Whether this still holds for recent methods is investigated in SQ2 and SQ3.
    - Quote: "Cameras are cheap, easy to use, and offer fast data acquisition. On the other hand, one of its main issues is the reduced accuracy of photogrammetry when compared to laser scanners."

### 2. Problem (source: problem-analysis.md)
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
    - Data processing on premise is preferred (secret projects).
- Gap that motivates SQ1: no standard method exists to assess and compare model quality [1, Sec. 4.3.4]. Benchmark datasets are lacking [3, Sec. 3.5], [2, Sec. 4].
- **Main research question:** How can a 3D model of indoor space be developed to support building inventory inspection based on visual input?
- subquestions:
    - Which metrics evaluate methods for generating a 3D model?
    - What methods exist and how do they compare on these metrics in literature?
    - How do the selected methods perform in experiments and which factors affect the results?
    - (possibly later) How can assets of one type and their condition be identified in the 3D model?

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
- Figure: overview of representations?

### 2. Reconstruction pipeline
- Capture, camera poses and geometry, 3D representation, semantics, asset list or BIM.
- Figure: pipeline diagram with the stages.

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
May move to the methods section of the final paper.
- Capture devices (specifications: TODO, from manufacturer data sheets):

| Device | Type | Provided by |
|---|---|---|
| Samsung Galaxy S25 | Smartphone | TODO |
| Ray-Ban Meta glasses Gen 2 (Wayfarer) | Smart glasses | Heijmans |
| DJI Osmo Pocket 3 | Handheld gimbal camera | TODO |
| GoPro Fusion | 360° camera | TODO |
| Ricoh Theta S | 360° camera | TODO |
| Insta360 X6 | 360° camera | Heijmans |

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

| Method | DOT strategy |
|---|---|
| Expert interview (Heijmans; Fontys ICT Game Design and Video Production) | Library |
| Problem analysis | Field |
| Literature study | Library |
| Available product analysis | Library |
| Benchmark test | Showroom |
| Decomposition | Workshop |
| Prototyping | Workshop |
| Requirements prioritization | Workshop |

## Conclusion
- What is known: summary of the method families and their reported performance.
- What is missing: the research gap.
- How each SQ addresses the gap.

## References
[1] R. Volk, J. Stengel, and F. Schultmann, "Building information modeling (BIM) for existing buildings: Literature review and future needs," *Automation in Construction*, vol. 38, pp. 109-127, 2014, doi: 10.1016/j.autcon.2013.10.023.

[2] N. Montás-Laracuente *et al.*, "A systematic review of artificial intelligence for capturing real-world structures into building information modelling," *Journal of Building Engineering*, vol. 113, Art. no. 114093, 2025, doi: 10.1016/j.jobe.2025.114093.

[3] N. Abreu, A. Pinto, A. Matos, and M. Pires, "Procedural point cloud modelling in scan-to-BIM and scan-vs-BIM applications: A review," *ISPRS International Journal of Geo-Information*, vol. 12, no. 7, Art. no. 260, 2023, doi: 10.3390/ijgi12070260.

[4] *Conditiemeting gebouwde omgeving - Deel 1: Methodiek*, NEN 2767-1+C1:2019, NEN, Delft, The Netherlands, 2019.

[5] HBO-i, "ICT research methods: Methods pack for research in ICT," 2018. [Online]. Available: https://ictresearchmethods.nl/
