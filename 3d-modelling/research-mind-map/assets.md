### Asset priority

#### Building Services Assets (highest asset management value)

These are directly linked to maintenance plans, inspections, and regulations

#### Electrical Engineering 
- Main distribution board(s)
- Sub-distribution boards
- Distribution cabinets
- Cable trays & conduits
- Lighting fixtures
- Emergency lighting
- UPS / emergency power supply
- Grounding systems

#### Mechanical Engineering 
- Air handling units (AHU)
- Fans
- Ducts & grilles
- Heating units
- Cooling installations
- Heat pumps
- Radiators / underfloor heating
- Shut-off valves & control valves

#### Sanitary 
- Water pipes
- Drains
- Sanitary fixtures
- Legionella-critical points

-> Relevant because: directly linked to maintenance systems.

#### Fire Safety Assets (compliance-critical) 
- Fire alarm system (FAS)
- Fire detectors
- Evacuation alarm system (EAS)
- Sprinkler system
- Alarm valve rooms (AVR)
- Fire dampers
- Fire hose reels
- Fire extinguishers
- Smoke & heat exhaust systems (SHE)
- Escape route lighting
- Escape route plans

-> Relevant because: legally required maintenance.

#### Vertical & Horizontal Transport Systems 
- Elevators
- Escalators
- Moving walkways
- Freight elevators
- Permanent lifting facilities

#### Spaces & Space-Related Assets

Crucial for navigation, localization and context — essential for Gaussian Splatting.

- Spaces (with unique ID)
- Space functions
- Zones
- Compartments
- Fire compartments
- Technical rooms
- Shafts

-> Relevant because: assets always exist within a space.

#### Safety & Occupational Health 
- Guardrails
- Fall protection systems
- Emergency exits
- First aid facilities
- Emergency response cabinets
- Evac chairs
- Anti-slip provisions

#### Site & Building-Related Outdoor Assets

Optional. Mainly relevant for large projects where, in addition to asset management & maintenance, infrastructure and building services are involved.

- Pavements
- Fences
- Gates
- Outdoor lighting
- Gullies
- Rainwater drainage
- Landscaping

#### Asset Metadata (at least as important as geometry)

Without this, BIM is not an asset management tool.

Relevant per asset: 
- Unique Asset ID (OMS connection)
- Asset group / classification
- Manufacturer
- Type
- Serial number
- Installation date
- Warranty
- Maintenance frequency
- Criticality
- Location (room, floor)
- Relationship with other assets

#### Assets that contribute to a 3D model/inventory and may pose risks, but are not maintained:

#### Structural & Architectural Assets

These form the spatial and safety-bearing structure of the building and are essential for inspections, damage assessments, and modifications.

#### Structure 
- Foundations (piles, footings, strip foundations)
- Columns
- Beams
- Floors (hollow-core slabs, wide slab floors, cast-in-place concrete)
- Load-bearing walls
- Stability elements (cores, shear walls)
- Stairs & landings

#### Architectural 
- Facades (curtain wall, precast concrete, masonry)
- Roofs (roof covering, insulation, roof penetrations)
- Interior walls
- Doors & frames
- Windows
- Ceilings
- Floor finishes

-> Relevant because: damage assessments, changes, inspections, and safety originate here.


