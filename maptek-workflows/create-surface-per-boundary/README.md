# Create Surface per Boundary

A customised workflow in Maptek PointStudio that creates separate
topographic surfaces for multiple boundary polygons
using the same pointcloud input.

## Purpose

Reduce repetitive surface creation, boundary selection,
surface repair, and naming steps.

## Features

- Processes multiple boundaries in a loop.
- Supports one or more source pointcloud objects.
- Relimits each surface to its boundary polygon.
- Trims large triangles using a configurable maximum edge length.
- Runs Fix Surface on each generated surface.
- Names each result: Surface <boundary name>.
- Checks input paths and duplicate boundary names.

## Requirements

- Maptek Workbench with PointStudio and workflow support.
- Support for embedded Python workflow components.
- Source pointcloud objects and closed boundary polygons.

The supplied file records Maptek Workbench 2025.1.
Compatibility with other versions should be checked.

## Inputs

| Input | Description |
|---|---|
| Pointcloud / scan(s) | Full object paths; separate multiple paths with commas |
| Boundary polygon(s) | Full polygon paths; separate multiple paths with commas |
| Folder hasil surface | Destination container inside PointStudio; default: /surfaces |
| Maximum edge length (m) | Maximum triangle edge length; default: 5 metres |

## Usage

1. Open the WFD file in Maptek Workbench.
2. Run the workflow with the relevant PointStudio project open.
3. Enter the source pointcloud object paths.
4. Enter the boundary polygon paths.
5. Set the destination container and maximum edge length.
6. Continue the workflow.
7. Inspect the generated surfaces in the destination container.

Each boundary must have a unique name.
Destination paths refer to PointStudio containers,
not Windows folders.

## Output

A separate surface for each processed boundary,
named Surface <boundary name>.
