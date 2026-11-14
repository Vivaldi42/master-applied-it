Midterm portfolio review - 10.11.2026
You have document on problem analysis and you were working on your background research. You found some additional papers related to maintenance of buildings. Now, your background research considers the building environment some more, but you still want to work on the document. For example, convert the bullet points into text and create a 'real' document.

Regarding the process of your project. We see that you are expanding from analysis towards design and realization. You plan to come with a list of algorithms to investigated further and define a proper experiment set-up. You use criteria based decision making. We advise to make this more explicit in your background research document. Define your criteria and substantiate the criteria. Also create a table and use --, -, +, ++ or something like that and substantiate your choices. You can list 15 potential algorithms and using criteria based decision making you can reduce to 5 algorithms which you investigate further by experimenting with them.

We discussed the option of an end-to-end prototype and then refine it iteratively. This resembles an MVP (minimal viable product). 

---

Analysis: your strongest current evidence
DONE:
- Your Problem Analysis is a good foundation. You explain the maintenance workflow, the shortcomings of existing asset inventories, and the potential value of reconstructing buildings from visual data.
- You also distinguish between the accuracy required for the 3D geometry and the information needed for an asset list. This is important because these may require different technical approaches.

NEXT STEPS: strengthen the scientific and technical analysis. In particular:
- Develop a systematic literature comparison of photogrammetry, SLAM, semantic mapping and learning-based reconstruction approaches.
- Critically investigate which assumptions from robotics remain valid when data is captured by a person wearing a camera.
- Define measurable evaluation criteria, including geometric accuracy, completeness, robustness, computational requirements and suitability for identifying assets.
- Investigate how the proposed reconstruction approach will actually support the maintenance workflow, rather than treating 3D reconstruction as an end in itself.
- A particularly promising contribution to IT-domain knowledge would be an evidence-based method for selecting and evaluating robotics-derived 3D reconstruction approaches for human-operated building inspections.

Professional Duties: Hardware Interfacing (Level 3)
DONE:
- You have identified a smartphone, smart glasses and a 360° camera as potential capture devices. This is relevant preparation, but it is not yet evidence of competence in Hardware Interfacing.

NEXT STEPS: investigate the practical interface between the capture hardware and the reconstruction software:
- For example, compare the devices' sensor capabilities, calibration requirements, image and video formats, timestamps, available motion data and possibilities for synchronising sensors.
- Demonstrate how you acquire, process and validate data from at least one device, and investigate how hardware characteristics influence reconstruction quality.
- The professional product could be a documented and tested data-acquisition interface or pipeline, supported by reproducible measurements.

Design and Realise
DONE: 
- Your background research identifies the main stages of a reconstruction pipeline, but this is not yet a substantiated design. As above you might have done more work already as shown in your portfolio so in that case that would be a good first step to take.

NEXT STEPS:
- Develop a software architecture that connects sensor input, localisation, geometry reconstruction, semantic information and asset identification. Justify the selected components and their interfaces using your analysis.
- Subsequently, implement and evaluate a limited but complete pipeline using representative building data.
- It would be particularly useful to demonstrate whether the resulting model meets the stakeholder requirements for location accuracy and whether asset information can be extracted reliably.
- Develop a MVP (end-to-end prototype).
  
Advise
DONE:
- Your stakeholder discussions provide a useful basis for future advice. In particular, the distinction between confidential and non-confidential projects could significantly influence selection of technologies to use.

NEXT STEPS:
- Develop a comparative recommendation that considers reconstruction quality, computational requirements, data security, implementation effort and maintenance value.
- Discuss the recommendations with company stakeholders and document their responses.

Manage & Control
DONE:
- There is not yet enough evidence for this outcome.

NEXT STEPS:
- Besides the documentation that most likely will arise from further development and a maturing prototype your progress report can also help to provide assessors with clear insights in how you managed your project in a structured and methodically sound manner.

Priorities

I recommend concentrating on four priorities for the next portfolio submission (in the middle of December):

- Complete the background analysis. Transform the current research outline into a critical, evidence-based comparison of relevant reconstruction methods and their applicability to maintenance.

- Establish a reproducible evaluation method. Define datasets, reference measurements, accuracy metrics and test conditions before comparing approaches.

- Demonstrate concrete software and hardware-interfacing evidence. Develop a limited working pipeline, document how sensor data is acquired and evaluate its performance (see also our discussion about what the prototype should serve most)..

- Connect technical results to professional value and transferability. Demonstrate whether the approach can support building inventory inspections and identify which findings may be useful in other buildings, devices or maintenance contexts.

---

Research questions:

Main research question: How can a 3D model of indoor space be developed to support buildinginventory inspection based on visual input?
- SQ1. Which metrics evaluate methods for generating a 3D model?
- SQ2. What methods exist and how do they compare on these metrics in literature?
- SQ3. How do the selected methods perform in experiments and which factors affect the results?

Your main research question and subquestions still focus primarily on generating a 3D model and evaluating the technologies used to create it.

However, as we discussed, and as your project is developing through input from professional stakeholders, the actual need appears to be somewhat different. The priority is not necessarily to create a realistic 3D representation of a building, but to reliably identify and localise relevant assets for building inventory inspections. A 3D model may support this, but its visual realism is less important than its spatial accuracy, the correct identification of assets and their association with the appropriate room or location.

This distinction is important because your current research questions risk making the technology (3D reconstruction) the starting point, rather than the professional problem you are trying to solve. You may consequently optimise the quality of a 3D model without sufficiently demonstrating its value for the actual inventory process.

I therefore recommend reconsidering your main research question and subquestions from a solution-driven rather than technology-driven perspective.

For example, your main research question could move towards:

How can visual data collected during building walkthroughs be used to reliably identify and localise building assets to support inventory inspections?

Your subquestions could then address:
- What information, accuracy and completeness are required to support building inventory inspections?
- Which visual sensing, localisation and reconstruction approaches can contribute to meeting these requirements, and what are their respective limitations?
- How can these approaches be combined into a solution that identifies assets and associates them with reliable spatial locations?
- How effectively does the resulting solution meet the requirements under representative building conditions?

This does not mean that 3D reconstruction is no longer relevant. It may remain an essential component of your solution. However, its role and the criteria used to evaluate it should follow from the requirements of the professional application, rather than the other way around.

This shift would also strengthen your Master's-level analysis and design work, because it connects stakeholder needs, technological choices, evaluation criteria and the intended contribution to transferable IT-domain knowledge.