# Research into 3D reconstruction for building maintenance

Research date: 17 September 2026

## 1. Purpose and scope

Heijmans needs a reliable inventory of building assets, their locations and their condition. Existing information can be incomplete or outdated, leading to repeated inspections and manual data entry.

The stakeholder agreed that the first task is to investigate algorithms and software for 3D model generation. A 3D model is a firm deliverable. The desired output contains individually selectable building elements and assets. Geometric accuracy matters more than photorealistic appearance. Later, the model should support asset information, condition records and updates.

The first experiment will cover one room using Samsung Galaxy S25 video. We will initially work with ordinary RGB video, without requiring a separate depth recording. The first model can be static, but the system should allow manual corrections and updates from later captures.

Preferred software should run locally, provide source code that can be modified, and permit commercial use. Its output should retain useful geometry and links to the original observations.

This document records an initial software and research review. No reconstruction software has been installed, forked or benchmarked during this investigation. Documented capabilities have not yet been independently validated on our data.

## 2. Available hardware

Read-only checks identified the following workstation:

| Component | Specification |
|---|---|
| Operating system | Ubuntu 24.04.4 LTS |
| CPU | AMD Ryzen 9 7950X, 16 cores and 32 threads |
| RAM | Approximately 128 GB installed, 124 GiB reported usable |
| GPUs | Two NVIDIA RTX 4090 cards, each with approximately 24 GB VRAM |
| NVIDIA driver | 580.178.04 |
| Free storage | Approximately 42 GB on the project filesystem when checked |

Initial experiments should fit on one GPU. GPU memory does not automatically combine across cards. Storage requirements should be checked before downloading environments and datasets. Existing data should not be deleted to make room without agreement.

## 3. Different approaches

The tools discussed solve different parts of the problem. They are not all direct alternatives.

| Approach | What it produces | Role in this project |
|---|---|---|
| Photogrammetry | Camera poses, point clouds and surface meshes from overlapping images | Reconstruct observed room geometry |
| Gaussian splatting | A scene represented by coloured 3D Gaussians for rendering different viewpoints | Visual inspection and reference |
| Semantic 3D mapping | Geometry associated with object categories and instances | Identify and locate individual assets |
| Scan-to-BIM | Structured building elements, often exported to IFC | Create editable building objects |
| AI-assisted procedural modelling | Geometry created through scripts or modelling operations | Assist model construction and correction |

A mesh or splat scene is not automatically a building information model. Objects still need to be separated, classified and linked to records. IFC is an open format for exchanging structured building information. MEP means mechanical, electrical and plumbing systems.

## 4. Reconstruction algorithms and software

### COLMAP

Links: [repository](https://github.com/colmap/colmap), [tutorial](https://colmap.github.io/tutorial.html), [licence](https://colmap.github.io/license.html).

COLMAP implements Structure from Motion and Multi-View Stereo. It estimates camera positions from overlapping images, generates a sparse reconstruction and can then produce dense geometry. Video must first be converted into selected frames.

It is a useful baseline because camera poses and geometry can support later asset mapping. Its core uses a BSD licence. The official documentation states that third-party dependencies can affect the licence of the resulting build.

The main experimental questions are completeness and accuracy inside rooms. Low-texture walls, reflections, occlusions and capture quality need attention. A sparse point cloud alone should not be assumed sufficient for Scan-to-BIM.

### OpenMVS

Link: [repository](https://github.com/cdcseacave/openMVS).

OpenMVS provides dense reconstruction, mesh reconstruction, refinement and texturing from calibrated images and an initial reconstruction. It can follow COLMAP when a surface mesh is required.

The repository uses AGPL-3.0. Commercial use is possible, but obligations concerning distribution and network access to modified versions require consideration. It should not be treated as equivalent to a permissive MIT or BSD dependency.

### Simple Photogrammetry GUI

Link: [repository](https://github.com/edin45/simple_photogrammetry_gui).

This application provides a graphical workflow around tools including COLMAP and OpenMVS. Its documented photogrammetry output is a textured OBJ mesh. Linux packaging is available, although parts of the build documentation are described as experimental.

It could simplify the first experiment, but its mesh still needs to be divided into meaningful building elements and assets. The GUI uses GPL-3.0 and includes separately licensed external software. Compatibility with this workstation has not been tested.

### Nerfstudio, Splatfacto and gsplat

Links: [Nerfstudio](https://github.com/nerfstudio-project/nerfstudio), [Splatfacto documentation](https://docs.nerf.studio/nerfology/methods/splat.html), [gsplat](https://github.com/nerfstudio-project/gsplat).

Nerfstudio is a framework for training and inspecting scene representations. Splatfacto is its Gaussian splatting implementation, using gsplat as the rendering backend. The ordinary video workflow uses COLMAP to obtain camera poses and initial points.

Splatfacto optimises a collection of 3D Gaussians against the input images. The documentation lists approximate memory requirements of 6 GB for the default model and 12 GB for a larger variant. Actual requirements depend on the scene and settings. The documented export is Gaussian PLY, not a conventional surface mesh.

Nerfstudio and gsplat use Apache-2.0 licences. These permit commercial use under their terms, but other pipeline dependencies still need checking.

This was the initial recommendation before the required output was clarified. Because editable objects matter more than photorealism, it is now better considered as a comparison method or visual reference. Asset recognition, persistent identities and condition records require additional development.

### VGGT

Links: [repository](https://github.com/facebookresearch/vggt), [licence](https://github.com/facebookresearch/vggt/blob/main/LICENSE.txt), [commercial checkpoint](https://huggingface.co/facebook/VGGT-1B-Commercial).

VGGT predicts camera parameters, depth maps and 3D points from images. It can export results in COLMAP format, making it a candidate for the geometry and camera-estimation stage.

It supports local inference, but the number of input frames is constrained by GPU memory. Its speed and accuracy on our room remain untested.

Only the designated commercial checkpoint permits commercial use. The original checkpoint remains non-commercial. The custom licence includes restrictions beyond military applications, including provisions concerning critical infrastructure. Suitability for the eventual deployment context requires review. VGGT is therefore a conditional research candidate.

### Depth Anything V2

Links: [repository and model licences](https://github.com/DepthAnything/Depth-Anything-V2), [paper](https://arxiv.org/abs/2406.09414).

Depth Anything V2 estimates depth from individual images. Its standard models predict relative depth; separate metric-depth variants are also documented. A depth map alone does not provide a coherent room reconstruction. Camera poses, scale handling and fusion across frames are still required.

The standard Small model uses Apache-2.0, while Base, Large and Giant use CC BY-NC 4.0 and do not meet our commercial-use requirement. The exact checkpoint matters, including when considering metric-depth variants.

V2 is relevant as a depth-estimation component, but is not the first choice for a complete reconstruction pipeline. Predicted depth must be validated against measurements rather than treated as sensor ground truth.

### Depth Anything 3

Links: [repository and model table](https://github.com/ByteDance-Seed/Depth-Anything-3), [paper](https://arxiv.org/abs/2511.10647).

Depth Anything 3 includes multi-view models that estimate depth and camera poses from multiple images. This makes the multi-view variants more directly relevant to room reconstruction than standalone single-image depth estimation.

The documented model licences differ:

| Model | Capability | Licence |
|---|---|---|
| DA3-Small and DA3-Base | Multi-view relative depth and camera poses | Apache-2.0 |
| DA3-Large, Giant and Nested variants | Larger multi-view models with capabilities varying by checkpoint | CC BY-NC 4.0 |
| DA3Metric-Large | Single-image metric depth | Apache-2.0 |
| DA3Mono-Large | Single-image relative depth | Apache-2.0 |

DA3-Base is a candidate for the first comparison because it combines multi-view geometry with a commercially permissive model licence. Metric depth is not a feature of this checkpoint. Scale needs to be established and checked separately. The metric model also requires appropriate camera focal information for conversion to metres, as described in the documentation.

The software supports local execution. Memory consumption depends on the number and resolution of images, so operation on one RTX 4090 must be measured. Its output still requires object identification and conversion before it becomes a structured asset model.

### LingBot-Map

Links: [repository](https://github.com/Robbyant/lingbot-map), [paper](https://arxiv.org/abs/2604.14141), [code licence](https://github.com/Robbyant/lingbot-map/blob/main/LICENSE.txt), [model card](https://huggingface.co/robbyant/lingbot-map).

LingBot-Map performs streaming 3D reconstruction from image sequences or video. Its Geometric Context Transformer combines an anchor context, a pose-reference window and trajectory memory to estimate geometry and camera motion while reducing accumulated drift.

The authors report approximately 20 FPS at 518 by 378 resolution and demonstrate long walkthroughs. These are reported results, not measurements on our workstation. The repository documents CPU offloading, keyframe selection and windowed inference to control memory use and handle longer sequences.

The code and model card specify Apache-2.0. Selected dependencies and optional rendering components still need checking. Local execution makes it a relevant candidate for the Galaxy S25 walkthrough experiment, with actual GPU memory requirements to be tested.

LingBot-Map produces geometric reconstruction rather than labelled BIM objects. Streaming within one capture does not automatically solve updates across separate visits, persistent asset identity or preservation of manual corrections.

### MASt3R-SLAM

Links: [project page](https://edexheim.github.io/mast3r-slam/), [repository](https://github.com/rmurai0610/MASt3R-SLAM), [code licence](https://github.com/rmurai0610/MASt3R-SLAM/blob/main/LICENSE.md), [checkpoint notice](https://github.com/naver/mast3r/blob/mast3r_sfm/CHECKPOINTS_NOTICE).

MASt3R-SLAM uses learned two-view reconstruction and matching to estimate camera motion and dense geometry from monocular video. It combines local fusion with loop closure and global optimisation. Loop closure recognises revisited locations and helps correct accumulated drift. The system can work without supplied camera calibration, while also supporting known calibration.

The authors report approximately 15 FPS and state that their experiments used an RTX 4090, primarily on Ubuntu. This makes the published hardware setup directly relevant to our workstation, although performance on our recording remains untested.

The code uses CC BY-NC-SA 4.0, which excludes commercial use under the published licence. Separate permission would be needed for commercial deployment, alongside suitable rights for dependencies and checkpoints. It is useful for the literature comparison, but does not meet the current implementation requirement. Its geometry would also need additional processing to create identifiable assets and condition records.

## 5. Structured building models and asset mapping

### Cloud2BIM

Links: [original repository](https://github.com/VaclavNezerka/Cloud2BIM), [paper](https://doi.org/10.1016/j.autcon.2025.106303), [MIT licence](https://github.com/VaclavNezerka/Cloud2BIM/blob/master/LICENSE).

Cloud2BIM converts point clouds into parametric building elements and IFC output. It uses point-density analysis together with image and morphological operations to extract elements such as slabs, walls, doors and windows.

The public research implementation runs through Python scripts and uses an MIT licence. The authors distinguish it from a separate commercial product with additional capabilities. Those capabilities should not be attributed to the public repository.

Cloud2BIM is relevant to the building structure, but is not a complete maintenance-asset recognition system. We have not established whether smartphone-derived point clouds will satisfy its input assumptions or provide enough coverage. Connecting COLMAP to Cloud2BIM is a proposed experiment, not a validated pipeline.

### ConceptGraphs

Links: [repository](https://github.com/concept-graphs/concept-graphs), [paper](https://arxiv.org/abs/2309.16650).

ConceptGraphs builds object-based 3D maps and scene graphs. It combines image segmentation and visual features with depth and camera poses to associate observations with objects in 3D. Scene graphs describe relationships between objects.

Its documented input is posed RGB-D imagery. Ordinary phone video does not directly supply all these inputs, so depth and poses must be obtained separately. The repository uses multiple external models and includes language-model stages.

It is relevant to later asset identification, but does not directly produce a complete IFC building model. Code, dependency and model-weight licences require further checking. Fully local operation must be assessed for the chosen configuration.

### Bonsai and IfcOpenShell

Links: [Bonsai](https://bonsaibim.org/), [documentation](https://docs.ifcopenshell.org/bonsai.html), [IfcOpenShell](https://github.com/IfcOpenShell/IfcOpenShell), [geometry creation API](https://docs.ifcopenshell.org/ifcopenshell-python/geometry_creation.html).

Bonsai provides a Blender-based interface for creating, inspecting and editing IFC models. IfcOpenShell provides libraries and APIs for working with IFC geometry and information. The ecosystem includes building elements, MEP and facility-management workflows.

These tools could provide the authoring and inspection environment for the structured result. They do not automatically reconstruct a building from video. Recognition and conversion from captured geometry remain separate tasks.

The ecosystem contains differently licensed components, including GPL and LGPL. Exact component licences should be recorded before integration or distribution. Asset condition history and update behaviour still need to be designed for this application.

### RelateAnything

Link: [repository](https://github.com/Maelic/RelateAnything).

RelateAnything takes an image and supplied regions, such as bounding boxes or masks, and predicts relationships between pairs of regions. The relation vocabulary can be specified at inference time.

It could support descriptions of how assets relate to their surroundings. It does not reconstruct geometry or replace the detector that supplies object regions. Its usefulness for maintenance-specific relationships is untested.

The repository identifies its code as Apache-2.0. Model-weight and backbone terms still require verification. This is a possible later extension.

## 6. AI-assisted modelling and other examples

### Astra with Blender

Links: [architectural modelling example](https://developers.openai.com/blog/architectural-visualization-with-astra), [model documentation](https://developers.openai.com/api/docs/models/gpt-6-astra).

OpenAI demonstrates Astra creating an editable architectural scene through Blender's Python API, then inspecting and refining rendered results. This supports considering Astra for scripting, model construction and correction.

The demonstration starts from a design brief. It does not establish accurate reconstruction of an existing room from video. For this project, modelling operations should be constrained by captured geometry and checked against the real room.

Astra can assist with local tools, but it is not established here as a locally runnable, open-weight model. Using it introduces a hosted-model dependency. A fully local reconstruction workflow should be able to operate independently of it.

### World Labs Atlas

Link: [official announcement](https://www.worldlabs.ai/blog/atlas).

Atlas combines spatial generation and reconstruction from images. The announcement describes camera-controlled outputs and improved fidelity when more observations are supplied.

The same source states that unseen areas can be filled with plausible generated content. Such additions cannot be treated as evidence that an asset exists. Reconstruction claims need quantitative testing for our use case.

Local availability, source-code access and commercial deployment terms were not established in this review. Atlas remains a comparison candidate rather than a selected implementation.

### LichtFeld Studio

Link: [official website](https://lichtfeld.io/).

LichtFeld Studio provides local Gaussian splat training, editing and rendering, with Windows and Linux support. It offers Python plugins and MCP automation. The site identifies GPLv3 as its licence.

It could support visual reconstruction comparisons and scene inspection. Selecting and editing splats does not automatically create persistent building assets or condition records. GPL licensing permits commercial use, but redistribution obligations require consideration.

### 360 Gaussian Pro

Link: [official website](https://www.360gaussianpro.com/).

360 Gaussian Pro provides a local workflow for frame extraction, masking, alignment and integration with splat trainers. It accepts ordinary video as well as 360-degree footage. Alignment produces camera poses and a sparse COLMAP point cloud.

The documented application is Windows-based and paid beyond a limited trial. The website permits commercial use of results subject to stated model restrictions. An open-source version suitable for forking was not established.

It is a useful workflow reference, but a weaker fit for the Ubuntu workstation and preference for modifiable software. It does not directly deliver structured building objects.

### SIGReg

Link: [LeJEPA paper](https://arxiv.org/abs/2511.08544).

If the intended term is Sketched Isotropic Gaussian Regularization from LeJEPA, SIGReg is a training objective that constrains learned representations and helps prevent their collapse. It is not a ready-to-use reconstruction algorithm. It would become relevant if the project involved developing or training representation models.

### News, rendering integrations and 4D methods

Discovery links: [integration directory](https://radiancefields.com/3d-gaussian-splatting-engine-support), [supplied video](https://www.youtube.com/watch?v=pZb6n8diMrc), [4DAnyone](https://github.com/ant-research/4DAnyone).

The supplied video description mentions Atlas, XGRIDS, COLMAP, phone reconstruction and 4D methods. These are research leads. The video itself was inaccessible during the review and its individual performance claims were not verified.

The directory can help identify viewers and plugins. Engine support does not establish geometric accuracy, object recognition or asset-management capability. Individual integrations need verification against primary documentation.

Time-varying 4D reconstruction is lower priority for the static-room experiment. Maintaining an inventory across inspections is a separate requirement from reconstructing continuous motion.

## 7. Preparing for future updates

The first prototype should generate a static model, with the following requirements retained for later development:

- Persistent asset IDs independent of mesh indices and scan files.
- Asset properties and condition history linked to those IDs.
- Individual objects that can be corrected, replaced, added or removed.
- Manual corrections preserved unless a reviewer accepts their replacement.
- Later captures aligned to the same coordinate system.
- Model versions and source evidence retained for reviewing changes.
- Missing observations flagged for review rather than interpreted as asset removal.

These are design requirements, not capabilities already demonstrated by the shortlisted tools. IFC identifiers alone do not solve matching objects across independently reconstructed scans. That association requires additional logic and validation.

## 8. Analysis and main points

The main clarification was the required output: selectable building elements and assets with adequate geometric accuracy. A realistic walkthrough is secondary.

This changes the comparison. Gaussian splatting supports appearance and inspection, but standard splat training does not solve asset identity or records. Photogrammetry provides geometric evidence. Scan-to-BIM and semantic mapping address different stages of turning that evidence into useful objects.

The likely solution is modular:

1. Reconstruct geometry and camera poses.
2. Identify building elements and individual assets.
3. Store structured objects with persistent IDs and properties.
4. Provide review and correction tools.

The largest technical uncertainty is whether ordinary phone video will provide sufficiently complete and accurate geometry for the later stages. The most promising reconstruction candidates from this initial review are COLMAP, LingBot-Map and DA3-Base. This is a use-case-based shortlist, not a demonstrated ranking of accuracy. Given the limited time, the recommendation is to start with COLMAP and test one learned alternative only if needed. Passing their results to Cloud2BIM remains a hypothesis to test, including format conversion, scale and geometric coverage. MASt3R-SLAM is relevant to the literature comparison, but its non-commercial licence excludes it from the current implementation shortlist.

Requirements also need refinement. Correct room and floor assignment was initially sufficient for asset location, but this does not define acceptable wall-dimension errors. These tolerances should be agreed separately. Full BIM modelling may exceed the needs of a first asset inventory, so the pilot should cover only a small set of useful object types.

Commercial suitability concerns the complete configuration, including dependencies and model weights. Public source code or a permissive wrapper licence is not sufficient evidence on its own.

## 9. Main conclusions and recommendations

### Prioritised shortlist

The following priorities reflect the project requirements and the documentation reviewed, not results from our own benchmarks. There is not enough evidence to call any method the best for this room. To limit the workload, start with one reconstruction method and retain two alternatives.

| Priority | Candidate | Reason for selection | Main uncertainty |
|---|---|---|---|
| First reconstruction test | [COLMAP](https://github.com/colmap/colmap), including dense reconstruction | Provides camera poses and explicit geometry from ordinary images. It is a useful starting point for inspecting geometric errors and passing captured evidence to modelling tools. Core code has a permissive BSD licence. | Blank walls, reflections and incomplete image coverage may prevent a usable room reconstruction. Processing time and dependency licences need checking. |
| First alternative | [LingBot-Map](https://github.com/Robbyant/lingbot-map) | Directly addresses walkthrough video and sequential reconstruction. Local execution and Apache-2.0 code and model terms make it a promising learned alternative if COLMAP is too slow or incomplete. | Actual dimensional accuracy, drift, memory use and export suitability on our recording are untested. Streaming does not solve persistent updates across visits. |
| Reserve alternative | [Depth Anything 3 Base](https://github.com/ByteDance-Seed/Depth-Anything-3) | Estimates depth and camera poses jointly from multiple images. Its Apache-2.0 checkpoint makes it suitable for investigating a learned reconstruction from a selected set of room views. | Scale, cross-view consistency and preservation of small assets must be checked. The Base model is not the metric-depth variant. |

COLMAP is recommended first because the immediate deliverable is a static model and the main priority is inspectable geometry. This does not imply that it will be more accurate than the learned methods. LingBot-Map is the first alternative because its video-oriented workflow closely matches the planned capture. DA3-Base remains available if the first two do not meet the room requirements. There is no need to benchmark all three before making progress.

### Turning reconstruction into useful building objects

The reconstruction shortlist covers only the geometry stage. The most relevant complementary tools are:

- **[Cloud2BIM](https://github.com/VaclavNezerka/Cloud2BIM):** a candidate for converting sufficiently complete point clouds into walls, slabs, doors and windows. Its MIT-licensed research implementation is worth a small trial, but compatibility with the selected reconstruction must be verified. It does not provide a general maintenance-asset inventory.
- **[Bonsai and IfcOpenShell](https://github.com/IfcOpenShell/IfcOpenShell):** candidates for inspecting, correcting and storing structured building objects. Begin with a few selectable elements and an asset ID linked to a record, rather than attempting a complete BIM model immediately.
- **[ConceptGraphs](https://github.com/concept-graphs/concept-graphs):** a later research candidate for mapping individual assets. It requires depth and camera poses, and its selected dependencies and model licences still need review. It should not delay the first geometry experiment.

### Methods to defer

Splatfacto and LichtFeld focus on visual scene reconstruction and would require extra work to produce the required structured objects. They remain useful if visual inspection becomes important. MASt3R-SLAM is technically relevant but its published non-commercial licence conflicts with the deployment requirement. VGGT has conditional commercial terms, while Atlas has unresolved local-deployment and licensing questions in this review. Neither offers a clear reason to displace the initial shortlist at this stage.

Astra can assist with scripting and evidence-based model correction, but its architectural design demonstration does not establish reconstruction accuracy. RelateAnything concerns object relationships, and SIGReg concerns model training. These are not immediate substitutes for the geometry stage.

Persistent asset IDs, correction history and links to source evidence should be planned from the start. Automated condition assessment and change detection can follow once the static workflow works.

## 10. Next steps

1. Define one pilot room, its main surfaces and openings, and one maintenance-asset category. Agree acceptable geometric error and correction effort.
2. Record the room with the Galaxy S25 and prepare a reference inventory. Measure several dimensions, using one for scale and the others for independent validation.
3. Check COLMAP's selected build, dependencies and storage needs, then run a small reconstruction. Include dense geometry if required for the next stage. Record frame selection and settings.
4. Check missing surfaces, dimensional errors, asset visibility, processing time and manual effort. If the result is adequate, proceed without testing every alternative. If it is inadequate or impractically slow, test LingBot-Map on the same recording. Keep DA3-Base as the next option if needed.
5. Check the chosen output's scale, coordinate system and format, then attempt a small Cloud2BIM conversion. Do not assume that all reconstruction outputs are directly compatible.
6. Inspect the result in Bonsai. Record missing or incorrect building elements and the time needed to correct them. If automatic conversion fails, investigate the failure and try limited assisted modelling from the captured geometry.
7. Add one selectable maintenance asset with a persistent ID and editable properties. Keep condition records separate from the scan so that geometry can later be replaced without losing history.
8. After the static workflow works, repeat capture after a known change and test alignment, identity preservation and reviewed updates. Treat missing observations as uncertain rather than automatic asset removal.
