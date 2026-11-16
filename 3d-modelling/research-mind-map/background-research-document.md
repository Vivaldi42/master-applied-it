# Background Research Document

[TODO] Add numbers to every section in the doc eg 1. Introduction, 1.1. Domain, 1.2 Problem,...



## Introduction

### 1. Domain
- Building maintenance requires data on installed components and equipment, including their exact location [1, Sec. 1].
- In many existing buildings the available building information is incomplete, outdated or scattered [1, Sec. 1].
- Most existing buildings are not maintained with BIM [1, Sec. 4.4.1]. The Heijmans stakeholders confirm this for the Dutch industry today (see Problem).
- Creating a model of an existing building from captured data (scan-to-BIM) is costly and mainly manual [1, Sec. 2], [2, Sec. 1].
- Camera-based reconstruction is cheaper but less accurate than laser scanning [3, Sec. 2.2.2].
- Recent learning-based methods make camera-based reconstruction more robust and easier to use [6, Sec. 3].
- Their geometric accuracy for building interiors has not been established. The closest indoor study did not measure it [7, Sec. 1, Sec. 4.2], and an outdoor study found that Gaussian splatting is not yet a mapping tool [8, Sec. 5]. This is the main research gap.

### 2. Problem
- Heijmans maintains large buildings (e.g., offices, hospitals, educational institutions, and airports) under fixed-term contracts.
- Most of these buildings are older and have no BIM.
- At contract handover the previous maintainer provides an asset list (Excel, sometimes annotated floor plans). These records are often incomplete or outdated.
- Heijmans then performs an inventory inspection: an inspector records every asset and its condition according to NEN 2767 [4]. The inspection takes days to weeks and is monotonous.
- Current mitigations (combining data sources, AR) depend on a BIM model, which most buildings lack.

### 3. Goal
- Goal: a person walks through the building with a handheld or wearable camera. The captured data is converted into a 3D model of the building. An asset list can be extracted from the model.

[TODO] Justification why a 3D model is useful in this case.

### 4. Research gap
- Image-based reconstruction using recent advancements in technology has not been evaluated against the requirements of inventory inspection.
- No standard method exists to assess and compare model quality [1, Sec. 4.3.4]. Benchmark datasets are lacking [3, Sec. 3.5], [2, Sec. 4].

### 5. Research questions
- **Main research question:** How can visual data collected during building walkthroughs be used to reliably identify and localise building assets to support inventory inspections?
- **Subquestions**:
    - SQ1. **Requirements and metrics**: What requirements must a solution meet to support building inventory inspections, and which metrics measure them?
    - SQ2. **Approaches and their limitations**: Which visual sensing, localisation and reconstruction approaches can contribute to meeting these requirements, and what are their limitations?
    - SQ3. **Developing a solution**: How can these approaches be combined into a solution that identifies assets and associates them with reliable spatial locations?
    - SQ4. **Evaluating the solution**: How effectively does the resulting solution meet the requirements under representative building conditions?

## SQ1. **Requirements and metrics**: What requirements must a solution meet to support building inventory inspections, and which metrics measure them?

### 1. Requirements
The requirements originate from interviews with the Heijmans stakeholders. The interview results are documented in a problem analysis, which the stakeholders approved (see Research process).

| # | Name | Requirement |
|---|---|-----------------|
| R1 | Asset count | For each room, the solution reports which fixed asset types (e.g. fire extinguishers, emergency exits, lights, ventilation) are present and how many of each. |
| R2 | Spatial accuracy | The 3D model represents the room and its assets at real-world scale. Positions deviate from reality by roughly 10 to 15 cm at most (indicative value). Spatial accuracy has priority over visual realism. |
| R3 | Data security | On-premise data processing is preferred. Cloud-based methods score lower. |
| R4 | Input data | The input data is collected by a person who walks through the building with a handheld or wearable camera. A short video walkthrough per room is sufficient input, without manual recording of assets. |
| R5 | Execution time | Processing is as fast as possible. |

### 2. Evaluation criteria
| # | Criterion | Requirement | Metric | Source |
|---|---|---|---------|---|
| C1 | Geometric accuracy | R2 | Precision: share of model points within a distance threshold of the reference | [9, Sec. 6] |
| C2 | Completeness | R1, R2 | Recall: share of reference points that have a model point within the distance threshold | [9, Sec. 6] |
| C3 | Robustness | R4, R5 | One connected, plausible model under difficult conditions (changing exposure, reflective and uniform surfaces) | [9, Sec. 8] |
| C4 | Asset detection quality | R1 | F1 score after one-to-one matching of detected and reference assets | [10, Sec. 3.1] |
| C5 | Processing time and hardware demand | R5 | Time from video to result and GPU memory needed | Requirement 5 |
| C6 | Runs locally | R3 | Code and model weights available to run on own hardware: yes or no | Requirement 3 |
| C7 | Input type | R4 | Works with video from one handheld or wearable camera | Requirement 4 |

## SQ2. **Approaches and their limitations**: Which visual sensing, localisation and reconstruction approaches can contribute to meeting these requirements, and what are their limitations?

### 1. Concepts and definitions

[TODO] Check if these section is still valuable and isn't redundant

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
The pipeline combines the scan-to-BIM framework [11, Sec. 1] with the stages of image-based reconstruction [9, Sec. 7]. The scan-to-BIM framework assumes a laser scanner, which delivers a point cloud directly. With a camera, the point cloud is computed from the video (stage 2).

| Stage | Output | Source |
|---|---|---|
| 1. Capture | Video | [11, Sec. 1] |
| 2. Camera poses and geometry | Point cloud | [9, Sec. 7] |
| 3. Semantics | Detected and classified assets | [11, Sec. 1] |
| 4. Asset list or BIM | Asset list or BIM model | [11, Sec. 1] |

### 3. Capture devices (stage 1)
All devices output video. The Samsung Galaxy S25 is a personal device. Heijmans provides the Ray-Ban Meta glasses and the Insta360 X6. ISSD provides the DJI Osmo Pocket 3, the GoPro Fusion and the Ricoh Theta S. No source lists a depth sensor for any device. "Not listed" means that the source does not mention the property. "Unverified" means that no manufacturer document was found.

[TODO] Check the table 

| Device | Type | Motion data saved with the video | Data security (R3): transfer without Wi-Fi or cloud | Recording limit | Processing before reconstruction |
|---|---|------|------| ------ | ------ |
| Samsung Galaxy S25 | Smartphone | Not confirmed. Accelerometer and gyroscope are present [12] (third party) | Yes. Internal storage, USB cable to a computer [17] | Not confirmed. Samsung states a 10 minute limit for high-resolution video on Galaxy phones in general [22] | None expected. Standard video file |
| Ray-Ban Meta glasses Gen 2 (Wayfarer) | Smart glasses | Not found | Not confirmed. Internal storage. The documented transfer runs through the Meta AI phone app (unverified) | 3 or 5 minutes per video, sources disagree (unverified) | None expected after the transfer through the phone app (unverified) |
| DJI Osmo Pocket 3 | Handheld gimbal camera | Not listed [14] | Yes. microSD card, card reader or USB cable [18] | Battery: 166 minutes at 1080p and 24 fps [14]. Limit per video not found | None. MP4 file [14] |
| Insta360 X6 | 360° camera | Not confirmed. A six-axis gyroscope is present [13] | Yes. microSD card, USB file transfer mode [19] | Battery: about 140 minutes at 8K and 30 fps [13]. Limit per video not found | Stitching with Insta360 software (unverified) |
| GoPro Fusion | 360° camera | Yes. Accelerometer (200 Hz), gyroscope (3200 Hz) and magnetometer [15] | Yes. Two microSD cards (one per lens), card reader or USB cable [20] | Battery: about 75 minutes at 5.2K and 30 fps [23] (third party) | Stitching of the two files with GoPro Fusion Studio [20] |
| Ricoh Theta S | 360° camera | Not listed [16] | Yes. Internal storage, USB cable to a computer [21] | 25 minutes per video [16] | Conversion with the RICOH THETA computer application [24] |

### 4. Method families per pipeline stage

| Stage | Family | Short description | Researched methods |
|---|---|---|---|
| 2. Camera poses and geometry | Photogrammetry (SfM and MVS) | Computes camera positions and 3D points from features matched across overlapping images, then estimates dense depth | COLMAP, GLOMAP, OpenSfM, Agisoft Metashape, RealityScan |
| 2. Camera poses and geometry | Visual SLAM | Estimates the camera position frame by frame while building a map, and corrects drift when a place is revisited (loop closure) | stella_vslam, ORB-SLAM3, DROID-SLAM, DPV-SLAM, MASt3R-SLAM |
| 2. Camera poses and geometry | Feed-forward reconstruction models | A neural network predicts camera positions, depth and 3D points from a set of images in one pass | VGGT, MapAnything, Depth Anything 3 |
| 2. Camera poses and geometry | Gaussian splatting | Optimises many small coloured blobs until rendered images match the video frames. Needs camera positions from another method | gsplat and Nerfstudio (including 2D Gaussian splatting), DN-Splatter, 3DGRUT, Postshot, Insta360 Spatial Capture |
| 3. Semantics | Open-vocabulary detection in images | Detects objects in video frames from a text description, without training on the asset type | Grounding DINO, OWLv2, YOLO-World and YOLOE, Florence-2, Qwen2.5-VL and Qwen3-VL |
| 3. Semantics | Segmentation and tracking in video | Outlines objects and follows each one through the video, so that one asset gets one identity | SAM 3, SAM 2 |
| 3. Semantics | Fine-tuned closed-set detectors | Detectors trained on labelled example images of the target asset types | RF-DETR, Ultralytics YOLO11 |
| 3. Semantics | 2D-to-3D lifting | Projects detections from many frames into the 3D model and merges them into one position per asset | Own projection and clustering baseline, OpenMask3D, Open-YOLO 3D |
| 3. Semantics | Detection in 3D and structured room models | Recognises objects directly in the point cloud, or describes the room as walls, doors, windows and objects | SpatialLM, Mask3D |

### 5. Comparison of methods
The proposed methods are compared against the evaluation criteria described above. [TODO] state the specific section. Scores (--, -, +, ++) are expected values from published results and documentation, not measurements. "?" means no source reports the property.

**Reconstruction (stage 2)**

| Method | Family | C1 | C2 | C3 | C5 | C6 | C7 | Commercial use |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| COLMAP [25] | Photogrammetry | ++ | + | - | -- | ++ | + | Yes |
| GLOMAP [26] | Photogrammetry | ++ | + | - | + | ++ | + | Yes |
| OpenSfM [27] | Photogrammetry | + | + | - | - | ++ | ++ | Yes |
| Agisoft Metashape [28] | Photogrammetry | ++ | + | - | + | ++ | ++ | Paid |
| RealityScan [29] | Photogrammetry | ++ | + | - | ++ | - | + | Free below 1 million USD revenue, paid above |
| stella_vslam [30] | Visual SLAM | - | -- | + | ++ | ++ | ++ | Yes |
| ORB-SLAM3 [31] | Visual SLAM | - | -- | + | ++ | ++ | + | Yes, copyleft (GPL) |
| DROID-SLAM [32] | Visual SLAM | + | - | ++ | + | ++ | + | Yes |
| DPV-SLAM [33] | Visual SLAM | + | -- | + | ++ | ++ | + | Yes |
| MASt3R-SLAM [34] | Visual SLAM | + | + | ++ | + | ++ | + | No |
| VGGT [35] | Feed-forward | + | + | ++ | ++ | ++ | + | Yes, commercial checkpoint only, no military use |
| MapAnything [36] | Feed-forward | + | + | + | ++ | ++ | + | Yes, Apache checkpoint only |
| Depth Anything 3 [37] | Feed-forward | + | + | + | ++ | ++ | + | Small, Base and Metric-Large models only |
| gsplat and Nerfstudio, 2D Gaussian splatting [38], [39], [40] | Gaussian splatting | ? | ++ | - | - | ++ | + | Yes |
| DN-Splatter [41] | Gaussian splatting | + | ++ | + | - | ++ | + | Yes |
| 3DGRUT [42] | Gaussian splatting | ? | ++ | - | - | ++ | ++ | Yes |
| Postshot [43] | Gaussian splatting | ? | ++ | ? | + | - | + | Paid |
| Insta360 Spatial Capture [44] | Gaussian splatting | ? | + | ? | ++ | -- | - | Paid cloud service |

The five reconstruction methods selected for testing are justified in Recommendations, sec. 1. [TODO] state explicitly where

**Asset detection (stage 3)**

"3D position": whether the method locates the asset in the room by itself.

| Method | Family | C4 | C5 | C6 | C7 | 3D position | Commercial use |
| --- | --- | --- | --- | --- | --- | --- | --- |
| SAM 3 [45] | Segmentation and tracking | ++ | + | ++ | ++ | No | Yes, no military use |
| Grounding DINO with SAM 2 [46], [47] | Open-vocabulary detection | + | + | ++ | ++ | No | Yes |
| OWLv2 [48] | Open-vocabulary detection | + | + | ++ | ++ | No | Yes |
| YOLO-World [49] and YOLOE [50] | Open-vocabulary detection | + | ++ | ++ | ++ | No | Yes, copyleft (GPL, AGPL) [TODO] rename in better way |
| Florence-2 [51] | Open-vocabulary detection | + | ++ | ++ | ++ | No | Yes |
| Qwen2.5-VL [52] and Qwen3-VL [53] | Open-vocabulary detection | + | - | ++ | ++ | No | Yes |
| RF-DETR [54] | Fine-tuned closed-set detector | ++ after training, -- before | ++ | ++ | ++ | No | Yes |
| Ultralytics YOLO11 [55] | Fine-tuned closed-set detector | ++ after training, -- before | ++ | ++ | ++ | No | Yes, copyleft (AGPL), or paid licence |
| Own projection and clustering baseline | 2D-to-3D lifting | Depends on 2D detector | + | ++ | ++ | Yes | Yes |
| OpenMask3D [56] | 2D-to-3D lifting | + | - | ++ | - | Yes | Yes |
| Open-YOLO 3D [57] | 2D-to-3D lifting | + | + | ++ | - | Yes | No, no licence stated |
| SpatialLM [10] | Structured room model | - | + | ++ | + | Yes, with room layout | No (weights) |
| Mask3D [58] | Detection in 3D | -- | + | ++ | - | Yes | Code yes, pretrained weights unclear |

The five detection methods selected for testing are justified in Recommendations, sec. 1.

### 6. Reported results and limitations
- **Reconstruction:** camera-based reconstruction is cheaper but less accurate than laser scanning [3, Sec. 2.2.2]. Photogrammetry breaks into disconnected parts and has difficulty with uniform surfaces and reflective materials [9, Sec. 8], and its accuracy degrades for large areas [11, Sec. 1].
- **New reconstruction methods:** the indoor geometric accuracy of Gaussian splatting has not been measured [7, Sec. 1, Sec. 4.2], and an outdoor study found that it is not yet a mapping tool [8, Sec. 5]. No indoor accuracy study was found for the feed-forward models.
- **Detection:** open-vocabulary detectors without fine-tuning failed on specialised building components (precision at most 0.02), while a fine-tuned detector reached 0.87 [64, Sec. 3]. On distinctive objects such as exit signs, an open-vocabulary detector found all instances [63, Sec. 6]. Small objects are detected less reliably than large ones [59, Sec. 4.1].
- **3D position:** detected assets can be placed in a 3D model [60], [62]. A sign on a wall was located within about 4 cm, but signs on ceilings or windows deviated by metres because the detection box contained background [63, Sec. 6]. The closest comparable study reports localisation errors of 0.43 m and 0.62 m [61, Abstract], and structured room models score lower on point clouds reconstructed from video [10, App. C.3].
- **Gaps:** no study tests these methods with video from a handheld or wearable camera in a finished building. This is why the selection in Recommendations, sec. 1 must be tested.

## Recommendations for SQ3 and SQ4

### 1. Methods to test
Selection rule, in this order: (1) works with colour video and runs locally on one 24 GB GPU (C5, C6, C7), (2) commercial use allowed, (3) expected quality (C1 and C2, or C4), (4) different method families. The scores are expected values, so each selection is a hypothesis for the experiments.

**Reconstruction (stage 2)**

| Rank | Method | Role | Why selected | Main risk | What to test |
|---|------|------|------|------|------|
| 1 | COLMAP with GLOMAP [25], [26] | Accuracy baseline | Reference pipeline [9], permissive licence, GLOMAP makes it faster | Holes or broken models at blank walls and glass [9, Sec. 8], slow | C1, C2, processing time |
| 2 | MapAnything [36] | Fast, real-world scale | Only permissive method that outputs real-world scale (R2) | Accuracy on long buildings and frame limit on 24 GB unknown | Scale error, maximum frames per run |
| 3 | VGGT [35] | Fast, feed-forward reference | Seconds per scene, tolerant of difficult images | No real-world scale, long videos must be split | C1 after scaling, drift between parts |
| 4 | stella_vslam [30] | Camera positions from 360° video | Only open method that reads 360° video directly (3 of 6 devices) | Sparse map only, no real-world scale | Completeness of the camera path, drift |
| 5 | DN-Splatter [41] | Dense model from ranks 1 to 4 | Built for indoor geometry, fills blank walls, gives a mesh | Indoor accuracy of splatting not established [7], [8] | C1, C2 compared with rank 1 |

Runner-ups: DROID-SLAM [32], Depth Anything 3 [37].

**Asset detection (stage 3)**

| Rank | Method | Role | Why selected | Main risk | What to test |
|---|---|---|---|---|---|
| 1 | SAM 3 [45] | Detect and track assets from a text prompt | No training needed, tracking supports counting each asset once (R1) | Open-vocabulary models failed on specialised components [64, Sec. 3] | C4 per asset type |
| 2 | Grounding DINO with SAM 2 [46], [47] | Permissive alternative to rank 1 | Found all exit signs in panoramas [63, Sec. 6] | Same as rank 1 | C4 compared with rank 1 |
| 3 | Own projection and clustering step | 3D position and count per room | Needed for R1 and R2 with any 2D detector | Background in boxes causes metre-level errors [63, Sec. 6] | Position error (R2), count error (R1) |
| 4 | RF-DETR [54] | Detector trained on labelled assets | Fine-tuned detectors clearly outperformed open-vocabulary ones [64, Sec. 3]. Public datasets exist [61], [65], but their licences restrict or do not state commercial use | Covers only trained asset types | C4 compared with ranks 1 and 2 |
| 5 | SpatialLM [10] | Room layout | Only method that outputs walls, doors and windows, needed to assign assets to rooms (R1) | Research-only weights, furniture classes | Correct room assignment |

Runner-ups: OWLv2 [48], Qwen2.5-VL [52] or Qwen3-VL [53]. If floor plans can assign assets to rooms, OWLv2 replaces rank 5.

### 2. First experiment
The first experiment narrows the selection of sec. 1 down to one reconstruction method (rank 1) and one detection method (rank 1), tested in one room on one asset type. It establishes a baseline. The other selected methods are tested later, one at a time, against this baseline.

| Step | Choice | Justification |
|---|------|------|
| Capture | Samsung Galaxy S25, normal video, video stabilisation off (optical stabilisation of the lens stays active), one room | Standard video file that can be transferred without Wi-Fi or cloud (SQ2, sec. 3). Stabilisation shifts and crops the frames, which disturbs reconstruction |
| Reconstruction | COLMAP [25] | Rank 1 in sec. 1, the reference method. All later reconstruction methods are compared with it |
| Scale | One distance measured with a tape measure | Simplest way to obtain real-world scale (R2) |
| Detection | SAM 3 [45] with a text prompt. | Rank 1 in sec. 1. Needs no training data. Tests whether open-vocabulary detection works for this asset type: it failed on specialised building components [64, Sec. 3] but worked on distinctive exit signs [63, Sec. 6]. If it fails, RF-DETR (rank 4) is tested next |
| Asset type | Fire extinguishers | Easy to describe in a text prompt and easy to count by hand |
| 3D position and count | Own projection and clustering step, using segmentation masks instead of boxes | Needed for R1 and R2. Boxes include background points, which caused position errors of several metres [63, Sec. 6] |
| Reference | Hand count and tape measurements of each fire extinguisher | Ground truth for C1 and C4 |

Results to report:
- Detection precision, recall and F1 (C4).
- Count error for the room (R1).
- Position error per fire extinguisher in cm (R2).
- Processing time per step (C5).

[TODO] First experiment": "Later experiment: check whether small assets remain detectable in 360° footage, which covers a room in one pass but spreads its resolution over the full view

### 4. Available hardware for testing

| Component | Specification |
|---|-----------|
| Operating system | Ubuntu 24.04.4 LTS |
| CPU | AMD Ryzen 9 7950X, 16 cores, 32 threads |
| RAM | Approximately 128 GB |
| GPUs | Two NVIDIA RTX 4090, approximately 24 GB VRAM each |
| Free storage | Approximately 42 GB on the project filesystem when checked |

Note: GPU memory does not combine across cards, so experiments should fit on one GPU.

# Research process
This research uses the following ICT research methods from the DOT framework [5]:

| Method | DOT strategy | Activity |
|---|---|---------|
| Expert interview | Library | Heijmans stakeholders were interviewed about the maintenance process and its problems. An interview was conducted also with a maintenance expert. Fontys ICT Game Design and Video Production experts were interviewed about 3D reconstruction of physical spaces used for gaming and video production. |
| Literature study | Library | Review papers on BIM for existing buildings, scan-to-BIM, and condition assessment were studied to describe the domain and the research gap. |
| Available product analysis | Library | Existing reconstruction software and commercial capture products were reviewed for their output, licence, and hardware requirements. |
| Problem analysis | Field | The interview results were documented in a problem analysis, which was discussed with and approved by the stakeholders. |
| Benchmark test | Showroom | [TODO] Selected methods are compared on the same captured data using the metrics from SQ1. |
| Decomposition | Workshop | [TODO] The reconstruction process was decomposed into pipeline stages (capture, localisation, geometry, semantics, BIM) to compare methods per stage. |
| Prototyping | Workshop | [TODO] A prototype was built to investigate what different algorithms can do using Samsung Galaxy S25 video. |
| Requirements prioritization | Workshop | [TODO] |

## Conclusion [TODO]
- What is known: summary of the method families and their reported performance.
- What is missing: the research gap.
- how each SQ addresses the gap.

## References
[1] R. Volk, J. Stengel, and F. Schultmann, "Building information modeling (BIM) for existing buildings: Literature review and future needs," *Automation in Construction*, vol. 38, pp. 109-127, 2014, doi: 10.1016/j.autcon.2013.10.023.

[2] N. Montás-Laracuente *et al.*, "A systematic review of artificial intelligence for capturing real-world structures into building information modelling," *Journal of Building Engineering*, vol. 113, Art. no. 114093, 2025, doi: 10.1016/j.jobe.2025.114093.

[3] N. Abreu, A. Pinto, A. Matos, and M. Pires, "Procedural point cloud modelling in scan-to-BIM and scan-vs-BIM applications: A review," *ISPRS International Journal of Geo-Information*, vol. 12, no. 7, Art. no. 260, 2023, doi: 10.3390/ijgi12070260.

[4] *Conditiemeting gebouwde omgeving - Deel 1: Methodiek*, NEN 2767-1+C1:2019, NEN, Delft, The Netherlands, 2019.

[5] HBO-i, "ICT research methods: Methods pack for research in ICT," 2018. [Online]. Available: https://ictresearchmethods.nl/

[6] W. Zhang, Y. Wu, S. Li, W. Ma, X. Ma, Q. Li, and Q. Wang, "Review of feed-forward 3D reconstruction: From DUSt3R to VGGT," arXiv preprint arXiv:2507.08448, 2025.

[7] S. Xu, J. Wang, J. Xia, and W. Shou, "Evaluating radiance field-inspired methods for 3D indoor reconstruction: A comparative analysis," *Buildings*, vol. 15, no. 6, Art. no. 848, 2025, doi: 10.3390/buildings15060848.

[8] S. McNally, S. Jabari, H. McGrath, and M. Masry, "A comprehensive evaluation of the spatial accuracy of building Gaussian splatting," *ISPRS Annals of the Photogrammetry, Remote Sensing and Spatial Information Sciences*, vol. XI-M-1-2026, pp. 31-38, 2026, doi: 10.5194/isprs-annals-XI-M-1-2026-31-2026.

[9] A. Knapitsch, J. Park, Q.-Y. Zhou, and V. Koltun, "Tanks and temples: Benchmarking large-scale scene reconstruction," *ACM Transactions on Graphics*, vol. 36, no. 4, Art. no. 78, 2017, doi: 10.1145/3072959.3073599.

[10] Y. Mao *et al.*, "SpatialLM: Training large language models for structured indoor modeling," in *Advances in Neural Information Processing Systems (NeurIPS)*, 2025. [Online]. Available: https://arxiv.org/abs/2506.07491

[11] R. Rashdi, J. Martínez-Sánchez, P. Arias, and Z. Qiu, "Scanning technologies to building information modelling: A review," *Infrastructures*, vol. 7, no. 4, Art. no. 49, 2022, doi: 10.3390/infrastructures7040049.

[12] Columbia University Information Technology, "Samsung Galaxy S25 specifications." Accessed: Nov. 15, 2026. [Online]. Available: https://www.cuit.columbia.edu/sites/default/files/content/CUIT%20Website%20Pages/Phone%20Specs/s25.pdf

[13] Insta360, "Insta360 X6 user manual: Hardware specifications." Accessed: Nov. 15, 2026. [Online]. Available: https://onlinemanual.insta360.com/x6/en-us/specs/hardware

[14] DJI, "Osmo Pocket 3: Specs." Accessed: Nov. 15, 2026. [Online]. Available: https://www.dji.com/osmo-pocket-3/specs

[15] GoPro, "GPMF parser." GitHub. Accessed: Nov. 15, 2026. [Online]. Available: https://github.com/gopro/gpmf-parser

[16] Ricoh Imaging, "RICOH THETA S." Accessed: Nov. 15, 2026. [Online]. Available: https://www.ricoh-imaging.co.jp/english/products/theta_s/

[17] Samsung, "Share and transfer files with your Galaxy phone and Windows." Accessed: Nov. 16, 2026. [Online]. Available: https://www.samsung.com/us/support/answer/ANS10001478/

[18] DJI, "Osmo Pocket 3: FAQ." Accessed: Nov. 16, 2026. [Online]. Available: https://www.dji.com/osmo-pocket-3/faq

[19] Insta360, "X series: Transferring files from camera to PC." Accessed: Nov. 16, 2026. [Online]. Available: https://onlinemanual.insta360.com/x6/en-us/operating-tutorials/connect/pc

[20] GoPro, "Fusion user manual." Accessed: Nov. 16, 2026. [Online]. Available: https://www.manualslib.com/manual/1356002/Gopro-Fusion.html

[21] Ricoh, "RICOH THETA S user guide: Importing still images and videos to a computer." Accessed: Nov. 16, 2026. [Online]. Available: https://theta-archive.ricoh360.com/support.theta360.com/en/manual/s/content/pc/pc_03

[22] Samsung, "Samsung phone stops recording videos after 10 minutes." Accessed: Nov. 16, 2026. [Online]. Available: https://www.samsung.com/us/support/troubleshoot/TSG10004918/

[23] Digital Trends, "GoPro Fusion review." Accessed: Nov. 16, 2026. [Online]. Available: https://digitaltrends.com/photography/gopro-fusion-review

[24] Ricoh, "RICOH THETA S user guide." Accessed: Nov. 16, 2026. [Online]. Available: https://theta-archive.ricoh360.com/support.theta360.com/en/manual/s/content/pc/pc_05

[TODO] Check the references

[25] J. L. Schönberger and J.-M. Frahm, "Structure-from-motion revisited," in *Proc. IEEE Conf. Comput. Vis. Pattern Recognit. (CVPR)*, 2016. [Online]. Available: https://www.cv-foundation.org/openaccess/content_cvpr_2016/papers/Schonberger_Structure-From-Motion_Revisited_CVPR_2016_paper.pdf

[26] L. Pan, D. Baráth, M. Pollefeys, and J. L. Schönberger, "Global structure-from-motion revisited," in *Proc. Eur. Conf. Comput. Vis. (ECCV)*, 2024. [Online]. Available: https://arxiv.org/abs/2407.20219

[27] OpenSfM contributors, "OpenSfM." GitHub. Accessed: Nov. 16, 2026. [Online]. Available: https://github.com/OpenSfM/OpenSfM

[28] Agisoft, "Processing spherical panoramas in Agisoft Metashape." Accessed: Nov. 16, 2026. [Online]. Available: https://agisoft.freshdesk.com/support/solutions/articles/31000161406-processing-spherical-panoramas-in-agisoft-metashape

[29] Epic Games, "RealityScan license." Accessed: Nov. 16, 2026. [Online]. Available: https://www.realityscan.com/license

[30] S. Sumikura, M. Shibuya, and K. Sakurada, "OpenVSLAM: A versatile visual SLAM framework," in *Proc. 27th ACM Int. Conf. Multimedia*, 2019, doi: 10.1145/3343031.3350539. Code (stella_vslam): https://github.com/stella-cv/stella_vslam

[31] C. Campos, R. Elvira, J. J. Gómez Rodríguez, J. M. M. Montiel, and J. D. Tardós, "ORB-SLAM3: An accurate open-source library for visual, visual-inertial and multi-map SLAM," *IEEE Trans. Robot.*, 2021, doi: 10.1109/TRO.2021.3075644.

[32] Z. Teed and J. Deng, "DROID-SLAM: Deep visual SLAM for monocular, stereo, and RGB-D cameras," in *Proc. Adv. Neural Inf. Process. Syst. (NeurIPS)*, 2021. [Online]. Available: https://arxiv.org/abs/2108.10869

[33] L. Lipson, Z. Teed, and J. Deng, "Deep patch visual SLAM," in *Proc. Eur. Conf. Comput. Vis. (ECCV)*, 2024. [Online]. Available: https://arxiv.org/abs/2408.01654

[34] R. Murai, E. Dexheimer, and A. J. Davison, "MASt3R-SLAM: Real-time dense SLAM with 3D reconstruction priors," in *Proc. IEEE/CVF Conf. Comput. Vis. Pattern Recognit. (CVPR)*, 2025. [Online]. Available: https://arxiv.org/abs/2412.12392

[35] J. Wang, M. Chen, N. Karaev, A. Vedaldi, C. Rupprecht, and D. Novotny, "VGGT: Visual geometry grounded transformer," in *Proc. IEEE/CVF Conf. Comput. Vis. Pattern Recognit. (CVPR)*, 2025. [Online]. Available: https://arxiv.org/abs/2503.11651

[36] N. Keetha *et al.*, "MapAnything: Universal feed-forward metric 3D reconstruction," in *Proc. Int. Conf. 3D Vis. (3DV)*, 2026. [Online]. Available: https://arxiv.org/abs/2509.13414

[37] H. Lin *et al.*, "Depth Anything 3: Recovering the visual space from any views," arXiv preprint arXiv:2511.10647, 2025.

[38] V. Ye *et al.*, "gsplat: An open-source library for Gaussian splatting," *J. Mach. Learn. Res.*, vol. 26, 2025. [Online]. Available: https://www.jmlr.org/papers/v26/24-1476.html

[39] M. Tancik *et al.*, "Nerfstudio: A modular framework for neural radiance field development," in *Proc. ACM SIGGRAPH Conf.*, 2023, doi: 10.1145/3588432.3591516.

[40] B. Huang, Z. Yu, A. Chen, A. Geiger, and S. Gao, "2D Gaussian splatting for geometrically accurate radiance fields," in *Proc. ACM SIGGRAPH Conf.*, 2024, doi: 10.1145/3641519.3657428.

[41] M. Turkulainen, X. Ren, I. Melekhov, O. Seiskari, E. Rahtu, and J. Kannala, "DN-Splatter: Depth and normal priors for Gaussian splatting and meshing," in *Proc. IEEE/CVF Winter Conf. Appl. Comput. Vis. (WACV)*, 2025. [Online]. Available: https://arxiv.org/abs/2403.17822

[42] Q. Wu, J. Martinez Esturo, A. Mirzaei, N. Moenne-Loccoz, and Z. Gojcic, "3DGUT: Enabling distorted cameras and secondary rays in Gaussian splatting," in *Proc. IEEE/CVF Conf. Comput. Vis. Pattern Recognit. (CVPR)*, 2025. [Online]. Available: https://arxiv.org/abs/2412.12507

[43] Jawset, "Postshot end user license agreement." Accessed: Nov. 16, 2026. [Online]. Available: https://activation.jawset.com/eula

[44] Insta360, "Insta360 and Splatica Gaussian splatting partnership." Accessed: Nov. 15, 2026. [Online]. Available: https://www.insta360.com/blog/enterprise/insta360-splatica-gaussian-splatting-partnership.html

[45] N. Carion *et al.*, "SAM 3: Segment anything with concepts," arXiv preprint arXiv:2511.16719, 2025.

[46] S. Liu *et al.*, "Grounding DINO: Marrying DINO with grounded pre-training for open-set object detection," arXiv preprint arXiv:2303.05499, 2023.

[47] N. Ravi *et al.*, "SAM 2: Segment anything in images and videos," arXiv preprint arXiv:2408.00714, 2024.

[48] M. Minderer, A. Gritsenko, and N. Houlsby, "Scaling open-vocabulary object detection," arXiv preprint arXiv:2306.09683, 2023.

[49] T. Cheng, L. Song, Y. Ge, W. Liu, X. Wang, and Y. Shan, "YOLO-World: Real-time open-vocabulary object detection," arXiv preprint arXiv:2401.17270, 2024.

[50] A. Wang, L. Liu, H. Chen, Z. Lin, J. Han, and G. Ding, "YOLOE: Real-time seeing anything," in *Proc. IEEE/CVF Int. Conf. Comput. Vis. (ICCV)*, 2025. [Online]. Available: https://arxiv.org/abs/2503.07465

[51] B. Xiao *et al.*, "Florence-2: Advancing a unified representation for a variety of vision tasks," arXiv preprint arXiv:2311.06242, 2023.

[52] S. Bai *et al.*, "Qwen2.5-VL technical report," arXiv preprint arXiv:2502.13923, 2025.

[53] S. Bai *et al.*, "Qwen3-VL technical report," arXiv preprint arXiv:2511.21631, 2025.

[54] I. Robinson, P. Robicheaux, M. Popov, D. Ramanan, and N. Peri, "RF-DETR: Neural architecture search for real-time detection transformers," in *Proc. Int. Conf. Learn. Represent. (ICLR)*, 2026. [Online]. Available: https://arxiv.org/abs/2511.09554

[55] Ultralytics, "Ultralytics YOLO." GitHub. Accessed: Nov. 16, 2026. [Online]. Available: https://github.com/ultralytics/ultralytics

[56] A. Takmaz, E. Fedele, R. W. Sumner, M. Pollefeys, F. Tombari, and F. Engelmann, "OpenMask3D: Open-vocabulary 3D instance segmentation," in *Proc. Adv. Neural Inf. Process. Syst. (NeurIPS)*, 2023. [Online]. Available: https://arxiv.org/abs/2306.13631

[57] M. E. A. Boudjoghra *et al.*, "Open-YOLO 3D: Towards fast and accurate open-vocabulary 3D instance segmentation," in *Proc. Int. Conf. Learn. Represent. (ICLR)*, 2025. [Online]. Available: https://arxiv.org/abs/2406.02548

[58] J. Schult, F. Engelmann, A. Hermans, O. Litany, S. Tang, and B. Leibe, "Mask3D: Mask transformer for 3D semantic instance segmentation," in *Proc. IEEE Int. Conf. Robot. Autom. (ICRA)*, 2023. [Online]. Available: https://arxiv.org/abs/2210.03105

[59] G. Baruch *et al.*, "ARKitScenes: A diverse real-world dataset for 3D indoor scene understanding using mobile RGB-D data," arXiv preprint arXiv:2111.08897, 2021.

[60] Y. Pan, A. Braun, I. Brilakis, and A. Borrmann, "Enriching geometric digital twins of buildings with small objects by fusing laser scanning and AI-based image recognition," *Autom. Constr.*, vol. 140, Art. no. 104375, 2022, doi: 10.1016/j.autcon.2022.104375.

[61] Y. Wen, Y. Qiao, C. C. Lam, I. Brilakis, S. Lee, and M. O. Wong, "Semantic BIM enrichment for firefighting assets: Fire-ART dataset and panoramic image-based 3D reconstruction," arXiv preprint arXiv:2511.01399, 2025.

[62] M. Tang and A. Zakhor, "Indoor asset detection in large scale 360° drone-captured imagery via 3D Gaussian splatting," in *Proc. IEEE/CVF Conf. Comput. Vis. Pattern Recognit. Workshops (3DMV)*, 2026. [Online]. Available: https://arxiv.org/abs/2604.05316

[63] S. De Geyter, M. Bassier, H. De Winter, and M. Vergauwen, "Object detection and localisation for BIM enrichment," *Int. Arch. Photogramm. Remote Sens. Spatial Inf. Sci.*, vol. XLVIII-1/W2-2023, 2023, doi: 10.5194/isprs-archives-XLVIII-1-W2-2023-155-2023.

[64] A. Abdalwhab, A. Imran, S. Heydarian, I. Iordanova, and D. St-Onge, "Are open-vocabulary models ready for detection of MEP elements on construction sites," in *Proc. 42nd Int. Symp. Autom. Robot. Constr. (ISARC)*, 2025. [Online]. Available: https://www.iaarc.org/publications/fulltext/184_Are_Open-Vocabulary_Models_Ready_for_Detection_of_MEP_Elements_on_Construction_Sites.pdf

[65] L. Arzoumanidis, W. Li, and Y. Dehbi, "Domain-adaptive object detection of electrical facilities for enhanced semantic indoor models," *ISPRS Ann. Photogramm. Remote Sens. Spatial Inf. Sci.*, vol. XI-2-2026, 2026, doi: 10.5194/isprs-annals-XI-2-2026-759-2026.
