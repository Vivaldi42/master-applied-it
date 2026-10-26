# 3D Reconstruction for Building Maintenance
# Background Research 

Date: October 26th, 2026

## 1. Purpose and scope

Heijmans needs a reliable inventory of building assets, their locations and their condition. Existing information can be incomplete or outdated, leading to repeated inspections and manual data entry.

The stakeholder agreed that the first task is to investigate algorithms and software for 3D model generation. A 3D model is a firm deliverable. Later, the model could support asset information, condition records and updates.

## 2. Available hardware

A computer with the following specifications is available for research and development:

| Component | Specification |
|---|---|
| Operating system | Ubuntu 24.04.4 LTS |
| CPU | AMD Ryzen 9 7950X, 16 cores, 32 threads |
| RAM | Approximately 128 GB installed, 124 GiB reported usable |
| GPUs | Two NVIDIA RTX 4090 cards, each with approximately 24 GB VRAM |
| NVIDIA driver | 580.178.04 |
| Free storage | Approximately 42 GB on the project filesystem when checked |

Initial experiments should fit on one GPU. GPU memory does not automatically combine across cards. Storage requirements should be checked before downloading environments and datasets.

## 3. Different approaches

The tools discussed could solve different parts of the problem. They are not all direct alternatives.

| Approach | What it produces | Role in this project |
|---|---|---|
| Photogrammetry | Camera poses, point clouds and surface meshes from overlapping images | Reconstruct observed room geometry |
| Gaussian splatting | A scene represented by coloured 3D Gaussians for rendering different viewpoints | Visual inspection and reference |
| Semantic 3D mapping | Geometry associated with object categories and instances | Identify and locate individual assets |
| Scan-to-BIM | Structured building elements, often exported to IFC | Create editable building objects |
| AI-assisted procedural modelling | Geometry created through scripts or modelling operations | Assist model construction and correction |

A mesh or splat scene is not automatically a building information model. Objects still need to be separated, classified and linked to records. IFC is an open format for exchanging structured building information. MEP means mechanical, electrical and plumbing systems.

## 4. Reconstruction algorithms and software

Each entry links the original paper where available. Papers for underlying algorithms are labelled separately. Licences refer to code unless model weights are specified; dependencies may have separate terms.

### COLMAP

[Seed paper: Structure-from-Motion Revisited](https://openaccess.thecvf.com/content_cvpr_2016/html/Schonberger_Structure-From-Motion_Revisited_CVPR_2016_paper.html) | [Repository](https://github.com/colmap/colmap)

Estimates camera poses and reconstructs sparse and dense geometry from overlapping images using Structure from Motion and Multi-View Stereo. It is the proposed photogrammetry baseline; video requires frame extraction and room dimensions require scale validation. **Licence:** [BSD](https://colmap.github.io/license.html), with separate dependency terms.

### OpenMVS

[Underlying method: PatchMatch](https://gfx.cs.princeton.edu/pubs/Barnes_2009_PAR/) | [Repository](https://github.com/cdcseacave/openMVS)

Reconstructs dense point clouds and textured meshes from calibrated images and an initial reconstruction, including mesh refinement. It can follow COLMAP when a surface mesh is required. **Licence:** [AGPL-3.0](https://github.com/cdcseacave/openMVS/blob/develop/LICENSE).

### Simple Photogrammetry GUI

[Repository](https://github.com/edin45/simple_photogrammetry_gui)

Provides a graphical workflow around COLMAP and OpenMVS to produce textured OBJ meshes. It simplifies processing but does not identify building elements or assets. **Licence:** GPL-3.0 for the GUI, with separate licences for bundled tools.

### Nerfstudio, Splatfacto and gsplat

[Seed paper: 3D Gaussian Splatting](https://arxiv.org/abs/2308.04079) | [Nerfstudio paper](https://arxiv.org/abs/2302.04264) | [gsplat paper](https://arxiv.org/abs/2409.06765) | [Nerfstudio repository](https://github.com/nerfstudio-project/nerfstudio) | [gsplat repository](https://github.com/nerfstudio-project/gsplat)

Splatfacto trains a Gaussian scene representation inside Nerfstudio using gsplat for rendering and typically COLMAP for camera poses. It supports visual inspection and novel-view rendering, but its Gaussian PLY output is not a conventional mesh or structured asset model. **Licence:** Apache-2.0 for Nerfstudio and gsplat.

### VGGT

[Paper](https://arxiv.org/abs/2503.11651) | [Repository](https://github.com/facebookresearch/vggt)

Predicts camera parameters, depth maps and 3D points jointly from images, with export to COLMAP format. It is a candidate for estimating geometry and camera poses. **Licence:** [custom VGGT licence](https://github.com/facebookresearch/vggt/blob/main/LICENSE.txt); only the [commercial checkpoint](https://huggingface.co/facebook/VGGT-1B-Commercial) permits commercial use, subject to use restrictions including military and critical-infrastructure applications.

### Depth Anything V2

[Paper](https://arxiv.org/abs/2406.09414) | [Repository](https://github.com/DepthAnything/Depth-Anything-V2)

Estimates depth from individual images, with standard relative-depth models and separate metric-depth variants. Room reconstruction still requires camera poses, scale handling and fusion across frames. **Model licences:** Small uses Apache-2.0; Base, Large and Giant use CC BY-NC 4.0, so the exact checkpoint matters.

### Depth Anything 3

[Paper](https://arxiv.org/abs/2511.10647) | [Repository](https://github.com/ByteDance-Seed/Depth-Anything-3)

The multi-view models jointly estimate depth and camera poses; DA3-Base is a reconstruction candidate but does not directly provide metric scale. **Licences:** code, Small, Base, DA3Metric-Large and DA3Mono-Large use Apache-2.0; multi-view Large, Giant and Nested checkpoints use CC BY-NC 4.0. The Metric and Mono variants process individual images.

### LingBot-Map

[Paper](https://arxiv.org/abs/2604.14141) | [Repository](https://github.com/Robbyant/lingbot-map)

Reconstructs camera motion and dense geometry from streaming images using a Geometric Context Transformer with context and trajectory memory to limit drift. It matches the walkthrough-video use case, but produces geometry rather than labelled building objects. **Licence:** [code](https://github.com/Robbyant/lingbot-map/blob/main/LICENSE.txt) and [model weights](https://huggingface.co/robbyant/lingbot-map) use Apache-2.0.

### MASt3R-SLAM

[Paper](https://arxiv.org/abs/2412.12392) | [Repository](https://github.com/rmurai0610/MASt3R-SLAM)

Uses learned two-view reconstruction to estimate camera motion and dense geometry from monocular video, with loop closure and global optimisation to correct drift. It supports supplied or unknown camera calibration. **Licence:** [CC BY-NC-SA 4.0](https://github.com/rmurai0610/MASt3R-SLAM/blob/main/LICENSE.md), excluding commercial use; checkpoints have [additional terms](https://github.com/naver/mast3r/blob/mast3r_sfm/CHECKPOINTS_NOTICE).

## 5. Structured building models and asset mapping

### Cloud2BIM

[Paper](https://doi.org/10.1016/j.autcon.2025.106303) | [Repository](https://github.com/VaclavNezerka/Cloud2BIM)

Converts point clouds into parametric slabs, walls, doors and windows with IFC output using point-density analysis and image operations. Compatibility with smartphone-derived geometry remains untested; the public implementation differs from the separate commercial product. **Licence:** [MIT](https://github.com/VaclavNezerka/Cloud2BIM/blob/master/LICENSE).

### ConceptGraphs

[Paper](https://arxiv.org/abs/2309.16650) | [Repository](https://github.com/concept-graphs/concept-graphs)

Combines segmentation and visual features with posed RGB-D images to build object-based 3D maps and scene graphs. It could support asset identification, but ordinary phone video needs depth and camera poses supplied separately. **Licence:** [MIT](https://github.com/concept-graphs/concept-graphs/blob/main/LICENSE) for the code; external models and dependencies require separate checks.

### Bonsai and IfcOpenShell

[Repository](https://github.com/IfcOpenShell/IfcOpenShell) | [Documentation](https://docs.ifcopenshell.org/bonsai.html)

Bonsai provides a Blender interface for authoring and editing IFC models, while IfcOpenShell provides APIs for IFC geometry and properties. They can support inspection and correction after reconstruction, but do not reconstruct a building from video. **Licences:** Bonsai uses GPL-3.0-or-later; the IfcOpenShell libraries use LGPL-3.0-or-later, with component-specific exceptions documented in the repository.

### RelateAnything

[Paper](https://arxiv.org/abs/2609.12552) | [Repository](https://github.com/Maelic/RelateAnything)

Predicts relationships between supplied object regions in an image using a relation vocabulary chosen at inference time. It could describe asset relationships, but does not detect the regions or reconstruct geometry. **Licence:** [AGPL-3.0](https://github.com/Maelic/RelateAnything/blob/main/LICENSE) for the current code; model and backbone terms require separate verification.

## 6. AI-assisted modelling and other examples

### Astra with Blender

[Official demonstration](https://developers.openai.com/blog/architectural-visualization-with-astra) | [Model documentation](https://developers.openai.com/api/docs/models/gpt-6-astra)

Astra creates and revises editable scenes through Blender's Python API, using rendered views for inspection. The demonstration models a design brief rather than reconstructing a measured room. **Licence:** Astra is a hosted proprietary model with service terms; Blender is [GPL-licensed](https://www.blender.org/about/license/).

### World Labs Atlas

[Official announcement](https://www.worldlabs.ai/blog/atlas)

Combines spatial reconstruction and generation from images, including camera-controlled views and explicit 3D outputs. It can invent unseen content, so generated details are not evidence of real assets.

### LichtFeld Studio

[Underlying method: 3D Gaussian Splatting](https://arxiv.org/abs/2308.04079) | [Repository](https://github.com/MrNeRF/LichtFeld-Studio)

Provides local Gaussian splat training, editing and rendering on Windows and Linux, with Python plugins and MCP automation. It supports visual scene inspection but does not directly produce structured building assets. **Licence:** GPLv3, as stated on the [official site](https://lichtfeld.io/).

### 360 Gaussian Pro

[Underlying method: 3D Gaussian Splatting](https://arxiv.org/abs/2308.04079) | Public repository: not identified | [Official site](https://www.360gaussianpro.com/)

Provides a local Windows workflow for video frame extraction, masking, COLMAP alignment and integration with splat trainers. It accepts ordinary and 360-degree video but is a weaker fit for the Ubuntu workstation. **Licence:** paid commercial application with a limited trial; no open-source licence identified and bundled model restrictions apply.

### SIGReg / LeJEPA

[Seed paper: LeJEPA](https://arxiv.org/abs/2511.08544) | [Repository](https://github.com/galilai-group/lejepa)

SIGReg regularises learned embeddings towards an isotropic Gaussian distribution to prevent representation collapse during self-supervised training. It is relevant to training representation models, rather than directly reconstructing rooms. **Licence:** [CC BY-NC 4.0](https://github.com/galilai-group/lejepa/blob/main/LICENSE) for the reference implementation.

### 4DAnyone

[Paper](https://arxiv.org/abs/2608.20335) | [Repository](https://github.com/ant-research/4DAnyone)

Generates consistent multi-view videos from monocular footage for downstream 4D Gaussian reconstruction. It targets dynamic subjects and is lower priority for a static building inventory. **Licence:** [Apache-2.0](https://github.com/ant-research/4DAnyone/blob/main/LICENSE) for the code; model weights and dependencies require separate checks.

Additional discovery sources: [rendering integration directory](https://radiancefields.com/3d-gaussian-splatting-engine-support) and [supplied video](https://www.youtube.com/watch?v=pZb6n8diMrc). These are research leads rather than reconstruction methods; individual claims require primary-source verification.
