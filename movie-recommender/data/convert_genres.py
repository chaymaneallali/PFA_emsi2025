#!/usr/bin/env python
# coding: utf-8

import pandas as pd
import ast
from pathlib import Path

def clean_genres(val):
    """
    Convert the genres value (likely a string representation of a list) into a normalized string.
    
    The function will:
      1. Try to use ast.literal_eval if the value starts with '[' and ends with ']'.
      2. Otherwise, try to split by '|' or comma.
      3. Return a string with genres separated by a single space.
    """
    if isinstance(val, str):
        val = val.strip()
        if not val:
            return "unknown"
        # Try literal_eval if enclosed in brackets.
        if val.startswith('[') and val.endswith(']'):
            try:
                parsed = ast.literal_eval(val)
                # Make sure we have a list with nonempty strings
                genres = [str(g).strip() for g in parsed if str(g).strip()]
                if genres:
                    return " ".join(genres)
            except Exception:
                pass  # If literal_eval fails, continue below.
        # If no bracket format, try splitting by '|'
        if '|' in val:
            genres = [g.strip() for g in val.split('|') if g.strip()]
            if genres:
                return " ".join(genres)
        # Alternatively, try splitting by comma
        if ',' in val:
            genres = [g.strip() for g in val.split(',') if g.strip()]
            if genres:
                return " ".join(genres)
        # Otherwise, return the original value
        return val
    return "unknown"

def convert_csv(input_file, output_file):
    """
    Reads a CSV input file, cleans its genres column, and writes to an output file.
    Assumes the input file has a column called 'genres'.
    """
    df = pd.read_csv(input_file)
    if 'genres' not in df.columns:
        raise ValueError("Column 'genres' not found in the CSV file.")
    
    # Create a new column with the cleaned genres
    df['genres_clean'] = df['genres'].apply(clean_genres)
    # Option: Replace the original genres or add the new column.
    # Here we replace the 'genres' column.
    df['genres'] = df['genres_clean']
    df.drop(columns=['genres_clean'], inplace=True)
    
    # Write out the cleaned CSV.
    df.to_csv(output_file, index=False)
    print(f"Converted CSV written to {output_file}")

if __name__ == '__main__':
    # Adjust these paths as needed.
    data_dir = Path(__file__).parent / "data"
    input_csv = 'movies_all_columns.csv'
    output_csv = "movies_full_clean.csv"
    
    convert_csv(input_csv, output_csv)
