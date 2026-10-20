## Automatic Volume Calculation per Request Level

A Maptek PointStudio workflow that automatically matches Top and Base/Bottom surfaces, repairs each pair, calculates volumes, and exports individual CSV reports.

## Purpose

Reduce repetitive surface selection and report setup when calculating volumes for multiple Request Levels (RL) or survey areas.

## Features

- Match surfaces by name rather than input order.
- Accept both Base and Bottom naming prefixes.
- Validate that every Top surface has a matching reference surface.
- Run Fix Surface on both surfaces before calculation.
- Apply optional polygon constraints.
- Export one CSV report per surface pair.

## Surface Naming

Surface names must follow these patterns:

- `Top <pair name>`
- `Base <pair name>` or `Bottom <pair name>`

Examples:

| Top surface | Matching reference surface | Report |
| --- | --- | --- |
| Top RL 234 LIM | Base RL 234 LIM | Volume RL 234 LIM.csv |
| Top Selective 2 | Bottom Selective 2 | Volume Selective 2.csv |

Matching is case-insensitive. Input order does not need to match.

The prefix `Bot` is not supported in this version.

## Inputs

| Input | Description |
| --- | --- |
| Top surface(s) | Full paths to Top surface objects, separated by commas |
| Base / Bottom surface(s) | Full paths to matching reference surfaces, separated by commas |
| Boundary polygon(s) | Optional closed polygon paths, separated by commas |
| Report folder | An existing Windows folder for CSV reports |

Surface and boundary paths refer to objects inside PointStudio, not Windows files.

The same boundary selection applies to every surface pair in the batch. Leave it empty to calculate without polygon constraints.

## Requirements

- Maptek Workbench with PointStudio and embedded Python execution.
- An open project containing the required surfaces and optional polygons.
- An existing, writable report folder.

The workflow was saved with Maptek Workbench 2025.1.

## Usage

1. Open the WFD file in Maptek Workbench.
2. Run it with the relevant PointStudio project open.
3. Enter or drag the Top surface object paths into the setup panel.
4. Enter or drag the corresponding Base/Bottom surface paths.
5. Add boundary polygons if required.
6. Set the report folder to a location on your computer.
7. Continue the workflow.
8. Review the CSV reports in the selected folder.

## Processing

For each Top surface, the workflow:

1. Finds its matching Base/Bottom surface.
2. Prepares the report filename.
3. Runs Fix Surface on both input surfaces.
4. Calculates surface volume with or without polygon constraints.
5. Writes the CSV report.

Fix Surface is configured to repair self-intersections, trifurcations, and facet normals. Vertical facet collapse is disabled.

## Output

One CSV report per pair, named:

`Volume <pair name>.csv`

The Surface Volume command provides total cut, total fill, and total difference values.

## Notes

- Fix Surface operates directly on the selected input surfaces.
- Pair names must be unique within each Top and Base/Bottom list.
- Every Top must have a corresponding Base/Bottom, and vice versa.
- Pair names must be valid for Windows report filenames.
- Change the report folder before running; the saved default is specific to the original computer.
