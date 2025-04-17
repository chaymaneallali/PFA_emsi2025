import pandas as pd
import requests
import json
import time
from pathlib import Path

# --- CONFIGURATION ---
TMDB_API_KEY = "5c98496341763fd19721ae7b3afc2a5c"

# File paths (adjust these paths based on your directory structure)
MOVIES_WITH_POSTERS = Path(r"C:\Users\walid\OneDrive\Bureau\New_Pfa\movie-recommender\notebooks\movies_with_posters.csv")
LINKS_CSV = Path(r"C:\Users\walid\OneDrive\Bureau\New_Pfa\movie-recommender\data\links.csv")
OUTPUT_JSON = Path(r"C:\Users\walid\OneDrive\Bureau\New_Pfa\movie-recommender\data\movies_full.json")

# --- FUNCTIONS ---

def fetch_movie_details(tmdb_id):
    """
    Given a TMDB movie id, fetch details from TMDB.
    Returns a dictionary with:
      - overview, release_year, duration, language, tmdb_rating, vote_count
    """
    url = f"https://api.themoviedb.org/3/movie/{tmdb_id}"
    params = {"api_key": TMDB_API_KEY, "language": "en-US"}
    try:
        response = requests.get(url, params=params, timeout=10)
        if response.status_code == 200:
            data = response.json()
            details = {
                "overview": data.get("overview"),
                "release_year": data.get("release_date", "")[:4] if data.get("release_date") else None,
                "duration": data.get("runtime"),
                "language": data.get("original_language"),
                "tmdb_rating": data.get("vote_average"),
                "vote_count": data.get("vote_count")
            }
            return details
    except Exception as e:
        print(f"Error fetching details for TMDB ID {tmdb_id}: {e}")
    return {
        "overview": None,
        "release_year": None,
        "duration": None,
        "language": None,
        "tmdb_rating": None,
        "vote_count": None
    }

def generate_full_movie_details():
    # Load movies with posters.
    movies_df = pd.read_csv(MOVIES_WITH_POSTERS)
    # Load links (that provide tmdbId for each movie)
    links_df = pd.read_csv(LINKS_CSV)
    
    # Merge the two datasets on movieId so that we can access tmdbId for each movie.
    merged_df = pd.merge(movies_df, links_df[["movieId", "tmdbId"]], on="movieId", how="left")
    
    # Ensure that tmdbId is numeric (if it's not, convert it)
    merged_df["tmdbId"] = pd.to_numeric(merged_df["tmdbId"], errors="coerce")
    
    full_records = []
    total = len(merged_df)
    print(f"Processing {total} movies from merged datasets...")
    
    for idx, row in merged_df.iterrows():
        movie_id = row["movieId"]
        title = row["title"]
        genres = row["genres"]        # Assume this is a string (you can split later as needed)
        poster_path = row["poster_path"]
        
        # Retrieve tmdbId from the merged data.
        tmdb_id = row.get("tmdbId")
        extra = {}
        if pd.notnull(tmdb_id) and tmdb_id != 0:
            extra = fetch_movie_details(int(tmdb_id))
            # Pause briefly to avoid hitting TMDB rate limits.
            time.sleep(0.25)
        else:
            print(f"No valid TMDB id for movie: {title}")

        record = {
            "movieId": movie_id,
            "title": title,
            "genres": genres,
            "poster_path": poster_path,
            **extra
        }
        full_records.append(record)
        print(f"[{idx+1}/{total}] Processed: {title}")

    # Write the full records to a JSON file.
    with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
        json.dump(full_records, f, indent=4)
    print(f"Full movie details JSON has been written to: {OUTPUT_JSON}")

if __name__ == "__main__":
    generate_full_movie_details()
