#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from IPython.display import display
from pathlib import Path



# In[2]:


import sys
sys.path.append(str(Path.cwd().parent))
from data_processing import load_and_clean_data
from recommendation_engine import RecommendationEngine

# In[3]:

movies_data = load_and_clean_data()
ratings_df = pd.read_csv('../data/ratings.csv')

# In[4]:


print("Movies Data:")
display(movies_df.head(2))
print("\nRatings Data:")
display(ratings_df.head(2))


# In[5]:


# Data preprocessing
movies_data = load_and_clean_data()
movies_data = fetch_posters(movies_data)


# In[6]:


genre_counts = pd.Series([genre for genres in movies_data['genres'] for genre in genres]).value_counts()

plt.figure(figsize=(12,6))
sns.barplot(x=genre_counts.values, y=genre_counts.index, palette='viridis')
plt.title('Movie Genre Distribution')
plt.xlabel('Count')
plt.ylabel('Genre')
plt.show()


# In[7]:


# Ratings analysis
plt.figure(figsize=(10,6))
sns.countplot(x='rating', data=ratings_df, palette='coolwarm')
plt.title('User Rating Distribution')
plt.show()


# In[8]:


engine = RecommendationEngine(movies_data, ratings_df)
engine.initialize_models()


# In[9]:


# Content-based filtering test
def test_content_recommendations(movie_title):
    results = engine.search_by_title(movie_title)
    print(f"Recommendations for '{movie_title}':")
    display(results[['title', 'genres', 'poster_path']])

test_content_recommendations("Toy Story")


# In[10]:


# Collaborative filtering test
def test_collaborative_recommendations(user_id):
    results = engine.get_collaborative_recommendations(user_id)
    print(f"Recommendations for user {user_id}:")
    display(results[['title', 'genres', 'poster_path', 'avg_rating']])

test_collaborative_recommendations(1)


# In[27]:


# Hybrid recommendations test
def test_hybrid_recommendations(user_input):
    results = engine.hybrid_recommendation(user_input)
    print(f"Hybrid recommendations based on '{user_input}':")
    display(results[['title', 'genres', 'poster_path', 'score']])

test_hybrid_recommendations("Matrix")


# In[12]:


# Model persistence test
engine.save_models("../model/recommendation_models.pkl")


# In[13]:


# Verify model loading
new_engine = RecommendationEngine(movies_data, ratings_df)
new_engine.load_models("../model/recommendation_models.pkl")


# In[14]:


get_ipython().system('jupyter nbconvert --to script model.ipynb --output-dir ../model')


# In[19]:


import requests
import json


# In[20]:


def get_tmdb_id(imdb_id):
    try:
        response = requests.get(
            f"https://api.themoviedb.org/3/find/{imdb_id}",
            params={
                "api_key": "5c98496341763fd19721ae7b3afc2a5c",
                "external_source": "imdb_id"
            }
        )
        if response.status_code == 200:
            return response.json()['movie_results'][0]['id']
        return None
    except Exception as e:
        print(f"Error fetching TMDB ID for IMDb {imdb_id}: {str(e)}")
        return None

# In your data processing:
def load_and_clean_data():
    movies_df = pd.read_csv('../data/movies.csv')
    links_df = pd.read_csv('../data/links.csv')

    # Convert IMDb IDs to proper format
    links_df['imdbId'] = links_df['imdbId'].apply(lambda x: f"tt{x:07d}")

    # Fetch missing TMDB IDs
    missing_tmdb = links_df[links_df['tmdbId'].isna()]
    for idx, row in missing_tmdb.iterrows():
        tmdb_id = get_tmdb_id(row['imdbId'])
        if tmdb_id:
            links_df.at[idx, 'tmdbId'] = tmdb_id

    # Merge datasets
    movies_data = movies_df.merge(
        links_df[['movieId', 'tmdbId']], 
        on='movieId', 
        how='left'
    )

    # Rest of your processing...
    return movies_data


# In[21]:


test_tmdb_id = 862  # TMDB ID for Toy Story
response = requests.get(
    f"https://api.themoviedb.org/3/movie/{test_tmdb_id}",
    params={"api_key": "5c98496341763fd19721ae7b3afc2a5c"}
)
print("API Response:", response.status_code)  # Should be 200
print("Poster Path:", response.json().get('poster_path'))  # Should show a path


# In[22]:


try:
    with open('poster_cache.json', 'r') as f:
        cache = json.load(f)
    print(f"Found {len(cache)} cached entries")
except FileNotFoundError:
    print("No cache file found - it will be created during processing")
except Exception as e:
    print(f"Error loading cache: {str(e)}")


# In[25]:


# Final verification after fixes
movies_data = load_and_clean_data()
movies_data = fetch_posters(movies_data)

print("\nPoster coverage statistics:")
print(f"Total movies: {len(movies_data)}")
print(f"Movies with posters: {movies_data['poster_path'].notna().sum()}")
print(f"Coverage: {movies_data['poster_path'].notna().mean():.1%}")

print("\nSample movies with posters:")
display(movies_data[movies_data['poster_path'].notna()][['title', 'poster_path']].sample(5))


# In[26]:


# Check cache hit rate
cached_ids = set(movies_data['tmdbId'].astype(str))
cache_hits = len([id for id in cached_ids if str(id) in cache])
print(f"Cache hits: {cache_hits}/{len(cached_ids)}")





# %%print("Movies Data:")
display(movies_data[['movieId', 'title', 'genres', 'release_year', 'tmdb_rating']].head(2))

# %%
