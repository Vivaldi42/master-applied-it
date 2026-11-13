# Raychaudhuri and Chang (2025): Semantic Mapping in Indoor Embodied AI

S. Raychaudhuri and A. X. Chang, "Semantic mapping in indoor embodied AI: A survey on advances, challenges, and future directions," *Transactions on Machine Learning Research*, 2025. arXiv: 2501.05750v3.

## Summary related to my research

The paper is a survey, not an experimental comparison. It categorizes methods that build semantic maps of indoor spaces, i.e. maps that store what objects are where, in addition to geometry. The context is robots and virtual agents that navigate, mostly in simulation. Its two categorization dimensions are map structure and map encoding. For the project it provides: 
- the stages of building a semantic map (pipeline)
- the trend towards open-vocabulary maps (asset recognition without a fixed class list)
- a set of evaluation dimensions for maps.

## Key points

### 1. Pipeline: how a semantic map is built
- Map building consists of localization (where the camera is), feature extraction (semantic information per observation), projection (2D pixels to 3D using depth and camera pose) and accumulation (merging observations over time) (Sec. 3.4, Fig. 5, p. 11-12).
- A SLAM system consists of a front-end (feature extraction, data association, loop closure) and a back-end (pose optimization and map estimation) (Sec. 2.2.2). There exist visual SLAM or vSLAM (RGB camera) and RGB-D (depth camera) SLAM and Visual-Inertial SLAM (camera and IMU).

### 2. Map structure and encoding
<!-- - Map structures: spatial grid, topological graph (objects as nodes, relations as edges), dense geometric (e.g. point cloud) and hybrid (Sec. 3.2). -->
<!-- - Encodings: explicit (e.g. an object class per location) or implicit (features from a pre-trained encoder). Implicit features are closed-vocabulary (fixed set of classes) or open-vocabulary (in theory any object) (Sec. 3.3). -->
- Trend: the field moves towards open-vocabulary, queryable, task-agnostic maps. Open challenges are memory demand and computational cost (Abstract).

### 3. Evaluation (input for SQ1)
- Extrinsic evaluation measures performance on the downstream task. Intrinsic evaluation measures the map itself. Most works use only extrinsic evaluation (Sec. 6).
- Intrinsic dimensions: accuracy, completeness (geometric and semantic coverage), consistency (e.g. ATE, RMSE against ground truth) and robustness (Sec. 6.2, Tab. 7).
- "There is no widely agreed-upon metric suite for evaluating the map representation itself" (Sec. 6.2). Semantic completeness is rarely quantified because detailed ground-truth semantic maps are lacking (Sec. 6.2, "Completeness").
- For classification and detection tasks, precision, recall and F1 are used (Sec. 6.1).

## Limitations for this project

- Embodied AI research often assumes perfect localization or perfect actuation (Sec. 3.4, "Localization"). A person with a wearable camera has neither.
- Simulated agents have no drift, so geometric consistency is rarely reported (Sec. 6.2, "Consistency"). In this project, drift is expected.
- The survey focuses on map building for indoor navigation (Abstract), not on inventory or inspection tasks.
- This project builds the map offline (capture first, process afterwards). The survey mainly covers online map building during a task (Sec. 3.4, "Online vs offline").

## Use in the background research document

- Sec. 2 (Reconstruction pipeline): pipeline stages (Key points 1).
- Sec. 3 (Method families): map structures and open-vocabulary encodings (Key points 2).
- Sec. 4 (Robotics assumptions vs. building inspection): Limitations.
- Inspiring methodologies / SQ1: evaluation dimensions and the missing standard metric suite (Key points 3).
