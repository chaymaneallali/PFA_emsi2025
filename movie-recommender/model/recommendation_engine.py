import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pickle


    # def get_collaborative_recommendations(self, user_id, top_n=10):
    #     user_ratings = self.ratings_df[self.ratings_df['userId'] == user_id]
    #     top_rated = user_ratings[user_ratings['rating'] >= 4.0]
    #     top_movies = top_rated.merge(self.movies_data, on='movieId')

    #     avg_ratings = self.ratings_df.groupby('movieId')['rating'].mean().reset_index()

    #     avg_ratings.columns = ['movieId', 'avg_rating']

    #     top_movies = top_movies.merge(avg_ratings, on='movieId', how='left')

    #     return top_movies.sort_values(by='rating', ascending=False).head(top_n)

class RecommendationEngine:
    def __init__(self, movies_data, ratings_df):
        self.movies_data = movies_data
        self.ratings_df = ratings_df
        self.vectorizer_title = None
        self.vectorizer_genres = None
        self.tfidf_title = None
        self.tfidf_genres = None

    def initialize_models(self):
        # Title vectorizer
        self.vectorizer_title = TfidfVectorizer(ngram_range=(1, 2))
        self.tfidf_title = self.vectorizer_title.fit_transform(self.movies_data['title'])
        
        # Genres vectorizer
        self.movies_data['genres_text'] = self.movies_data['genres'].apply(lambda x: ' '.join(x))
        self.vectorizer_genres = TfidfVectorizer(ngram_range=(1, 2))
        self.tfidf_genres = self.vectorizer_genres.fit_transform(self.movies_data['genres_text'])

    def save_models(self, path="reco_model.pkl"):
        with open(path, "wb") as f:
            pickle.dump({
                "vectorizer_title": self.vectorizer_title,
                "tfidf_title": self.tfidf_title,
                "vectorizer_genres": self.vectorizer_genres,
                "tfidf_genres": self.tfidf_genres
            }, f)



    def load_models(self, path="model/recommendation_models.pkl"):
        with open(path, "rb") as f:
            models = pickle.load(f)
            self.vectorizer_title = models["vectorizer_title"]
            self.tfidf_title = models["tfidf_title"]
            self.vectorizer_genres = models["vectorizer_genres"]
            self.tfidf_genres = models["tfidf_genres"]

    def search_by_title(self, title_query, top_n=10):
        tfidf_query = self.vectorizer_title.transform([title_query])
        similarities = cosine_similarity(tfidf_query, self.tfidf_title).flatten()
        top_indices = similarities.argsort()[::-1][:top_n]

        results = self.movies_data.iloc[top_indices].copy()
        results['similarity'] = similarities[top_indices]
        return results


    



    
    def get_collaborative_recommendations(self, target_user_id, top_n=10):
    # Create a pivot table: rows are userIds, columns are movieIds
        user_item_matrix = self.ratings_df.pivot(index='userId', columns='movieId', values='rating').fillna(0)
    
    # Compute cosine similarity between users
        user_sim_matrix = cosine_similarity(user_item_matrix)
    # Create a DataFrame for easy look-up
        user_sim_df = pd.DataFrame(user_sim_matrix, index=user_item_matrix.index, columns=user_item_matrix.index)

    # Get similar users for the target (exclude the target themselves)
        similar_users = user_sim_df[target_user_id].drop(target_user_id).sort_values(ascending=False)
        top_similar_users = similar_users.head(10)  # consider top 10 similar users

    # Get movies the target user has already rated
        rated_movies = set(self.ratings_df[self.ratings_df['userId'] == target_user_id]['movieId'])

    # Aggregate weighted scores for movies not rated by the target user
        recommendation_scores = {}
        for similar_user, similarity in top_similar_users.items():
        # Retrieve the ratings for the similar user
            user_ratings = self.ratings_df[self.ratings_df['userId'] == similar_user]
            for _, row in user_ratings.iterrows():
                movie_id = row['movieId']
                rating = row['rating']
                if movie_id in rated_movies:
                    continue
            # Use similarity * rating as a weighted contribution
                recommendation_scores[movie_id] = recommendation_scores.get(movie_id, 0) + similarity * rating

    # Convert aggregated scores into a DataFrame and sort descending by score
        recs = pd.DataFrame(list(recommendation_scores.items()), columns=['movieId', 'collab_score'])
        recs = recs.sort_values('collab_score', ascending=False).head(top_n)

    # Merge with the movies dataset to add movie details (like title, genres, etc.)
        recs = recs.merge(self.movies_data, on='movieId', how='left')
        return recs





    


    def get_top_rated_movies(self, min_ratings=100):
        rating_counts = self.ratings_df.groupby('movieId')['rating'] \
            .agg(num_ratings=('count'), avg_rating=('mean')) \
            .reset_index()\
            .rename(columns={'count': 'num_ratings', 'mean': 'avg_rating'})
    
    # Filter movies with minimum ratings
        filtered = rating_counts[rating_counts['num_ratings'] >= min_ratings]
    
    # Merge with movie data
        return filtered.merge(
            self.movies_data,
            on='movieId',
            how='left'
        ).sort_values('avg_rating', ascending=False)


    def get_content_recommendations(self, movie_id, top_n=10):
        movie_idx = self.movies_data[self.movies_data['movieId'] == movie_id].index[0]
    
        title_sim = cosine_similarity(
            self.tfidf_title[movie_idx], 
            self.tfidf_title
        ).flatten()
    
        genre_sim = cosine_similarity(
            self.tfidf_genres[movie_idx], 
            self.tfidf_genres
        ).flatten()
    
        combined_sim = 0.6 * title_sim + 0.4 * genre_sim
    
        similar_indices = combined_sim.argsort()[::-1][1:top_n+1]
        return self.movies_data.iloc[similar_indices]









def get_hybrid_recommendations(self, user_id, top_n=10):
    try:
        # Collaborative recommendations (new version)
        collab_recs = self.get_collaborative_recommendations(user_id, top_n=30)
        collab_recs = collab_recs[['movieId', 'collab_score']]

        # Content-based part: Get user's top-rated movies (e.g., ratings >= 4.0)
        user_top_rated = self.ratings_df[(self.ratings_df['userId'] == user_id) & (self.ratings_df['rating'] >= 4.0)]
        top_rated_movie_ids = user_top_rated['movieId'].unique()

        # Collect content recommendations from each top-rated movie
        content_recs_list = []
        for movie_id in top_rated_movie_ids:
            try:
                recs = self.get_content_recommendations(movie_id, top_n=10)
                # get only movieId and its similarity column (rename as content_score)
                recs = self.get_content_recommendations(movie_id, top_n=10).copy()                # If get_content_recommendations originally returns a 'similarity' column,
                # here we assume that column represents the content-based score.
                recs['content_score'] = self.tfidf_title[movie_id].dot(self.tfidf_title.T).A.flatten()[movie_id] \
                    if movie_id < self.tfidf_title.shape[0] else 0

                content_recs_list.append(recs)
            except Exception:
                continue

        if len(content_recs_list) > 0:
            content_recs = pd.concat(content_recs_list)
            # Combine scores if the same movie appears from several top-rated movies
            content_recs = content_recs.groupby('movieId', as_index=False).agg({'content_score':'mean'})
        else:
            content_recs = pd.DataFrame(columns=['movieId', 'content_score'])

        # Merge collaborative and content recommendations (outer join)
        merged_recs = pd.merge(collab_recs, content_recs, on='movieId', how='outer').fillna(0)

        # Compute a hybrid score (using equal weighting here, adjust as needed)
        merged_recs['hybrid_score'] = 0.5 * merged_recs['collab_score'] + 0.5 * merged_recs['content_score']

        merged_recs = merged_recs.sort_values('hybrid_score', ascending=False).head(top_n)
        # Merge with movie details
        merged_recs = merged_recs.merge(self.movies_data, on='movieId', how='left')
        return merged_recs

    except Exception as e:
        print(f"Hybrid error: {str(e)}")
        # Fallback in case of error: return top-rated movies
        return self.get_top_rated_movies(10).head(top_n)



