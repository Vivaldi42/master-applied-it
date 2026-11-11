<!-- Command to convert to PDF -->
<!-- pandoc problem-analysis.md -o problem-analysis.pdf --pdf-engine=xelatex -V geometry:margin=2.5cm -->

# Problem Analysis
# Author: Vladislav Stefanov
# Date: 07.11.2026

This analysis is based on interviews with project stakeholders from Heijmans. It was discussed with and approved by them.

## 1. Industry context

Construction and building maintenance companies, such as Heijmans, maintain large buildings (e.g., offices, hospitals, educational institutions and airports). The maintenance is done under a contract with the building owner. Contract durations vary (e.g., 1, 2 or 5 years). Before a contract starts, the maintainer (also referred to as the contractor) needs reliable information about the fixed assets in a building: which assets are present, where they are located and what their condition is.

In the Netherlands, the condition of building and installation components is assessed according to the **NEN 2767 standard**. The method is visual and involves no measurements. For every asset, the inspector records the defects present (e.g., rust or corrosion) and rates each defect by its severity, intensity and extent. These ratings are combined into a condition score on a six-point scale, from 1 (excellent) to 6 (very poor).

Most maintained buildings (e.g., hospitals and office buildings) have no 3D model. Buildings constructed in the last 5 to 10 years usually have one in the form of a building information model (BIM). The majority of maintained buildings are older than that. This situation applies to the entire industry, not only to Heijmans. Smaller contractors rarely use BIM, but they are also rarely involved in projects of this scale.

## 2. Contract handover

At the start of a contract, the previous maintainer hands over an asset inventory list. This list is usually an Excel sheet, sometimes accompanied by floor plans with the assets drawn on them by hand. The data is recorded and maintained manually.

## 3. Building inventory inspection

After the handover, Heijmans performs a building inventory inspection. This is the process of inspecting, identifying and officially documenting the assets (e.g., fire alarms and fire extinguishers) in a building and their current physical condition. An inspector walks through the building, records every asset and assesses its condition according to NEN 2767 (Section 1). The inspector then compares the result with the records of the previous maintainer.

## 4. Problems

- **The records handed over by the previous maintainer are frequently incomplete or outdated.** Data quality varies per project but is usually low. Changes made in a building are often not recorded or communicated. This also applies to changes made by other companies working in the building. As a result, the list inevitably deviates further from reality over time. Keeping the list up to date is a common problem across the entire industry. Low data quality also limits the usefulness of the data-driven solutions that Heijmans develops on top of the asset data, because these solutions require high-quality data.

- **The inspection itself is monotonous and time-consuming.** Depending on the building, it takes days or even weeks and requires a considerable number of people. The task is repetitive and labor-intensive, which makes it unpopular among employees.

## 5. Current mitigation

Heijmans experiments with different technologies to improve data quality. One approach is to combine all available data sources: Excel lists, floor plan drawings and, where available, BIM models. Heijmans also explores augmented reality (AR) solutions for maintenance in buildings for which a BIM model is available. However, both approaches are limited without a BIM model, which most maintained buildings do not have (Section 1).

## 6. Project goal

This project focuses on AI wearables used by a person who walks through a building to collect data. The use of AI wearables was chosen by the stakeholders. The collected data is converted into a 3D model of the building that contains its assets. An asset list can then be extracted from this model. In addition, the 3D model can be used for other purposes, such as the approaches described in Section 5. The solution adds value if it reduces the time required for the inspection or improves the quality of the data.

The project has two deliverables with different accuracy requirements:

- **3D model:** a location accuracy of 10 to 15 cm is sufficient. Deviations of a few centimeters are acceptable.
- **Asset list:** for each asset, it is sufficient to know the floor and the room in which it is located. The list should be as complete and correct as possible.

Because the NEN 2767 assessment is visual (Section 1), a camera can in principle capture the information an inspector uses. In a later phase, a simplified classification of the asset conditions (e.g., good, intermediate or bad) may be developed.

## 7. Long-term direction

The long-term goal is a system that keeps the 3D model, the asset list and the asset conditions of a building up to date with minimal manual effort.

### 7.1 Data collection stages

The expected development of data collection consists of three stages:

1. **Periodic walkthrough (currently the main direction):** a person walks through the building with an AI wearable. The collected data is used to update the 3D model, the asset list and the asset conditions. The walkthrough is repeated every few months or once a year. This stage extends beyond the scope of this project.
2. **Continuous collection (years from now):** employees wear smart glasses or body-worn cameras during their regular work. The system uses this data to keep the 3D model up to date continuously.
3. **Robotic inspection (years from now):** a mobile robot performs the walkthrough instead of a person and uses the same system to update the 3D model. One reason this is currently not feasible is limited door access in some buildings.

### 7.2 Data security

Heijmans distinguishes between secret and non-secret projects. Data should be processed as locally as possible. **The preferred option is Heijmans' own on-premise servers**, mainly because of the requirements of secret projects. Servers located in the EU are the next option.

For non-secret projects, a third-party application can be acceptable if either the data is stored on EU servers and is not used to train AI models, or the data stays on the device and is deleted within several hours.

Third-party applications are not acceptable for secret projects. In some secret projects, cameras may not be allowed at all.

The stakeholders recommend basing the advice of this project on the requirements of secret projects, because such advice is also valuable for non-secret projects. 