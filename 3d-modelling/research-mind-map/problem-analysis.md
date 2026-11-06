# Problem analysis

## 1. Industry context

Construction and building maintenance companies, such as Heijmans (the project stakeholder), maintain large buildings like offices, hospitals, educational institutions and airports. The maintenance is done under a contract with the building owner. The contract duration varies per contract, for example 1, 2 or 5 years. Before a contract starts, the maintainer needs reliable information about the building: which assets are present, where they are located and what their condition is.

## 2. Condition assessment standard (NEN 2767)

In the Netherlands, the condition of building and installation components is assessed according to NEN 2767. The method is visual and involves no measurements. For every asset, the inspector records the defects present (e.g., rust or corrosion) and rates each defect by its severity, intensity and extent. These ratings are combined into a condition score on a six-point scale, from 1 (excellent) to 6 (very poor).

## 3. Contract handover

At the start of a contract, the previous maintainer hands over an asset inventory list. This list is usually an Excel sheet, sometimes accompanied by floor plans with the assets drawn on them by hand. For existing buildings that Heijmans maintains, no 3D model is usually available. Detailed 3D models with extensive data exist mainly for buildings constructed by Heijmans.

## 4. Building inventory inspection

After the handover, Heijmans performs a building inventory inspection. This is the process of inspecting, identifying and officially documenting the assets (e.g., fire alarms, fire extinguishers) in a building and their current physical condition. An inspector walks through the building, records every asset and assesses its condition according to NEN 2767 (Section 2). The inspector then compares the result with the records of the previous maintainer.

## 5. Problems

- The handed-over records provided by the previous maintainer are frequently incomplete or outdated. If a list is not updated thoroughly over time, it deviates more and more from reality. Data quality differs per project but is usually low. Keeping the list up to date is a common struggle across the entire industry.

- The inspection itself is difficult and time consuming. Depending on the building, it takes days or even weeks and requires considerable manpower.

- Heijmans also develops solutions that perform data-driven tasks on top of the asset data. These solutions require high-quality data, so incorrect or incomplete records limit their usefulness.

## 6. Current mitigation

Heijmans experiments with different technologies to improve data quality. One approach is to combine all available data sources: Excel lists, floor plan drawings and, where available, 3D building models with data from connected building systems such as heating and ventilation. These systems contain information about which assets are linked to them. In most cases, however, no 3D model of the building is present.

## 7. Project goal

This project focuses on AI wearables used by a person who walks through the building to collect the data, which is then converted to a 3D model. The solution adds value if it reduces the time required for the inspection or improves the quality of the data.

The required output is an asset list that is as correct as possible. For maintenance, it is sufficient to know which assets are present in each room and on which floor. Centimeter-level accuracy is not required; location accuracy of 10 to 15 cm is sufficient.

Because the condition assessment is visual, a camera can in principle capture everything an inspector sees. 