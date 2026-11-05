# Problem analysis

## 1. Industry context

Construction and building maintenance companies, such as Heijmans (the project stakeholder), maintain large buildings like offices, hospitals, educational institutions and airports. The maintenance is done under a contract with the building owner. The contract duration varies per contract, for example 1, 2 or 5 years. Before a contract starts, the maintainer needs reliable information about the building: which assets are present, where they are located and what their condition is.

## 2. Contract handover

At the start of a contract, the previous maintainer hands over an asset inventory list. This list is usually an Excel sheet, sometimes accompanied by floor plans with the assets drawn on them by hand. For existing buildings that Heijmans maintains, no 3D model is usually available. Detailed 3D models with extensive data exist mainly for buildings constructed by Heijmans.

## 3. Building inventory inspection

After the handover, Heijmans performs a building inventory inspection. This is the process of inspecting, identifying and officially documenting the assets (e.g., fire alarms, fire extinguishers) in a building and their current physical condition. An inspector walks through the building, records every asset and its condition and compares the result with the records of the previous maintainer.

The condition assessment follows NEN 2767, the Dutch standard for inventory and condition inspection. The assessment is visual only and involves no measurements. For every asset, the inspector records a condition score and the defects present (e.g., rust or corrosion). For each defect, the inspector records its intensity, size and severity, its consequences and whether it affects part of the asset or the entire asset.

## 4. Problems

The handed-over records provided by the previous maintainer are frequently incomplete or outdated. If a list is not updated thoroughly over time, it deviates more and more from reality. Data quality differs per project but is usually low. Keeping the list up to date is a common struggle across the entire industry.

The inspection itself is difficult and time consuming. Depending on the building, it takes days or even weeks and requires considerable manpower.

Low data quality also affects other work. Heijmans develops solutions that perform data-driven tasks on top of the asset data. These solutions are currently based on incorrect or incomplete data.

## 5. Current mitigation

Heijmans experiments with different technologies to improve data quality. One approach is to combine all available data sources: Excel lists, floor plan drawings and, where available, 3D building models with data from connected building systems such as heating and ventilation. These systems contain information about which assets are linked to them. In most cases, however, no 3D model of the building is present.

## 6. Project goal

This project focuses on wearables and on the point of view of a person who walks through the building and collects the data. The solution adds value if it reduces the time required for the inspection or improves the quality of the data. An example target is that one person walks through a building in one day and a 3D model is created from the collected data.

## 7. Requirements and scope

The required output is an asset list that is as correct as possible. For maintenance, it is sufficient to know which assets are present in each room and on which floor. Centimeter-level accuracy is not required; location accuracy of 10 to 15 cm is sufficient.

Because the condition assessment is visual, a camera can in principle capture everything an inspector sees. The project will test the approach on one specific asset type.

## 9. Adoption risk

Inspectors may resist the new solution. To address this, the project needs to show that the solution is valuable to the inspectors themselves: it reduces the time and effort spent on a task they do not enjoy, so they can focus on work they find more meaningful.

## Open points

- Which asset type the project will test.
