# Method longlist: reconstruction and asset detection

Version: 16-11-2026. Status: first complete draft, to be verified (see Section 6).

## 1. Scope and method

### 1.1 Purpose
This document supports subquestion SQ2 of the background research document. It lists methods that can contribute to two stages of the pipeline:

- Stage 2, reconstruction: from video to camera positions and a 3D model of the room.
- Stage 3, asset detection: from the video and the 3D model to a list of assets per room, with their location.

The methods are compared with the evaluation criteria C1 to C7 of the background research document. Five methods per stage are recommended for testing.

### 1.2 Boundary conditions
The boundary conditions follow from the requirements R1 to R5 and from the available capture devices.

- The input is ordinary colour video. No capture device has a depth sensor. Motion sensor data is confirmed for one device only (GoPro Fusion).
- Three of the six capture devices are 360° cameras.
- Processing is preferred on own hardware: one PC with one NVIDIA RTX 4090 graphics card (24 GB memory) running Ubuntu.
- Open-source software with a licence that allows commercial use has priority. Research-only software and commercial products are listed and marked.
- Spatial accuracy has priority over visual realism. The indicative target is 10 to 15 cm.

### 1.3 Search and selection procedure
The selection followed a funnel with three steps.

1. **Wide scan (95 methods and products).** Candidates were collected from the papers in the repository, the link list (`links.md`), the review on feed-forward reconstruction [ref. 6 in background document], and the author's knowledge of the field up to mid-2026. Appendix A lists all candidates that were not selected, with the reason.
2. **Screening (30 methods).** A candidate was removed when it failed one of these checks: (a) works with colour video without a depth sensor or a laser scanner, (b) code or product is available, (c) runs on one 24 GB graphics card or in an available product, (d) no better maintained successor exists in the list.
3. **Scoring and ranking (5 plus 5).** The remaining methods were scored against the criteria and ranked with the rule in Section 1.4.

Limitation of this procedure: a planned automated web search with several parallel search agents stopped because of a usage limit before it returned results. The wide scan therefore relies on the author's knowledge and on targeted web checks. Licences of all 30 selected methods and the key vendor statements were checked online on 16-11-2026. Each entry states its verification status (Section 1.5).

### 1.4 Scores and ranking rule
Scores use the scale --, -, +, ++. A question mark means that no source reports the property.

The scores are **expected values**, not measurements. They are derived from published benchmark results, documentation and known properties of each method family. Benchmarks use other scenes and cameras than this project, so the scores are hypotheses that the experiments of SQ4 must test.

| Criterion | ++ | -- |
|---|---|---|
| C1 Geometric accuracy | Accurate camera positions and geometry on published indoor or large-scene benchmarks | Known large errors, or no real-world scale and no way to obtain it |
| C2 Completeness | Dense model of walls, ceiling and objects | Only a sparse set of points |
| C3 Robustness | Designed for difficult conditions (white walls, changing light, long sequences) | Known to break on such conditions |
| C4 Asset detection quality | Finds new asset types from a text description, or is proven on similar small objects | Fixed furniture classes only, retraining needed |
| C5 Processing time and hardware | Seconds to minutes per room on one GPU | Hours per room, or more than 24 GB GPU memory |
| C6 Runs locally | Code and weights run on own hardware under Linux | Cloud service only |
| C7 Input type | Works with video from all device types, including 360° | Needs a depth sensor or special hardware |

Ranking rule for the recommendations, in this order:
1. Fit to the boundary conditions: colour video input, runs locally on one 24 GB GPU (C5, C6, C7).
2. Licence: commercial use allowed > research only > commercial product.
3. Expected accuracy and completeness (C1, C2 for reconstruction, C4 for detection).
4. Diversity: the five methods should cover different method families, so that the tests compare approaches and not variants of one approach.

### 1.5 Verification status
Each method has one of these labels in the tables. Author lists and venues in the reference list are a separate matter, see the note above the references.

- **Checked:** licence read from the official repository through the GitHub interface, from the Hugging Face model card, or from a web source summarising the official page, on 16-11-2026.
- **Memory:** taken from the author's knowledge, not checked online. To be verified before use in the background research document.

## 2. Reconstruction longlist

### 2.1 Photogrammetry: structure from motion and multi-view stereo

**Main idea.** Photogrammetry measures 3D shape from overlapping photos. When the same point of a room is visible in two photos taken from different positions, its 3D position can be computed by intersecting the two viewing rays, in the same way that two eyes judge distance.

**How it works.**
1. *Feature detection:* the software finds distinctive spots in each image, such as corners or texture patterns.
2. *Matching:* it finds the same spots in other images.
3. *Structure from motion (SfM):* from these matches it computes where each photo was taken (camera position and direction) and the 3D position of the matched spots. The result is a sparse point cloud.
4. *Multi-view stereo (MVS):* with the camera positions known, it estimates a depth value for almost every pixel and merges them into a dense point cloud or mesh.

**Typical weaknesses.** Plain white walls, glass and mirrors give no reliable features, so the model gets holes or breaks into separate parts [9]. The result has no real-world scale: a room and a doll's house look the same in photos. One known distance (for example a tape measurement) fixes the scale. Large scenes take hours to process.

| Method | What it does | Input and 360° support | Licence | Status |
|---|---|---|---|---|
| COLMAP [1], [2] | Reference open-source SfM and MVS pipeline, one of the pipelines evaluated in the Tanks and Temples benchmark [9 in background document] | Images or video frames. 360° video must first be split into normal (perspective) views | BSD 3-clause ("new BSD"). Dependencies are licensed separately | Checked |
| GLOMAP [3] | Faster SfM that solves all camera positions at once instead of adding them one by one. Uses COLMAP for the dense step | As COLMAP | BSD 3-clause | Checked |
| OpenSfM [4] | SfM pipeline by Mapillary, also used inside OpenDroneMap | Images or frames. The camera models of the continued project include spherical (equirectangular) images | BSD 2-clause. Mapillary stopped development. The project continues at github.com/OpenSfM/OpenSfM | Checked |
| Agisoft Metashape [5] | Commercial photogrammetry software used in surveying | Images or frames. Supports frame, fisheye, spherical and cylindrical cameras | Commercial, paid licence. Runs on Windows, macOS and Linux | Checked |
| RealityScan [6] | Commercial photogrammetry software by Epic Games (formerly RealityCapture) | Images or frames | Commercial. Free for organisations below 1 million USD revenue in the past 12 months, otherwise 1250 USD per seat per year. Windows only | Checked |

### 2.2 Visual SLAM

**Main idea.** SLAM (simultaneous localisation and mapping) comes from robotics. It processes the video frame by frame while the camera moves, and estimates at each moment where the camera is and what the surroundings look like. It is built to work in real time, so it is fast.

**How it works.**
1. *Tracking:* for each new frame, the method estimates how far the camera moved since the previous frame.
2. *Mapping:* it adds new 3D points of the surroundings to a map.
3. *Drift:* small errors in each step add up, so after a long corridor the estimated position slowly deviates from the true one. This is called drift.
4. *Loop closure:* when the camera returns to a place it has seen before, the method recognises it and corrects the accumulated drift along the whole path.

**Typical weaknesses.** Most classical SLAM methods produce only a sparse map that is useful for positions but not as a 3D model. With one camera and no motion sensor the scale is unknown, and the scale can also change slowly along the walk. Learned SLAM methods produce dense maps but need a strong graphics card.

| Method | What it does | Input and 360° support | Licence | Status |
|---|---|---|---|---|
| stella_vslam [7] | Feature-based SLAM, successor of OpenVSLAM | Monocular video. Supports perspective, fisheye and equirectangular (360°) cameras | BSD 2-clause. Versions before 0.3 were GPL | Checked |
| ORB-SLAM3 [8] | Widely used feature-based SLAM, also with motion sensor data | Monocular, stereo, with or without IMU. Pinhole and fisheye | GPL-3.0 (copyleft). A closed-source commercial licence is available from the authors | Checked |
| DROID-SLAM [9] | Learned SLAM that estimates dense depth and camera motion with a neural network | Monocular, stereo or RGB-D video. Pinhole cameras | BSD 3-clause | Checked |
| DPV-SLAM [10] | Lighter learned SLAM that tracks small image patches | Monocular video | MIT | Checked |
| MASt3R-SLAM [11] | Real-time dense SLAM built on the MASt3R feed-forward model | Monocular video, no calibration needed | CC BY-NC-SA 4.0 (research only) | Checked |

### 2.3 Feed-forward reconstruction models

**Main idea.** These are large neural networks trained on millions of images with known 3D shape. They look at a set of images and directly output, in one pass, the camera positions and a 3D point for every pixel. They skip the step-by-step calculations of photogrammetry, which makes them fast and more tolerant of difficult images [ref. 6 in background document].

**How it works.**
1. The images are cut into small patches and turned into numbers by the network.
2. The network compares all patches of all images with each other (attention) to find which parts belong together.
3. It outputs a depth map, a 3D point per pixel and the camera position for each image.
4. Some models (MapAnything, Depth Anything 3 metric) are trained to output real-world scale directly.

**Typical weaknesses.** Memory use grows with the number of images, so a long walkthrough must be split into chunks and joined afterwards, which can introduce drift. The result is a learned estimate: it can look plausible without being correct, which matters for the accuracy requirement. Several models are released for research use only.

| Method | What it does | Real-world scale | Licence | Status |
|---|---|---|---|---|
| VGGT [12] | Predicts cameras, depth and 3D points from up to hundreds of images in seconds | No | Custom VGGT License (July 2025). Checkpoint VGGT-1B-Commercial is licensed for commercial use except military applications. The original checkpoint is non-commercial | Checked |
| MapAnything [13] | Predicts a metric 3D reconstruction and camera positions from images, optionally with extra inputs such as known camera parameters | Yes | Code Apache 2.0. Checkpoint `map-anything-apache` Apache 2.0. Default checkpoint CC BY-NC 4.0 | Checked |
| Depth Anything 3 [14] | Predicts depth and camera positions from any number of views. A separate metric model outputs real-world depth | Yes (metric model) | Code Apache 2.0. Small, Base and Metric-Large models Apache 2.0. Large and Giant models CC BY-NC 4.0 | Checked |

### 2.4 Gaussian splatting and neural surfaces

**Main idea.** These methods build a 3D model by trial and error. Gaussian splatting represents the scene as millions of small coloured, semi-transparent blobs. The computer renders images from the known camera positions, compares them with the real video frames and adjusts the blobs until the rendered images match [15].

**How it works.**
1. Camera positions are computed first, usually with COLMAP or a feed-forward model. Splatting cannot work without them.
2. The blobs are placed at an initial sparse point cloud.
3. In thousands of iterations, the blobs are moved, resized and recoloured to reduce the difference between rendered and real images.
4. A mesh or point cloud can be extracted from the blobs afterwards.

**Why realistic is not the same as accurate.** The optimisation rewards correct-looking images, not correct geometry. A blank wall can be faked by blobs floating in front of it, and the picture still looks right. Surface-oriented variants (2D Gaussian splatting, DN-Splatter) force the blobs to lie flat on surfaces, which improves geometry. An outdoor study found that Gaussian splatting is not yet a mapping tool [ref. 8 in background document].

| Method | What it does | Input and 360° support | Licence | Status |
|---|---|---|---|---|
| gsplat and Nerfstudio [16], [17] | Open-source library and framework for Gaussian splatting. Contains Splatfacto and a 2D Gaussian splatting option for flat surfaces [18] | Images with camera positions. gsplat also supports fisheye cameras | Apache 2.0 | Checked |
| DN-Splatter [19] | Gaussian splatting for indoor scenes that uses estimated depth and surface direction to improve geometry and to extract meshes | Images with camera positions, plus depth and normal estimates from a neural network | Apache 2.0 | Checked |
| 3DGRUT (3DGRT and 3DGUT) [20] | NVIDIA Gaussian splatting that supports fisheye lenses and rolling shutter | Images with camera positions, fisheye supported | Apache 2.0 | Checked |
| Postshot [21] | Commercial desktop software for Gaussian splatting, recommended by a video production expert (see `links.md`) | Video or images | Commercial, time-limited licence. The licence agreement states that an internet connection is required to use it. Supported operating systems not confirmed | Checked (licence agreement only) |
| Insta360 Spatial Capture with Splatica [22] | Cloud service that turns a short Insta360 360° video into a Gaussian splat | Insta360 360° video | Commercial cloud service | Checked (earlier in this project) |

## 3. Detection longlist

### 3.1 Open-vocabulary detection in images

**Main idea.** A classical detector only finds the object types it was trained on, such as "chair" or "person". An open-vocabulary detector has learned the link between images and text from very large collections of images with captions. It can therefore search for any object described in words, for example "fire extinguisher" or "green emergency exit sign", without new training [23].

**How it works.**
1. The text prompt and the image are both turned into numbers by a neural network.
2. The detector compares image regions with the text and draws a box where they match.
3. Each box gets a confidence score. A threshold decides which boxes are kept.

**Typical weaknesses.** Small objects and rare object types are found less reliably than common ones. Vague prompts give false detections. The same asset is detected again in every frame where it is visible, so the detections must be merged before counting (Section 3.3).

| Method | What it does | Licence | Status |
|---|---|---|---|
| Grounding DINO and MM-Grounding-DINO [23] | Detects objects described by a text prompt. Often combined with SAM 2 for exact outlines (Grounded-SAM-2) | Apache 2.0 (Grounding DINO, Grounded-SAM-2 and MMDetection) | Checked |
| OWLv2 [24] | Open-vocabulary detector by Google, also accepts an example image instead of text | Apache 2.0 (Scenic repository) | Checked |
| YOLO-World and YOLOE [25], [26] | Fast open-vocabulary detectors in the YOLO family | GPL-3.0 (YOLO-World), AGPL-3.0 (YOLOE) | Checked |
| Florence-2 [27] | Small vision model by Microsoft that detects, describes and locates objects from text | MIT (model card) | Checked |
| Qwen2.5-VL and Qwen3-VL [28] | Vision-language models that can answer questions about an image and return box coordinates. Useful to check detections from a faster detector | Apache 2.0 (code and the 7B model card checked) | Checked |

### 3.2 Segmentation and tracking in video

**Main idea.** Segmentation finds the exact outline of an object instead of a box. Tracking follows the same object through the video, so that one physical asset gets one identity even when it is visible in hundreds of frames. This is the basis for counting.

| Method | What it does | Licence | Status |
|---|---|---|---|
| SAM 3 [29] | Finds, outlines and tracks all instances of a concept described by a short text (for example "smoke detector") in images and video | Custom SAM License (November 2025). Commercial use allowed, with restrictions (no military use, export rules) | Checked |
| SAM 2 [30] | Outlines and tracks objects in video after a click or a box. Has no text input itself, so it is combined with a detector | Apache 2.0 | Checked |

### 3.3 Fine-tuned closed-set detectors

**Main idea.** A standard detector is trained on a labelled set of example images of the target assets. With a few hundred labelled examples per asset type, such detectors are usually more accurate and faster than open-vocabulary detectors, but every new asset type needs new labels.

| Method | What it does | Licence | Status |
|---|---|---|---|
| RF-DETR [31] | Transformer-based real-time detector, designed to be fine-tuned on small custom datasets | Apache 2.0 | Checked |
| Ultralytics YOLO11 [32] | Widely used detector with simple training tools | AGPL-3.0, or paid enterprise licence | Checked (AGPL) |

### 3.4 From 2D detections to 3D asset positions

**Main idea.** A detection in a video frame says where the asset is in the image, not where it is in the room. Because the reconstruction step provides the camera position of each frame and a 3D model, each detection can be projected into the 3D model. Detections of the same asset from many frames then fall on the same spot and are merged into one asset with one position. This merging removes double counts.

**How it works.**
1. Detect or segment assets in many frames (Sections 3.1 to 3.3).
2. For each detection, follow the viewing ray from the camera through the detected pixels until it hits the 3D model.
3. Group 3D detections that lie close together and have the same label.
4. Count the groups per room. The room boundaries come from the 3D model or from a floor plan.

**Typical weaknesses.** Errors in the camera positions move the 3D position of the asset. Many published methods expect depth images from a depth sensor. With this project's devices, depth must instead be rendered from the reconstructed model, which is an untested workaround.

| Method | What it does | Input | Licence | Status |
|---|---|---|---|---|
| Own projection and clustering baseline | Simple pipeline of steps 1 to 4 above, combining a 2D detector with the reconstruction output | Video frames, camera positions, 3D model | Own code | Design proposal, not a published method |
| OpenMask3D [33] | Open-vocabulary 3D instance segmentation: finds object instances in the point cloud and labels them with text | Point cloud plus posed colour and depth images | MIT | Checked |
| Open-YOLO 3D [34] | Faster open-vocabulary 3D instance segmentation that uses a 2D detector for the labels | Point cloud plus posed colour and depth images | No licence stated in the repository, so by default no right of use | Checked (secondary source) |

### 3.5 Detection directly in 3D and structured room models

**Main idea.** These methods work on the 3D point cloud instead of on video frames. Point cloud networks learn to recognise object shapes in 3D. Structured modelling methods such as SpatialLM go one step further: a language model reads the point cloud and writes a description of the room as a list of walls, doors, windows and objects with their boxes [ref. 10 in background document].

**Typical weaknesses.** Most models are trained on furniture in homes (ScanNet dataset) and do not know building assets such as smoke detectors. Small wall-mounted objects contain few 3D points. Point clouds from video are noisier than from depth sensors, and SpatialLM reports lower scores on such point clouds [ref. 10 in background document].

| Method | What it does | Input | Licence | Status |
|---|---|---|---|---|
| SpatialLM [ref. 10 in background document] | Language model that turns a point cloud into walls, doors, windows and object boxes. Tested on point clouds reconstructed from video | Point cloud | Mixed. Repository licence file is the Llama 3.2 Community License. README: code parts Apache 2.0, SpatialLM 1.1 weights CC BY-NC 4.0 (research only) | Checked |
| Mask3D [35] | 3D instance segmentation network trained on ScanNet classes | Point cloud | Code MIT. Pretrained weights depend on the ScanNet terms of use (not checked) | Checked (code) |

## 4. Scoring tables

### 4.1 Reconstruction

| Method | C1 | C2 | C3 | C5 | C6 | C7 | Licence | Main reason |
|---|---|---|---|---|---|---|---|---|
| COLMAP | ++ | + | - | -- | ++ | + | Commercial use | Reference pipeline with high accuracy [9 in background document], but slow and breaks on featureless walls |
| GLOMAP | ++ | + | - | + | ++ | + | Commercial use | Same accuracy class as COLMAP with much faster camera estimation |
| OpenSfM | + | + | - | - | ++ | ++ | Commercial use | Only open SfM pipeline here with native 360° support |
| Agisoft Metashape | ++ | + | - | + | ++ | ++ | Commercial product | Survey-grade tool that runs locally on Linux, but paid |
| RealityScan | ++ | + | - | ++ | - | + | Commercial product (free below revenue threshold) | Fast, but Windows only, while the test PC runs Ubuntu |
| stella_vslam | - | -- | + | ++ | ++ | ++ | Commercial use | Handles 360° video directly and closes loops, but gives only a sparse map |
| ORB-SLAM3 | - | -- | + | ++ | ++ | + | GPL-3.0 | Mature and fast, sparse map only, no 360° model |
| DROID-SLAM | + | - | ++ | + | ++ | + | Commercial use | Learned tracking is robust in difficult footage, dense depth is noisy |
| DPV-SLAM | + | -- | + | ++ | ++ | + | Commercial use | Light and fast, but sparse |
| MASt3R-SLAM | + | + | ++ | + | ++ | + | Research only | Dense and robust from uncalibrated video, licence excludes commercial use |
| VGGT (commercial checkpoint) | + | + | ++ | ++ | ++ | + | Commercial use, except military | Seconds per scene and tolerant of difficult images, no real-world scale, limited number of frames per run |
| MapAnything (Apache checkpoint) | + | + | + | ++ | ++ | + | Commercial use | Only feed-forward model with real-world scale under a permissive licence |
| Depth Anything 3 (Apache models) | + | + | + | ++ | ++ | + | Commercial use for Small, Base and Metric-Large | Strong depth and pose estimation, best models are research only |
| gsplat and Nerfstudio (2D Gaussian splatting) | ? | ++ | - | - | ++ | + | Commercial use | Dense surfaces, needs camera positions from another method, geometry accuracy indoors not established |
| DN-Splatter | + | ++ | + | - | ++ | + | Commercial use | Designed for indoor geometry, uses depth priors to fill blank walls |
| 3DGRUT | ? | ++ | - | - | ++ | ++ | Commercial use | Handles fisheye and rolling shutter, aimed at rendering rather than measurement |
| Postshot | ? | ++ | ? | + | - | + | Commercial product | Easy desktop splatting, but needs an internet connection, operating systems not confirmed, no accuracy statement |
| Insta360 Spatial Capture | ? | + | ? | ++ | -- | - | Commercial cloud service | Cloud processing conflicts with R3, Insta360 cameras only |

### 4.2 Detection
C4 scores assume the target asset types of R1 (small, wall or ceiling mounted). The column "3D position" states whether the method gives a position in the room by itself.

| Method | C4 | C5 | C6 | C7 | 3D position | Licence | Main reason |
|---|---|---|---|---|---|---|---|
| SAM 3 | ++ | + | ++ | ++ | No, needs projection (3.4) | Commercial use, with restrictions | Finds and tracks all instances of a text concept in video, which supports counting |
| Grounding DINO with SAM 2 | + | + | ++ | ++ | No, needs projection | Commercial use | Mature open-vocabulary detector, weaker on small objects |
| OWLv2 | + | + | ++ | ++ | No, needs projection | Commercial use | Accepts example images, useful for asset types that are hard to describe |
| YOLO-World and YOLOE | + | ++ | ++ | ++ | No, needs projection | GPL-3.0 and AGPL-3.0 | Real-time, but copyleft licences |
| Florence-2 | + | ++ | ++ | ++ | No, needs projection | Commercial use | Small and fast, lower accuracy than larger detectors |
| Qwen2.5-VL and Qwen3-VL | + | - | ++ | ++ | No | Commercial use | Slow per frame, best used to verify uncertain detections |
| RF-DETR (fine-tuned) | ++ after training, -- before | ++ | ++ | ++ | No, needs projection | Commercial use | Most accurate once labelled examples exist, needs labelling effort |
| Ultralytics YOLO11 (fine-tuned) | ++ after training, -- before | ++ | ++ | ++ | No, needs projection | AGPL-3.0 | As RF-DETR, licence less suitable |
| Own projection and clustering baseline | Depends on 2D detector | + | ++ | ++ | Yes | Own code | Turns any 2D detector into 3D positions and unique counts |
| OpenMask3D | + | - | ++ | - | Yes | Commercial use | Open-vocabulary 3D instances, needs depth images |
| Open-YOLO 3D | + | + | ++ | - | Yes | No licence stated | Faster than OpenMask3D, needs depth images |
| SpatialLM | - | + | ++ | + | Yes, plus room layout | Research only (weights) | Gives walls, doors and objects per room, but furniture classes |
| Mask3D | -- | + | ++ | - | Yes | Weights depend on ScanNet terms | Fixed classes, needs clean depth-sensor point clouds |

## 5. Recommended methods

### 5.1 Reconstruction: top 5

| Rank | Method | Why | Main risk |
|---|---|---|---|
| 1 | COLMAP (with GLOMAP for speed) | Established accuracy reference [9 in background document], permissive licence, runs on Linux. Every other method can be compared with it | Slow, and holes or broken models in rooms with blank walls |
| 2 | MapAnything (Apache checkpoint) | Only permissively licensed method that outputs real-world scale directly, which addresses R2 without a manual measurement | Accuracy on long, repetitive buildings unknown. Number of frames per run on 24 GB unknown |
| 3 | VGGT (commercial checkpoint) | Very fast and tolerant of difficult footage. Strong reference for the feed-forward family | No real-world scale. Long walkthroughs must be split into chunks and joined |
| 4 | stella_vslam | Only open method here that processes 360° video directly, which covers three of the six devices | Sparse map only. Must be combined with a dense method (rank 5) for a 3D model |
| 5 | DN-Splatter (on gsplat and Nerfstudio) | Turns camera positions from rank 1 to 4 into a dense indoor model, uses depth priors against holes on blank walls | Geometric accuracy of Gaussian splatting indoors is not established [refs. 7 and 8 in background document] |

Runner-ups: DROID-SLAM (robust, but no 360° support) and Depth Anything 3 (best models research only).

The five do not exclude each other. Ranks 1 to 4 deliver camera positions and a first model. Rank 5 can densify the output of any of them. This allows the experiments to answer which pose method gives the most accurate final model.

### 5.2 Detection: top 5

| Rank | Method | Why | Main risk |
|---|---|---|---|
| 1 | SAM 3 | Finds all instances of a text concept and tracks them through the video. Tracking supports counting unique assets (R1) | Performance on small wall-mounted assets unknown. Custom licence with restrictions |
| 2 | Grounding DINO with SAM 2 | Mature open-vocabulary alternative under Apache 2.0, many tutorials and integrations | Small objects and rare classes are a known weakness of open-vocabulary detectors |
| 3 | Own projection and clustering baseline | Needed for any 2D detector to give 3D positions (R2) and unique counts per room (R1). Simple and transparent | Depends on accurate camera positions. Must be implemented by the student |
| 4 | RF-DETR (fine-tuned) | Expected best accuracy once a small labelled set of the target assets exists. Apache 2.0 | Labelling effort. Only covers the trained asset types |
| 5 | SpatialLM | Gives room layout (walls, doors, windows) together with objects, which supports assigning assets to rooms. Already tested on point clouds from video | Research-only weights. Trained on furniture, not on building assets |

Runner-ups: OWLv2 (example-image prompts) and Qwen2.5-VL or Qwen3-VL (to verify uncertain detections).

## 6. Open points

1. **Licences:** all 30 are checked. Still open: the terms of the ScanNet-trained Mask3D weights, the full VGGT and SAM licence texts (read only the summaries and first lines), and whether RF-DETR's largest models have a different licence than the repository.
2. **No verbatim quotes were collected** from the primary sources, because the automated search stopped. Before citing a method in the background research document, open its paper and quote the sentence that supports the claim.
3. **Domain-specific literature is missing.** Papers and public datasets on detecting fire safety equipment and other building assets (for example on Roboflow Universe, Kaggle or Hugging Face) were not searched. They could provide labelled data for rank 4 of the detection list.
4. **Evaluation studies are missing.** Apart from refs. 7 and 8 of the background document, no study was collected that measures camera-only indoor reconstruction against a laser scan.
5. **Frame limits** of VGGT, MapAnything and Depth Anything 3 on a 24 GB GPU are not known. This decides how a building walkthrough must be split.
6. **Class coverage:** check whether the ScanNet200 classes (Mask3D) and the SpatialLM categories include any target assets.
7. **Commercial products:** Metashape (Linux, spherical cameras) and RealityScan (Windows only, revenue threshold) are checked. Postshot: supported operating systems not confirmed. The required internet connection should be raised with the stakeholders, because of R3.

## Appendix A. Methods found in the wide scan and not selected
Licences are only stated where they decided the exclusion. All entries are from memory unless marked.

| Method or product | Family | Reason for exclusion |
|---|---|---|
| OpenMVG | Photogrammetry | Older SfM library, COLMAP and OpenSfM cover the same role with more users |
| OpenMVS | Photogrammetry | Dense step only, COLMAP MVS already covered. AGPL licence |
| Meshroom and AliceVision | Photogrammetry | Similar to COLMAP, smaller user base in research |
| OpenDroneMap | Photogrammetry | Aimed at aerial images, uses OpenSfM internally |
| MicMac | Photogrammetry | Steep learning curve, aimed at expert surveying |
| Theia | Photogrammetry | No longer actively maintained |
| hloc with SuperPoint and LightGlue | Photogrammetry component | Improves matching inside COLMAP. Not a separate pipeline. SuperPoint weights are non-commercial |
| VGGSfM | Learned photogrammetry | Superseded by VGGT from the same group |
| MASt3R-SfM | Learned photogrammetry | Research-only licence. Covered by MASt3R-SLAM in the longlist |
| ACE0 | Learned photogrammetry | Research code, less tested on large indoor scenes |
| 3DF Zephyr | Commercial photogrammetry | Windows only. Metashape covers the role on Linux |
| Pix4D | Commercial photogrammetry | Aimed at drones, cloud or Windows workflows |
| Bentley iTwin Capture | Commercial photogrammetry | Enterprise product, Windows only |
| DSO and LDSO | SLAM | Sensitive to camera calibration and lighting changes, no dense model |
| VINS-Mono and VINS-Fusion | SLAM | Need motion sensor data, available for one device only |
| OpenVINS, Basalt, OKVIS2, Kimera | SLAM | Need motion sensor data |
| RTAB-Map | SLAM | Designed for depth or stereo cameras |
| SplaTAM | Splatting SLAM | Needs depth images |
| MonoGS | Splatting SLAM | Research licence (inherited from the original Gaussian splatting code) |
| Photo-SLAM | Splatting SLAM | Builds on ORB-SLAM3, research focus on rendering |
| GLORIE-SLAM, HI-SLAM2, Splat-SLAM | Splatting SLAM | Recent research code, licences mostly non-commercial, not checked |
| VGGT-SLAM and VGGT-Long | Feed-forward SLAM | Extensions of VGGT for long sequences. Considered as add-ons to VGGT, licences not checked |
| SLAM3R | Feed-forward SLAM | Builds on DUSt3R, research licence |
| DUSt3R | Feed-forward | Research-only licence, superseded by MASt3R and VGGT |
| MASt3R | Feed-forward | Research-only licence. Covered by MASt3R-SLAM |
| Spann3R, CUT3R, Fast3R, MUSt3R | Feed-forward | Recent research models, licences mostly non-commercial, not checked. VGGT and MapAnything cover the family |
| Pi3 | Feed-forward | Weights CC BY-NC 4.0 (checked) |
| MoGe-2 | Monocular depth | Single image only. Depth Anything 3 covers multi-view |
| UniDepth and UniK3D | Monocular depth | Single image only. Research licence (memory). UniK3D handles 360° and is worth a later look |
| Metric3D v2 | Monocular depth | Single image only |
| Depth Pro | Monocular depth | Single image only, Apple licence not checked |
| Original 3D Gaussian splatting | Splatting | Non-commercial licence. Same method available in gsplat under Apache 2.0 |
| 2DGS original code, PGSR, SuGaR, Gaussian Opacity Fields, MILo | Surface splatting | Built on the non-commercial original code. 2DGS is available in gsplat |
| Scaffold-GS, Mip-Splatting | Splatting | Improve rendering quality, not geometry |
| Brush, OpenSplat, LichtFeld Studio | Splatting tools | Alternative implementations. gsplat and Nerfstudio cover the role. OpenSplat AGPL, LichtFeld GPL |
| InstantSplat, CF-3DGS, NoPoSplat, AnySplat | Pose-free splatting | Build on research-only models or are aimed at few images |
| Neuralangelo | Neural surface | NVIDIA non-commercial licence, very long training |
| NeuS, NeuS2, MonoSDF, SDFStudio | Neural surface | Slower than splatting, superseded for indoor use by DN-Splatter style methods |
| Luma AI, Polycam, KIRI Engine, Scaniverse | Commercial apps | Cloud or phone processing, conflicts with R3, no accuracy statement |
| Teleport by Varjo, XGRIDS | Commercial splatting | Cloud or dedicated hardware |
| Matterport | Commercial platform | Cloud processing. Supports some 360° cameras |
| OpenSpace, Cupix, HoloBuilder, StructionSite, DroneDeploy 360 | Construction 360° walkthrough platforms | Cloud processing, aimed at progress photos rather than measured models |
| NavVis, Leica BLK2GO, XGRIDS Lixel | Mobile laser scanners | Need the vendor's laser scanner, conflicts with R4 |
| Prevu3D | Commercial platform | Works with laser scans and meshes, not with plain video |
| Apple RoomPlan | Device framework | Needs an iPhone or iPad with LiDAR |
| Google ARCore Depth API | Device framework | Phone-only live depth, not a reconstruction pipeline |
| Grounding DINO 1.5 and 1.6, DINO-X, T-Rex2 | Open-vocabulary detection | Available through a paid cloud API only |
| GLIP, Detic, OWL-ViT (v1) | Open-vocabulary detection | Superseded by Grounding DINO and OWLv2 |
| APE, OmDet-Turbo, LLMDet | Open-vocabulary detection | Less used, covered by the selected detectors. Licences not checked |
| RT-DETR, RT-DETRv2, D-FINE, DEIM | Closed-set detection | Similar role to RF-DETR |
| YOLOX, YOLO-NAS | Closed-set detection | Older or licence restrictions on weights (YOLO-NAS) |
| FastSAM, EfficientSAM, MobileSAM | Segmentation | Faster but less accurate versions of SAM. Speed is not critical offline |
| ByteTrack, BoT-SORT, DEVA, Cutie | Tracking | Components. SAM 3 and SAM 2 already track |
| PaliGemma 2, Molmo | Vision-language models | Similar role to Qwen-VL, licences not checked |
| Gemini, GPT vision | Vision-language models | Cloud only, conflicts with R3 |
| OpenScene, ConceptFusion | Open-vocabulary 3D maps | Aimed at semantic maps, not at object instances |
| ConceptGraphs, HOV-SG, BBQ, Clio | Open-vocabulary 3D maps | Need depth images from a depth sensor |
| Open3DIS, OpenIns3D, Any3DIS, MaskClustering, SAI3D, SAM3D (Yang et al.) | Open-vocabulary 3D instances | Similar to OpenMask3D. Most need depth images |
| LERF, LangSplat, LEGaussians, Feature 3DGS, Gaussian Grouping, OpenGaussian | Language-embedded splats | Search the splat by text, but are slow and mostly built on non-commercial code |
| SceneScript | Structured modelling | CC BY-NC licence, trained on synthetic homes, SpatialLM covers the role |
| RoomFormer | Structured modelling | Floor plans only, no objects |
| Cubify Anything | 3D detection | Apple research licence, trained on homes |
| OneFormer3D, SPFormer, ISBNet, SoftGroup | 3D instance segmentation | Fixed classes, need clean depth-sensor point clouds. OneFormer3D CC BY-NC |
| VoteNet, 3DETR, FCAF3D, TR3D, V-DETR | 3D detection | Fixed furniture classes, need depth-sensor point clouds |
| Point Transformer V3, Sonata (Pointcept) | Point cloud encoders | Building blocks, not detectors. Sonata weights CC BY-NC (checked via SpatialLM) |
| ImVoxelNet, NeRF-Det, MVSDet | 3D detection from posed images | Fixed furniture classes, research code |
| SAM 3D Objects | 3D generation | Generates the 3D shape of a single object from one image. Generated, not measured geometry |

Count: 30 methods in Sections 2 and 3, and about 65 methods or products in this appendix (some rows group several).

## References
Reference numbers in this document are local. "Ref. n in background document" refers to the reference list of the background research document. Author lists and venues of references marked (M) were written from memory and must be checked before use.

[1] J. L. Schönberger and J.-M. Frahm, "Structure-from-motion revisited," in *Proc. IEEE Conf. Comput. Vis. Pattern Recognit. (CVPR)*, 2016, pp. 4104-4113. (M)

[2] J. L. Schönberger, E. Zheng, J.-M. Frahm, and M. Pollefeys, "Pixelwise view selection for unstructured multi-view stereo," in *Proc. Eur. Conf. Comput. Vis. (ECCV)*, 2016, pp. 501-518. (M)

[3] L. Pan, D. Baráth, M. Pollefeys, and J. L. Schönberger, "Global structure-from-motion revisited," in *Proc. Eur. Conf. Comput. Vis. (ECCV)*, 2024. (M)

[4] Mapillary, "OpenSfM." GitHub. [Online]. Available: https://github.com/mapillary/OpenSfM

[5] Agisoft, "Agisoft Metashape." [Online]. Available: https://www.agisoft.com/

[6] Epic Games, "RealityScan." [Online]. Available: https://www.realityscan.com/

[7] S. Sumikura, M. Shibuya, and K. Sakurada, "OpenVSLAM: A versatile visual SLAM framework," in *Proc. 27th ACM Int. Conf. Multimedia*, 2019, pp. 2292-2295. Code: stella_vslam. Accessed: Nov. 16, 2026. [Online]. Available: https://github.com/stella-cv/stella_vslam

[8] C. Campos, R. Elvira, J. J. Gómez Rodríguez, J. M. M. Montiel, and J. D. Tardós, "ORB-SLAM3: An accurate open-source library for visual, visual-inertial, and multimap SLAM," *IEEE Trans. Robot.*, vol. 37, no. 6, pp. 1874-1890, 2021. (M)

[9] Z. Teed and J. Deng, "DROID-SLAM: Deep visual SLAM for monocular, stereo, and RGB-D cameras," in *Proc. Adv. Neural Inf. Process. Syst. (NeurIPS)*, 2021. (M)

[10] L. Lipson, Z. Teed, and J. Deng, "Deep patch visual SLAM," in *Proc. Eur. Conf. Comput. Vis. (ECCV)*, 2024. (M)

[11] R. Murai, E. Dexheimer, and A. J. Davison, "MASt3R-SLAM: Real-time dense SLAM with 3D reconstruction priors," in *Proc. IEEE/CVF Conf. Comput. Vis. Pattern Recognit. (CVPR)*, 2025. (M)

[12] J. Wang, M. Chen, N. Karaev, A. Vedaldi, C. Rupprecht, and D. Novotny, "VGGT: Visual geometry grounded transformer," in *Proc. IEEE/CVF Conf. Comput. Vis. Pattern Recognit. (CVPR)*, 2025. Commercial checkpoint: https://huggingface.co/facebook/VGGT-1B-Commercial (M for authors)

[13] N. Keetha *et al.*, "MapAnything: Universal feed-forward metric 3D reconstruction," arXiv:2509.13414, 2025. Commercial checkpoint: https://huggingface.co/facebook/map-anything-apache

[14] H. Lin *et al.*, "Depth Anything 3: Recovering the visual space from any views," arXiv preprint, 2025. Code: https://github.com/ByteDance-Seed/Depth-Anything-3 (M for title and authors)

[15] B. Kerbl, G. Kopanas, T. Leimkühler, and G. Drettakis, "3D Gaussian splatting for real-time radiance field rendering," *ACM Trans. Graph.*, vol. 42, no. 4, 2023. (M)

[16] V. Ye *et al.*, "gsplat: An open-source library for Gaussian splatting," *J. Mach. Learn. Res.*, vol. 26, 2025. Code: https://github.com/nerfstudio-project/gsplat (M)

[17] M. Tancik *et al.*, "Nerfstudio: A modular framework for neural radiance field development," in *Proc. ACM SIGGRAPH Conf.*, 2023. (M)

[18] B. Huang, Z. Yu, A. Chen, A. Geiger, and S. Gao, "2D Gaussian splatting for geometrically accurate radiance fields," in *Proc. ACM SIGGRAPH Conf.*, 2024. (M)

[19] M. Turkulainen, X. Ren, I. Melekhov, O. Seiskari, E. Rahtu, and J. Kannala, "DN-Splatter: Depth and normal priors for Gaussian splatting and meshing," in *Proc. IEEE/CVF Winter Conf. Appl. Comput. Vis. (WACV)*, 2025. (M)

[20] Q. Wu *et al.*, "3DGUT: Enabling distorted cameras and secondary rays in Gaussian splatting," in *Proc. IEEE/CVF Conf. Comput. Vis. Pattern Recognit. (CVPR)*, 2025. Code: https://github.com/nv-tlabs/3dgrut (M)

[21] Jawset, "Postshot." [Online]. Available: https://www.jawset.com/

[22] Insta360, "Insta360 and Splatica Gaussian splatting partnership." Accessed: Nov. 15, 2026. [Online]. Available: https://www.insta360.com/blog/enterprise/insta360-splatica-gaussian-splatting-partnership.html

[23] S. Liu *et al.*, "Grounding DINO: Marrying DINO with grounded pre-training for open-set object detection," in *Proc. Eur. Conf. Comput. Vis. (ECCV)*, 2024. (M)

[24] M. Minderer, A. Gritsenko, and N. Houlsby, "Scaling open-vocabulary object detection," in *Proc. Adv. Neural Inf. Process. Syst. (NeurIPS)*, 2023. (M)

[25] T. Cheng, L. Song, Y. Ge, W. Liu, X. Wang, and Y. Shan, "YOLO-World: Real-time open-vocabulary object detection," in *Proc. IEEE/CVF Conf. Comput. Vis. Pattern Recognit. (CVPR)*, 2024. (M)

[26] A. Wang *et al.*, "YOLOE: Real-time seeing anything," arXiv:2503.07465, 2025. (M)

[27] B. Xiao *et al.*, "Florence-2: Advancing a unified representation for a variety of vision tasks," in *Proc. IEEE/CVF Conf. Comput. Vis. Pattern Recognit. (CVPR)*, 2024. (M)

[28] S. Bai *et al.*, "Qwen2.5-VL technical report," arXiv:2502.13923, 2025. (M)

[29] N. Carion *et al.*, "SAM 3: Segment anything with concepts," arXiv:2511.16719, 2025. Code: https://github.com/facebookresearch/sam3 (M for authors)

[30] N. Ravi *et al.*, "SAM 2: Segment anything in images and videos," in *Proc. Int. Conf. Learn. Represent. (ICLR)*, 2025. (M)

[31] Roboflow, "RF-DETR." GitHub. [Online]. Available: https://github.com/roboflow/rf-detr

[32] Ultralytics, "Ultralytics YOLO." GitHub. [Online]. Available: https://github.com/ultralytics/ultralytics

[33] A. Takmaz, E. Fedele, R. W. Sumner, M. Pollefeys, F. Tombari, and F. Engelmann, "OpenMask3D: Open-vocabulary 3D instance segmentation," in *Proc. Adv. Neural Inf. Process. Syst. (NeurIPS)*, 2023. (M)

[34] M. E. A. Boudjoghra *et al.*, "Open-YOLO 3D: Towards fast and accurate open-vocabulary 3D instance segmentation," in *Proc. Int. Conf. Learn. Represent. (ICLR)*, 2025. (M)

[35] J. Schult, F. Engelmann, A. Hermans, O. Litany, S. Tang, and B. Leibe, "Mask3D: Mask transformer for 3D semantic instance segmentation," in *Proc. IEEE Int. Conf. Robot. Autom. (ICRA)*, 2023. (M)
