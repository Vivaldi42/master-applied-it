# Background Research (Draft)

Verification tags:
- [n, Sec. x]: claim from reference n. Verbatim quotes for the Introduction claims are in background-research-document.md.
- [PA, Sec. x]: claim from problem-analysis.md.
- [TODO: source]: claim not yet supported by a source that was read. Verify or remove.
- No tag: a decision of this project, not a factual claim.

## 1. Introduction

### 1.1 Domain
Building maintenance requires detailed data on installed components and equipment, including their geometry and exact location [1, Sec. 1]. In many existing buildings, however, this information is incomplete, obsolete, or fragmented [1, Sec. 1]. Building information models (BIM) can store such data, but the majority of existing buildings are not maintained with BIM [1]. Creating a model of an existing building from captured data, known as scan-to-BIM, is costly and mainly manual [1, Sec. 2], and it remains time-consuming and resource-intensive [2].

Laser scanners are one of the most used tools to capture 3D features of buildings [3, Sec. 2.2.2]. Cameras are cheap and easy to use, but photogrammetry has traditionally been less accurate than laser scanning [3, Sec. 2.2.2]. Technological advances of recent years may have reduced this difference [TODO: source].

### 1.2 Problem
Heijmans maintains large buildings, such as offices, hospitals, educational institutions, and airports, under fixed-term contracts [PA, Sec. 1]. Most of these buildings are older than 5 to 10 years and have no BIM [PA, Sec. 1]. At the start of a contract, the previous maintainer hands over an asset list, usually an Excel sheet and sometimes annotated floor plans [PA, Sec. 2]. These records are frequently incomplete or outdated [PA, Sec. 4]. Heijmans therefore performs an inventory inspection, in which an inspector records every asset and assesses its condition according to NEN 2767 [PA, Sec. 3], [4]. The inspection takes days to weeks and is monotonous [PA, Sec. 4]. Current mitigations, such as combining data sources and augmented reality, are limited when no BIM model is available [PA, Sec. 5].

### 1.3 Goal and research questions
In this project, a person walks through a building with an AI wearable to collect data [PA, Sec. 6]. The collected data is converted into a 3D model of the building that contains its assets, and an asset list is extracted from the model [PA, Sec. 6]. The stakeholders require a location accuracy of 10 to 15 cm for the 3D model and the floor and room of each asset for the asset list [PA, Sec. 6]. Processing on Heijmans' own servers is preferred [PA, Sec. 7.2].

To compare methods for this purpose, suitable evaluation criteria are needed. No standard method has been established to compare the quality of building models [1, Sec. 4.3.4], and representative benchmark datasets are lacking [3, Sec. 3.5], [2, Sec. 4].

This leads to the main research question: How can a 3D model of indoor space be developed to support building inventory inspection based on visual input? The subquestions are:
1. Which metrics evaluate methods for generating a 3D model?
2. What methods exist and how do they compare on these metrics in literature?
3. How do the selected methods perform in experiments and which factors affect the results?
4. (Possibly later) How can assets of one type and their condition be identified in the 3D model?

## 2. Background and Related Work

### 2.1 Concepts and definitions
A point cloud is a set of points, each with x, y, and z coordinates and optional attributes such as intensity or RGB colour [3, Sec. 2.2.1]. A mesh represents a surface as connected polygons [TODO: source]. Gaussian splatting represents a scene as a set of 3D Gaussians that can be rendered from new viewpoints [TODO: source].

BIM is defined as a "shared digital representation of physical and functional characteristics of any built object" [1, Sec. 2]. A BIM consists of parametric objects that represent building components [1, Sec. 2]. These objects can have geometric attributes and non-geometric attributes, such as functional, semantic, or topologic information [1, Sec. 2]. Industry Foundation Classes (IFC) is the dominant non-proprietary format to exchange building information between software [1, Sec. 4.2.3], [3, Sec. 1.2.1].

This document distinguishes geometry (shape and position) from semantics (which object or class a part of the model represents).

### 2.2 Reconstruction pipeline
Creating a BIM of an existing building from captured data consists of data capture, data processing, object recognition, and modelling [1, Sec. 4.3]. A similar procedure is described for laser scanning: data acquisition, preprocessing, and modelling [3, Sec. 2]. For camera input, camera poses must be estimated before geometry can be reconstructed [TODO: source].

### 2.3 Method families
- Photogrammetry: structure from motion (SfM) estimates camera poses and sparse geometry from overlapping images. Multi-view stereo (MVS) computes dense geometry from the posed images [TODO: source].
- Robotics: simultaneous localisation and mapping (SLAM) estimates the sensor trajectory and a map at the same time [TODO: source]. Indoor mobile laser scanners, carried by hand or as a backpack, are usually SLAM-based and do not require satellite positioning [3, Sec. 2.4.2]. Semantic mapping adds object classes to the map [TODO: source].
- Neural and learning-based methods: Gaussian splatting [TODO: source] and feed-forward reconstruction models [TODO: source].

History: [TODO: source]. Development from photogrammetry and laser scanning to SLAM to learning-based methods.

### 2.4 Robotics assumptions vs. building inspection
Robotics methods typically assume [TODO: source]. In this project, a person carries a wearable camera through buildings with long corridors, glass, and repetitive rooms. Sensor fusion methods from robotics that model sensor uncertainty explicitly are not yet common in the construction domain [3, Sec. 3.1]. Which assumptions remain valid in this setting is an open question.

### 2.5 Research gap
Image-based reconstruction with recent methods has not been evaluated against the requirements of building inventory inspection [TODO: source; claim from this project]. In addition, no standard method exists to compare model quality [1, Sec. 4.3.4], and benchmark datasets are lacking [3, Sec. 3.5].

## 3. Relevant Results from Other Papers
Recognition of coarse planar components (walls, ceilings, floors, doors, windows) in small scenes of single or few rooms reaches recognition rates between 89% and 93% [1, Sec. 4.3.3]. Detailed technical equipment is not yet recognized automatically and requires intense user input [1, Sec. 4.3.3]. For maintenance applications, a geometric deviation of 2% has been defined by Klein *et al.*, as reported in [1, Sec. 4.1.2].

Reported accuracy and completeness of each method family on indoor scenes: [TODO: source].

Factors known to cause failures:
- Laser scanning: reflective, transparent, and dark surfaces [1, Sec. 4.3.1].
- Photogrammetry: surfaces with low features and windows [3, Sec. 2.2.2].
- Indoor scenes: more complex geometry and more clutter than outdoor scenes [3, Sec. 2.4.2].

## 4. Inspiring Methodologies from Other Papers
Point cloud quality can be assessed by accuracy, precision, point density, and resolution [3, Sec. 2.2.1]. Completeness, accuracy, resolution, and registrability have also been used as data quality criteria, as reported in [3, Sec. 2.2.4]. For semantic segmentation in scan-to-BIM, the most used metrics are accuracy, precision, recall, F1-score, and intersection over union (IoU) [2, Sec. 4].

The ISPRS benchmark on indoor modelling provided a public dataset and an evaluation framework, but the dataset became inaccessible after the results were published in 2021 [3, Sec. 3.5].

Ground truth: [TODO: source].

Research design: DOT framework [TODO: source].

## 5. Conclusion
Existing buildings often lack reliable asset data and BIM, and creating models of them is mainly manual. Camera-based reconstruction is a low-cost option, but its suitability for inventory inspection has not been evaluated. No standard evaluation method or benchmark exists. SQ1 defines the metrics, SQ2 compares methods in literature, SQ3 tests selected methods in experiments, and SQ4 optionally addresses asset identification.

## References
[1] R. Volk, J. Stengel, and F. Schultmann, "Building information modeling (BIM) for existing buildings: Literature review and future needs," *Automation in Construction*, vol. 38, pp. 109-127, 2014, doi: 10.1016/j.autcon.2013.10.023.

[2] N. Montás-Laracuente *et al.*, "A systematic review of artificial intelligence for capturing real-world structures into building information modelling," *Journal of Building Engineering*, vol. 113, Art. no. 114093, 2025, doi: 10.1016/j.jobe.2025.114093.

[3] N. Abreu, A. Pinto, A. Matos, and M. Pires, "Procedural point cloud modelling in scan-to-BIM and scan-vs-BIM applications: A review," *ISPRS International Journal of Geo-Information*, vol. 12, no. 7, Art. no. 260, 2023, doi: 10.3390/ijgi12070260.

[4] *Conditiemeting gebouwde omgeving - Deel 1: Methodiek*, NEN 2767-1+C1:2019, NEN, Delft, The Netherlands, 2019.
