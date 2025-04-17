import pandas as pd
import re
import json
import os
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data"
TMDB_API_KEY = "5c98496341763fd19721ae7b3afc2a5c"

def load_and_clean_data():
    movies_df = pd.read_csv(DATA_DIR / "movies_full_clean.csv")
    links_df = pd.read_csv(DATA_DIR / "links.csv")
    
    movies_data = movies_df.merge(
        links_df[['movieId', 'tmdbId', 'imdbId']], 
        on='movieId', 
        how='left'
    )

    movies_data['movieId'] = movies_data['movieId'].astype(int)


    
    movies_data['title'] = movies_data['title'].apply(
        lambda x: re.sub("[^a-zA-Z0-9 ]", "", x)
    )
    
    movies_data['genres'] = movies_data['genres'].str.split('|')
    movies_data = movies_data[~movies_data['genres'].apply(
        lambda x: '(no genres listed)' in x
    )]
    
    movies_data['tmdbId'] = pd.to_numeric(movies_data['tmdbId'], errors='coerce').astype('Int64')
    movies_data['imdbId'] = movies_data['imdbId'].apply(lambda x: f"tt{x:07d}")
    
    return movies_data

def fetch_posters(movies_data):
    CACHE_FILE = BASE_DIR / "model/poster_cache.json"
    
    def fetch_poster(tmdb_id):
        if pd.isna(tmdb_id) or tmdb_id == 0:
            return None
        try:
            response = requests.get(
                f'https://api.themoviedb.org/3/movie/{tmdb_id}',
                params={'api_key': TMDB_API_KEY},
                timeout=10
            )
            if response.status_code == 200:
                return response.json().get('poster_path')
            return None
    
        except Exception as e:
            print(f"Error fetching {tmdb_id}: {str(e)}")
            return None

    cache = {}
    if CACHE_FILE.exists():
        with open(CACHE_FILE, 'r') as f:
            cache = json.load(f)
    
    tmdb_ids = movies_data['tmdbId'].dropna().unique().astype(int)
    tmdb_ids_str = [str(id) for id in tmdb_ids]
    new_ids = [id for id in tmdb_ids_str if id not in cache]
    
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = {executor.submit(fetch_poster, int(id)): id for id in new_ids if id.isdigit()}
        for future in as_completed(futures):
            movie_id = futures[future]
            try:
                cache[movie_id] = future.result()
            except:
                pass
    
    with open(CACHE_FILE, 'w') as f:
        json.dump(cache, f)
    
    movies_data['poster_path'] = movies_data['tmdbId'].apply(
        lambda x: f"https://image.tmdb.org/t/p/w500{cache.get(str(int(x)), None)}" 
        if pd.notnull(x) else None
    )

    
    
    return movies_data



