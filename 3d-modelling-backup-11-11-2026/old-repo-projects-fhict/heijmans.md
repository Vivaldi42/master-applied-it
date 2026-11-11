Heijmans Project

Work on the project both to:
1. solve the problem of the stakeholder use case
2. generalize to demonstrate that the solution can be relevant also for other situations via 1.

Make a planning for the semester.

----
Heijmans project: core system; justification; generalization
How recent developments in world models and robotics algorithms can be used to optimize construction and building maintenance?
-> get better context about the problem

- **Justify** the design choices (which algorithms).
- Explore **related work**, do literature study. How do others solve the problem? How is the problem solved now?
- How those algorithms can be applied to construction/building environments? How to measure the acceptance criteria/evaluation criteria/**benchmarks**/measurement and validation methodology/validation of conclusions. Comparing the performance of different algorithms. What are my contributions to those algorithms related to construction/maintenance?
- **Generalization**: 
    - Does the project provide new knowledge how to address problems in architecture/construction/building maintenance? Using this system architecture different use cases in architecture/construction can be solved.
    - Write a paper to share the knowledge and the contributions to the ICT domain.
    - Generalization happens when you have justification and validation
- User quality/user tests.

You need to understand the things to the level you can better apply them.
When building a system rank the functions by their added value for the client. What are the functions that have the highest value?


Design Challenge
[
   <FOS - Form of Solution>
    - the product in general
    - break down the system in different system functionalities listed as keypoints
]
=>
[
    <Users>
]
=> in =>
[
    <Context>
]
=>
[
    <PA - Perform Activities> --- functional requirements
    - keypoints of what users can do using the system
]
=> so that =>
[
    <TP - Targetted Performance> --- non-functional requirements
    - what do they achieve?
]

The client Heijmans is interested in TP. Users at Heijmans are interested in PA and TP.

---

Giving instructions to an LLM is very similar to giving instructions to a person/team member. The way it is done is similar to managing or coaching a team member. When doing it think about information flow, information management and information structuring. I have knowledge of the client and understand the content to be conveyed by the output of the LLM.

Apply the V-model - specify the requirements and validating the results

       control, boudnary conditions
        |
input->[module]->output
        |
        API

If I deliver a module, it is going to be successful only if the client can apply it successfully. The success of my client is also my responsibility.
Try to understand the things to the level you can better apply them.
Think what are the functions that bring the highest value to the client - this is the start of the system definition and what is a proof-of-concept - core benefit of the system.

|------ waterfall way (the entire project) ------|
agile (execution within a phace) -> agile -> agile ->...
The entire project is done waterfall and the phases within are done agile.
The first step is specification/requirements.
Plan experiments and execute them.
---

When constructing a building, there are a BIM model and 3D info available.
When maintening one, there is no knowledge about the building. A person needs to go to a location, do inspections and write down all assets available and what is their condition in a manually made 2D map. This process can take 1 year before starting the maintenance. If a 3D model can be created instantly and some assets are recognized this can make the process much more efficient. This will speed up the information acquiring about a new building.

If this can be done with smart glasses, the benefit is that a person can do it and there is no need for a robot or any other hardware.

It would be highly valuable if information on the model can be overidden and be kept up-to-date.

Openspace is an alternative solution but it does not provide recognition of assets and in general is not used in maintenance.

A key question is how to be sure that glasses capture everything needed.


If a person wears the glasses every day, the model can be updated daily.

Priorities:
1. Generate a 3D model and see how detailed is it.
2. What is the speed? How fast can the 3d map be developed?
3. What is its quality? Can assets be recognized in the map?

---

I work on a project related to maintenance of buildings, and I'm interested in how can I create a 3D model of that building from video on smartphone or on smart glasses from Meta. The goal is to create it and compare how fast it is, how detailed is it, what is the quality, and later can we recognize assets in the video. Assets in that sense mean fire alarms, walls, sockets in the walls, doors, and so on. The model should ideally be easy to get up to date, so it should be able to overwrite and make it up to date.

You need data about what is in a building before you can maintain it - (vaststelling rivet situatie/opname) - building inventory inspection. The act of inspecting, identifying, and officially documenting the current physical state of a building. Currently this process is quite a mess. It is important to know what assets are in the building and what is their condition. Maybe the list from the previous maintainer is not a complete overview because if it isn't updated thoroughly over time it deviates more and more from reality. The process of writing down the assets is difficult and time consuming. This is a standard procedure for the entire industry

NEN 2767 - inventory check and condition inventory standard. It is visual inspection, no measurements. For every asset condition score and malfunctions (e.g., corosion, rust) intensity and size are recorded. 

It is a list of assets with their condition. When a building is given to a tender, different companies apply. When a company wins it is given the old asset list which is usually incomplete and obsolete. The new company makes a new list. When there is a change, the list should be updated but often that doesn't happen and the list deviates from reality over time. When the contract is finished, there is another tender and the company hands over that list to the new maintainer company. After that the company that wins the tender needs to make the same inspection and list again. This happens every 1,2,5 years depending on the contract. Data in the asset list is not usually on a map/model of buildings they maintain. When starting a new contract it's an excel list, may be floor plans with things drawn on it. Data quality is not very high.

What would fix the problem is to scan the building (preferably estimate of the condition) and make a 3D model. This shouldn't take more manpower and hours than it takes now. It should be done with high accuracy. Maybe combine different kinds of data to improve its quality?

It is important the list of assets to be as correct as posible and where is their position. Doesnt need to be cm-level accurate, knowing what asset is in which room on which floor is enough.

Example buildings include offices, hospitals, universities, airports, industrial buildings.

If the first version is done for a specific asset type, that would be fine.

Look at it from the perspective of a person. How they go around the building and get that data easily and fast? It needs to cost less time and effort than the old approach. Currently it takes several days, maybe weeks.

Think about GDPR, do not follow the people because that would violate their privacy.
---------------------------------------------------
Building Services Assets (highest asset management value)

These are directly linked to maintenance plans, inspections, and regulations

Electrical Engineering 
• Main distribution board(s)
• Sub-distribution boards
• Distribution cabinets
• Cable trays & conduits
• Lighting fixtures
• Emergency lighting
• UPS / emergency power supply
• Grounding systems

Mechanical Engineering 
• Air handling units (AHU)
• Fans
• Ducts & grilles
• Heating units
• Cooling installations
• Heat pumps
• Radiators / underfloor heating
• Shut-off valves & control valves

Sanitary 
• Water pipes
• Drains
• Sanitary fixtures
• Legionella-critical points

➡️ Relevant because: directly linked to maintenance systems.

Fire Safety Assets (compliance-critical) 
• Fire alarm system (FAS)
• Fire detectors
• Evacuation alarm system (EAS)
• Sprinkler system
• Alarm valve rooms (AVR)
• Fire dampers
• Fire hose reels
• Fire extinguishers
• Smoke & heat exhaust systems (SHE)
• Escape route lighting
• Escape route plans

➡️ Relevant because: legally required maintenance.

Vertical & Horizontal Transport Systems 
• Elevators
• Escalators
• Moving walkways
• Freight elevators
• Permanent lifting facilities

Spaces & Space-Related Assets

Crucial for navigation, localization and context — essential for Gaussian Splatting.

• Spaces (with unique ID)
• Space functions
• Zones
• Compartments
• Fire compartments
• Technical rooms
• Shafts

➡️ Relevant because: assets always exist within a space.

Safety & Occupational Health 
• Guardrails
• Fall protection systems
• Emergency exits
• First aid facilities
• Emergency response cabinets
• Evac chairs
• Anti-slip provisions

Site & Building-Related Outdoor Assets

Optional. Mainly relevant for large projects where, in addition to asset management & maintenance, infrastructure and building services are involved.

• Pavements
• Fences
• Gates
• Outdoor lighting
• Gullies
• Rainwater drainage
• Landscaping

Asset Metadata (at least as important as geometry)

Without this, BIM is not an asset management tool.

Relevant per asset: 
• Unique Asset ID (OMS connection)
• Asset group / classification
• Manufacturer
• Type
• Serial number
• Installation date
• Warranty
• Maintenance frequency
• Criticality
• Location (room, floor)
• Relationship with other assets

Assets that contribute to a 3D model/inventory and may pose risks, but are not maintained:

Structural & Architectural Assets

These form the spatial and safety-bearing structure of the building and are essential for inspections, damage assessments, and modifications.

Structure 
• Foundations (piles, footings, strip foundations)
• Columns
• Beams
• Floors (hollow-core slabs, wide slab floors, cast-in-place concrete)
• Load-bearing walls
• Stability elements (cores, shear walls)
• Stairs & landings

Architectural 
• Facades (curtain wall, precast concrete, masonry)
• Roofs (roof covering, insulation, roof penetrations)
• Interior walls
• Doors & frames
• Windows
• Ceilings
• Floor finishes

➡️ Relevant because: damage assessments, changes, inspections, and safety originate here.