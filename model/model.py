#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# import pandas as pd
# import numpy as np
# import matplotlib.pyplot as plt
# import seaborn as sns
# from IPython.display import display
# from pathlib import Path

import sys
from pathlib import Path
import pandas as pd



# In[2]:

sys.path.append(str(Path.cwd().parent))

from data_processing import load_and_clean_data
from recommendation_engine import RecommendationEngine

# In[3]:

movies_data = load_and_clean_data()  # This file already contains all the necessary columns.

ratings_df = pd.read_csv('../data/ratings.csv')


# In[4]:

engine = RecommendationEngine(movies_data, ratings_df)
engine.initialize_models()


# In[5]:


test_movie_id = movies_data.iloc[0]['movieId']
print(f"Content-based recommendations for movieId {test_movie_id}:")
content_recs = engine.get_content_recommendations(test_movie_id)
print(content_recs[['title', 'genres']].head())


# In[6]:

print("\nCollaborative recommendations for user 1:")
collab_recs = engine.get_collaborative_recommendations(1)
print(collab_recs[['title', 'genres']].head())

# In[7]:


model_path = "../model/reco_model.pkl"
engine.save_models(model_path)
print(f"\nModel has been saved to {model_path}")


# In[8]:


# In[9]:
