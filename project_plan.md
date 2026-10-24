# Heijmans: Project Plan

## 1. Context

Heijmans needs reliable building information before starting a maintenance contract. This includes:

- Which assets are present.
- Their location within the building.
- Their condition.

At contract handover, the previous maintainer provides an asset inventory list, often through Excel sheets and sometimes annotated floor plans. After the handover, Heijmans performs a new building inspection visually, comparing the new information with the records from the previous maintainer. These records are frequently incomplete or outdated. The process of visual inspection consists of noting down every asset in the building and its condition and can take days or even weeks. 

This applied master's research project examines the potential of video-based 3D reconstruction and asset recognition to support inventory collection. Heijmans is the client and the people inspecting buildings and recording assets are the intended users.

## 2. Problem Description

At the start of a maintenance contract, Heijmans must establish a reliable inventory through building inspections and manual recording. This requires substantial time and effort. During the contract, changes are not consistently recorded, causing the inventory to become outdated and creating repeated work at the next handover.

The main issues are:

- Incomplete or outdated asset information.
- Time-consuming inspection and manual recording.
- Limited links between asset records and their locations.
- Difficulty keeping the inventory up-to-date.

The research problem is determining whether video-based 3D reconstruction and asset recognition can support reliable inventory collection with less manual effort.

## 3. Project Objectives

**Research objective:** Evaluate how video-based 3D reconstruction and asset recognition can support building inventory collection for maintenance.

The research aims to:

- Compare selected methods in terms of model detail, completeness, processing time and asset recognition accuracy (targetting 10-15 cm deviation from the physical world).
- Assess whether assets can be located by room and floor.
- Identify limitations and conditions affecting practical use.

**Practical objective:** Provide Heijmans with evidence to assess whether these methods can produce a reliable inventory with less collection and recording effort than the current process.

## 4. Research Questions

**Main research question:**

How can 3D world models and robotics algorithms support more efficient building maintenance?

**Subquestions:**

1. How can 3D reconstruction of indoor space be developed to support maintenance based on visual input? What metrics are suitable to compare different methods?
2. How can assets and their conditions be identified in the 3D reconstruction?
3. What evaluation framework is suitable to compare different methods?


## 5. Expected Business and Technical Outcomes

| Outcome | Expected contribution |
| --- | --- |
| Business value        | Evidence for Heijmans to assess whether the investigated methods can reduce inventory effort.                                 |
| Technical insights    | A comparison of selected methods, identifying their performance, limitations and conditions for use.                          |
| Research deliverables | A research paper documenting the methods, experiments, results and recommendations.                                           |
| Wider applicability   | An assessment of which findings may apply to other building maintenance situations and which depend on the tested conditions. |

## 6. Scope and Boundaries

The research focuses on building a 3D reconstruction of an indoor space, using data captured by a person. The proposed scope is:

| Within scope | Outside scope |
| --- | --- |
| Comparing selected methods for video-based 3D reconstruction and asset recognition. | Developing a production-ready maintenance system. |
| Evaluating model detail, completeness, processing time and recognition accuracy. | Autonomous robot navigation and data collection. |
| Investigating asset location by room and floor. | Centimetre-level positioning as a requirement. |

The capture device could be a smartphone, Meta smart glasses or another camera. Different capturing devices would be compared and evaluated. A study limited to one asset type is acceptable.

## 7. Potential Methods

| Approach | Output |
|---|---|
| Photogrammetry        | Camera poses, point clouds and surface meshes from overlapping images                 |
| Gaussian splatting    | A scene represented by coloured 3D Gaussians for rendering different viewpoints       |
| Semantic 3D mapping   | Geometry associated with object categories and instances                              | 

## 8. Ethics and Data Management
- Agree on permission and conditions for recording at the selected building.
- Minimize capture of identifiable people and sensitive building information. Exclude or anonymize such content where necessary.
- Follow GDPR practises.

## 9. Planning

| Sprint N              | Duration         |
| --------------------- | ---------------  |
| Sprint 1              | Sept 23 - Oct 14 |
| Sprint 2              | Oct 15 - Nov 11  |
| Sprint 3              | Nov 12 - Dec 10  |
| Sprint 4              | Dec 11 - Jan 13  |
| Sprint 5              | Jan 14 - Jan 27  |
