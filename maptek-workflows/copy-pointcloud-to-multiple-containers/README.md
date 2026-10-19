# Copy Pointcloud to Multiple Containers

A Maptek PointStudio workflow that copies one or more pointcloud objects to multiple destination containers.

## Purpose

Reduce repetitive copy-and-paste steps when preparing pointcloud data for multiple survey areas or Request Levels (RL).

## How It Works

1. Enter the source pointcloud paths and destination container paths.
2. Validate the input paths and check for duplicates.
3. Copy the first source pointcloud.
4. Paste it into each destination container.
5. Repeat for the remaining source pointclouds.

## Requirements

- Maptek Workbench with PointStudio.
- An open project containing the source pointclouds.
- Destination containers already created in the same project.
- Embedded Python execution enabled in Workbench.

The workflow was saved with Maptek Workbench 2025.1. It uses native PointStudio Copy/Paste commands and embedded Python without importing the Maptek Python SDK.

## Inputs

| Input | Description |
| --- | --- |
| Source pointclouds | One or more full object paths, separated by commas |
| Destination containers | One or more full container paths, separated by commas |

Example source paths:

`/surveys/cloud_a, /surveys/cloud_b`

Example destination paths:

`/rl/area_01, /rl/area_02, /rl/area_03`

These are PointStudio project paths, not Windows folder paths.

## Usage

1. Open the WFD file in Maptek Workbench.
2. Run the workflow with the relevant PointStudio project open.
3. Enter or drag the source pointcloud object paths into the setup panel.
4. Enter or drag the destination container paths.
5. Separate multiple paths with commas.
6. Continue the workflow.
7. Inspect the copied objects in each destination container.

## Input Validation

The workflow checks for:

- Empty source or destination lists.
- Paths that do not begin with `/`.
- Duplicate source or destination paths.
- Destinations that match a source path or sit beneath it.

These checks validate path text; object existence and type are resolved by PointStudio during execution.

## Output

Each destination container receives a copy of every source pointcloud.

For example, two source pointclouds and three destination containers produce six copied objects.

Original source objects remain in place. Copy naming follows PointStudio's default behaviour.

## Notes

- The workflow does not create destination containers.
- It does not rename the copied objects.
- Running it again may create additional copies.
