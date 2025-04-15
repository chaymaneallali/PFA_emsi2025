import pandas as pd
import json
from pathlib import Path

# File paths should match those used in step 1.
INPUT_JSON = Path(r"C:\Users\walid\OneDrive\Bureau\New_Pfa\movie-recommender\data\movies_full.json")
OUTPUT_CSV = Path(r"C:\Users\walid\OneDrive\Bureau\New_Pfa\movie-recommender\data\movies_all_columns.csv")

def convert_json_to_csv():
    with open(INPUT_JSON, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    # Create a DataFrame and save to CSV.
    df = pd.DataFrame(data)
    df.to_csv(OUTPUT_CSV, index=False)
    print(f"CSV file created at: {OUTPUT_CSV}")

if __name__ == "__main__":
    convert_json_to_csv()
