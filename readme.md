# MIDI to CSV Converter

A Python utility that converts MIDI files to CSV format, extracting note information including pitch, timing, and velocity.

## Features

- Converts MIDI files to CSV format
- Extracts note information including:
  - Pitch (MIDI note number)
  - Start time (in seconds)
  - End time (in seconds)
  - Velocity (note intensity)
- Supports multiple tracks within a MIDI file
- Preserves timing information with high precision

## Requirements

- Python 3.x
- Required Python packages (install using pip):
  - music21
  - pandas

## Installation

1. Clone this repository or download the source code
2. Install the required dependencies:

```bash
pip install -r requirements.txt
```

## Usage

Run the script with the following command:

```bash
python midi_to_csv.py --midi-file file.mid --output-file file.csv --track-name "MIDI"
```

### Arguments

- `--midi-file`: Path to the input MIDI file (required)
- `--output-file`: Path to the output CSV file (optional, defaults to same name as MIDI file with .csv extension)
- `--track-name`: Name of the track to convert (required)

### Output Format

The generated CSV file will contain the following columns:
- `ps`: MIDI pitch number
- `note_start`: Start time in seconds
- `note_end`: End time in seconds
- `velocity`: Note velocity (0-127)

## Example

```bash
python midi_to_csv.py --midi-file example.mid --output-file example.csv --track-name "Piano"
```

This will create a CSV file containing all the note information from the "Piano" track in the MIDI file.



