# Stake Out CSV Format Merger

Combines Stake Out point CSV Format into one file
ready for import into Maptek PointStudio.

## Features

- Combines CSV files from a selected folder.
- Renumbers points sequentially from 1000.
- Preserves the original coordinate digits.
- Removes RTCM reference rows.
- Skips rows with missing or non-numeric X, Y, or Z.
- Replaces empty descriptions with 0.

## Output Format

P, X, Y, Z, Description — without a header row.

## Requirements

Python 3 with Tkinter. No additional packages are required.

## Usage

1. Extract the raw CSV files into one folder.
2. Open the Python script in IDLE.
3. Press F5 and select the raw data folder.
4. Check the processing summary and output CSV.
