from music21 import *
import pandas as pd
import os
import argparse

def midi_to_csv(midi_name, track_index, output_file):
    """
    Convert a MIDI file to CSV for a given track.
    
    Parameters:
      midi_name (str): The MIDI file name.
      track_index (int): The index of the track to process.
      output_file (str): The output file name.
    """

    file = converter.parse(midi_name)
    tempo_feature = features.jSymbolic.InitialTempoFeature(file)
    tempo = tempo_feature.extract().vector[0]
    
    # Create a DataFrame with the required columns.
    columns = ["ps", "note_start", "note_end", "velocity"]
    df = pd.DataFrame(columns=columns)
    
    part = file.parts[track_index]
    
    def add_note(midi, note_start, note_end, velocity):
        """
        Add a note to the DataFrame if it doesn't exist; otherwise 
        update the note_end.
        """
        # Define conditions separately for readability
        cond1 = (df.note_end == note_start) & (df.ps == midi)
        cond2 = (df.note_start == note_start) & (df.ps == midi)
        
        # Check if note exists
        if len(df[cond1 | cond2]) == 0:
            df.loc[len(df)] = [midi, note_start, note_end, velocity]
        # Update existing note
        elif len(df[cond1]) > 0:
            df.loc[cond1, 'note_end'] = note_end

    # Process each measure in the specified part.
    for measure in part.getElementsByClass(stream.Measure):
        measure.show("text")
        for a in measure.recurse().notes:
            if a.isNote:
                offset = a.offset + measure.offset
                length = a.duration.quarterLength
                note_start = (offset / tempo) * 60
                note_end = ((offset + length) / tempo) * 60
                velocity = a.volume.velocity
                pitch = a.pitch.midi
                add_note(pitch, note_start, note_end, velocity)
            if a.isChord:
                offset = a.offset + measure.offset
                note_start = (offset / tempo) * 60
                length = a.duration.quarterLength
                note_end = ((offset + length) / tempo) * 60
                velocity = a.volume.velocity
                for n in a._notes:
                    pitch = n.pitch.midi
                    add_note(pitch, note_start, note_end, velocity)
    
    # Sort and prepare the DataFrame for CSV export.
    df = df.sort_values(by=['note_start'])
    df = df.astype({
        "ps": "int", 
        "note_start": "float",
        "note_end": "float", 
        "velocity": "int"
    })
    df.to_csv(path_or_buf=output_file, float_format='%.12f')

def main():
    """
    Main entry point: parses command-line arguments, verifies directories,
    and performs the MIDI-to-CSV conversion.
    
    Example usage:
      python midi_to_csv.py --file file.mid --track "MIDI" --output-file file.csv
    """
    parser = argparse.ArgumentParser(
        description="Convert a MIDI file to CSV"
    )
    parser.add_argument(
        "--midi-file", 
        required=True, 
        help="The MIDI file to convert (e.g., file.mid)"
    )
    parser.add_argument(
        "--output-file", 
        required=False, 
        help="The output file name (e.g., file.csv)"
    )
    parser.add_argument(
        "--track-name", 
        required=True, 
        help="The track name to convert (e.g., MIDI)"
    )
    args = parser.parse_args()

    track_name = args.track_name
    midi_file = args.midi_file
    output_file = args.output_file

    if not output_file:
        output_file = midi_file.replace("mid", "csv")
   
    # Parse the MIDI file and display track names.
    file = converter.parse(midi_file)
    track_info = [
        (index, part.partName) 
        for index, part in enumerate(file.parts)
    ]
    print("Track names: ", track_info)
    
    # Retrieve the track index from the track name.
    try:
        track_index = [
            part.partName for part in file.parts
        ].index(track_name)
    except ValueError:
        print(f"Track '{track_name}' not found in {midi_file}.")
        return

    # Convert the MIDI to CSV.
    midi_to_csv(midi_file, track_index, output_file)

if __name__ == "__main__":
    main()

    
# ps,note_start,note_end,velocity
# 0,57.00000000,3.75675676,3.76013514,61.00000000
# 1,67.00000000,3.75675676,3.76013514,61.00000000