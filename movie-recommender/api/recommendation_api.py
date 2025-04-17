from flask import Flask, jsonify, request
from flask_cors import CORS
import pandas as pd
import pickle
import sys
from pathlib import Path




sys.path.append(str(Path(__file__).parent.parent))

from model.data_processing import load_and_clean_data, fetch_posters
from model.recommendation_engine import RecommendationEngine
import logging

app = Flask(__name__)

CORS(app, resources={
    r"/api/*": {
        "origins": ["http://localhost:8090", "http://localhost:4200"],
        "allow_headers": ["*"],
        "methods": ["GET", "POST"]
    }
})



logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

engine = None

def initialize_api():
    global engine
    try:
        movies_data = load_and_clean_data()
        ratings_df = pd.read_csv("data/ratings.csv")
        
        if ratings_df.empty or movies_data.empty:
            raise ValueError("Movies or ratings data is empty!")
        
        movies_data = fetch_posters(movies_data)
        
        engine = RecommendationEngine(movies_data, ratings_df)
        
        model_path = str(Path(__file__).parent.parent / "model/reco_model.pkl")
        engine.load_models(model_path)
        
        logger.info("API initialization completed successfully")
    except Exception as e:
        logger.error(f"Initialization failed: {str(e)}")
        raise

@app.route('/api/health')
def health_check():
    return jsonify({"status": "healthy", "model_loaded": engine is not None})



@app.route('/api/recommendations/top-rated', methods=['GET'])
def get_top_rated():
    try:
        min_ratings = request.args.get('min_ratings', default=100, type=int)
        results = engine.get_top_rated_movies(min_ratings)
        return jsonify(results.to_dict(orient='records'))
    except Exception as e:
        logger.error(f"Top rated error: {str(e)}", exc_info=True)  # Add exc_info
        return jsonify({"error": "Recommendation failed", "detail": str(e)}), 500




@app.route('/api/recommendations/hybrid/<int:user_id>', methods=['GET'])
def get_hybrid_recommendations(user_id):
    try:
        top_n = request.args.get('top_n', default=10, type=int)
        results = engine.get_hybrid_recommendations(user_id, top_n)

        results = results.where(pd.notnull(results), None)
        results['genres'] = results['genres'].apply(lambda x: x if isinstance(x, list) else [])

        return jsonify(results.to_dict(orient='records'))

    except Exception as e:
        logger.error(f"Hybrid error: {str(e)}", exc_info=True)
        fallback = engine.get_top_rated_movies(10).head(5)
        fallback = fallback.where(pd.notnull(fallback), None)
        fallback['genres'] = fallback['genres'].apply(lambda x: x if isinstance(x, list) else [])
        return jsonify(fallback.to_dict(orient='records')), 200




@app.route('/api/recommendations/collaborative/<int:user_id>', methods=['GET'])
def get_collaborative_recommendations(user_id):
    try:
        top_n = request.args.get('top_n', default=10, type=int)
        results = engine.get_collaborative_recommendations(user_id, top_n)
        return jsonify(results.to_dict(orient='records'))
    except Exception as e:
        logger.error(f"Collaborative error for user {user_id}: {str(e)}")
        return jsonify({"error": "Recommendation failed"}), 500

@app.route('/api/movies/<int:movie_id>', methods=['GET'])
def get_movie_details(movie_id):
    try:
        movie = engine.movies_data[engine.movies_data['movieId'].astype(int) == movie_id]
        
        if movie.empty:
            return jsonify({"error": f"Movie {movie_id} not found"}), 404
            
        recommendations = engine.get_content_recommendations(movie_id)
        
        return jsonify({
            "movie": movie.iloc[0].to_dict(),
            "recommendations": recommendations.to_dict(orient='records')
        })
    except Exception as e:
        logger.error(f"Movie details error for {movie_id}: {str(e)}", exc_info=True)
        return jsonify({"error": "Movie lookup failed", "detail": str(e)}), 500


@app.route('/api/movies', methods=['GET'])
def get_all_movies():
    try:
        page = request.args.get('page', default=1, type=int)
        per_page = request.args.get('per_page', default=100, type=int)
        
        start_idx = (page - 1) * per_page
        end_idx = start_idx + per_page
        
        results = engine.movies_data.iloc[start_idx:end_idx]
        return jsonify({
            "page": page,
            "per_page": per_page,
            "total_movies": len(engine.movies_data),
            "results": results.to_dict(orient='records')
        })
    except Exception as e:
        logger.error(f"Movies list error: {str(e)}")
        return jsonify({"error": "Movie list failed"}), 500

    
if __name__ == '__main__':
    initialize_api()
    app.run(host='0.0.0.0', port=5000, threaded=True)



    

# from flask import Flask, jsonify, request
# from flask_cors import CORS
# import pandas as pd
# import pickle
# import sys
# import logging
# from pathlib import Path

# # Add the parent directory to path
# sys.path.append(str(Path(__file__).parent.parent))

# from model.data_processing import load_and_clean_data, fetch_posters
# from model.recommendation_engine import RecommendationEngine

# app = Flask(__name__)

# # Enable CORS
# CORS(app, resources={
#     r"/api/*": {
#         "origins": ["http://localhost:8090", "http://localhost:4200"],
#         "allow_headers": ["*"],
#         "methods": ["GET", "POST"]
#     }
# })

# # Load movie data for genre-based fallback recommendations
# movies_df = pd.read_csv("data/movies_all_columns.csv")
# movies_df['genres'] = movies_df['genres'].apply(lambda x: x.split('|') if isinstance(x, str) else [])
# movies_dict = movies_df.set_index('movieId').to_dict(orient='index')

# # Logging setup
# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)

# engine = None

# # Genre-based fallback recommendations
# def get_recommendations(movie_id):
#     if movie_id not in movies_dict:
#         return []

#     target_genres = set(movies_dict[movie_id]['genres'])
#     similar_movies = []

#     for mid, details in movies_dict.items():
#         if mid == movie_id:
#             continue
#         shared_genres = target_genres.intersection(details['genres'])
#         if shared_genres:
#             similar_movies.append((mid, len(shared_genres)))

#     similar_movies = sorted(similar_movies, key=lambda x: x[1], reverse=True)[:10]
#     return [movies_dict[mid] | {"movieId": mid} for mid, _ in similar_movies]

# # Initialization
# def initialize_api():
#     global engine
#     try:
#         movies_data = load_and_clean_data()
#         ratings_df = pd.read_csv("data/ratings.csv")
        
#         if ratings_df.empty or movies_data.empty:
#             raise ValueError("Movies or ratings data is empty!")
        
#         movies_data = fetch_posters(movies_data)
        
#         engine = RecommendationEngine(movies_data, ratings_df)
        
#         model_path = str(Path(__file__).parent.parent / "model/recommendation_models.pkl")
#         engine.load_models(model_path)
        
#         logger.info("API initialization completed successfully")
#     except Exception as e:
#         logger.error(f"Initialization failed: {str(e)}")
#         raise

# # Health check route
# @app.route('/api/health')
# def health_check():
#     return jsonify({"status": "healthy", "model_loaded": engine is not None})

# # Top-rated movie recommendations
# @app.route('/api/recommendations/top-rated', methods=['GET'])
# def get_top_rated():
#     try:
#         min_ratings = request.args.get('min_ratings', default=100, type=int)
#         results = engine.get_top_rated_movies(min_ratings)
#         return jsonify(results.to_dict(orient='records'))
#     except Exception as e:
#         logger.error(f"Top rated error: {str(e)}", exc_info=True)
#         return jsonify({"error": "Recommendation failed", "detail": str(e)}), 500

# # Hybrid recommendations
# @app.route('/api/recommendations/hybrid/<int:user_id>', methods=['GET'])
# def get_hybrid_recommendations(user_id):
#     try:
#         top_n = request.args.get('top_n', default=10, type=int)
#         results = engine.get_hybrid_recommendations(user_id, top_n)
        
#         results = results.where(pd.notnull(results), None)
#         results['genres'] = results['genres'].apply(lambda x: x if isinstance(x, list) else [])
        
#         return jsonify(results.to_dict(orient='records'))
    
#     except Exception as e:
#         logger.error(f"Hybrid error: {str(e)}", exc_info=True)
#         return jsonify({
#             "error": "Recommendation failed",
#             "detail": "Using fallback recommendations",
#             "fallback": engine.get_top_rated_movies(10).head(5).to_dict(orient='records')
#         }), 200

# # Collaborative recommendations
# @app.route('/api/recommendations/collaborative/<int:user_id>', methods=['GET'])
# def get_collaborative_recommendations(user_id):
#     try:
#         top_n = request.args.get('top_n', default=10, type=int)
#         results = engine.get_collaborative_recommendations(user_id, top_n)
#         return jsonify(results.to_dict(orient='records'))
#     except Exception as e:
#         logger.error(f"Collaborative error for user {user_id}: {str(e)}")
#         return jsonify({"error": "Recommendation failed"}), 500

# # Movie details and genre-based fallback recommendations
# @app.route("/api/movies/<int:movie_id>", methods=["GET"])
# def get_movie_details(movie_id):
#     movie = movies_dict.get(movie_id)
#     if not movie:
#         return jsonify({"error": "Movie not found"}), 404

#     recommendations = get_recommendations(movie_id)

#     return jsonify({
#         "movie": movie | {"movieId": movie_id},
#         "recommendations": recommendations
#     })

# # Get all movies with pagination
# @app.route('/api/movies', methods=['GET'])
# def get_all_movies():
#     try:
#         page = request.args.get('page', default=1, type=int)
#         per_page = request.args.get('per_page', default=100, type=int)
        
#         start_idx = (page - 1) * per_page
#         end_idx = start_idx + per_page
        
#         results = engine.movies_data.iloc[start_idx:end_idx]
#         return jsonify({
#             "page": page,
#             "per_page": per_page,
#             "total_movies": len(engine.movies_data),
#             "results": results.to_dict(orient='records')
#         })
#     except Exception as e:
#         logger.error(f"Movies list error: {str(e)}")
#         return jsonify({"error": "Movie list failed"}), 500

# # Run the Flask app
# if __name__ == '__main__':
#     initialize_api()
#     app.run(host='0.0.0.0', port=5000, threaded=True)




