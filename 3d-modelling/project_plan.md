# Heijmans: Project Plan

## 1. Context

Heijmans needs reliable building information before starting a maintenance contract. This includes which assets are present, their location within the building and their condition.

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

Build an end-to-end prototype (i.e., MVP) incl. 3D model generation and object recognition. Asset recognition by room and floor has a higher priority than geometric accuracy. Focus on one generic room (e.g., office space). The priority is fixed assets such as fire extinguishers, emergency exits, lights, ventilation.

Focus on building the 3D model without acessing external cloud service (i.e., ABRO regulations). Compare the developed system to OpenSpace - focus on X6 and smart glasses.

Check what operating systems can your system run on.

Currently the industry standard is Autodesk Revit BIM.

**Practical objective:** Provide Heijmans with evidence to assess whether these methods can produce a reliable inventory with less collection and recording effort than the current process.

## 4. Research Questions

**Main research question:** 

How can a 3D model of indoor space be developed to support building inventory inspection based on visual input?

**Subquestions:**
1. Which metrics evaluate methods for generating a 3D model?
2. What methods exist and how do they compare on these metrics in literature?
3. How do the selected methods perform in experiments and which factors affect the results?
4. (possibly later) How can assets of one type and their condition be identified in the 3D model?

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

## 9. Risks

## 9. Adoption risk

- Inspectors may resist the new solution. To address this, the project needs to show that the solution is valuable to the inspectors themselves: it reduces the time and effort spent on a task they do not enjoy, so they can focus on work they find more meaningful.


## 9. Planning

| Sprint N              | Duration         |
| --------------------- | ---------------  |
| Sprint 1              | Sept 23 - Oct 14 |
| Sprint 2              | Oct 15 - Nov 11  |
| Sprint 3              | Nov 12 - Dec 10  |
| Sprint 4              | Dec 11 - Jan 13  |
| Sprint 5              | Jan 14 - Jan 27  |
