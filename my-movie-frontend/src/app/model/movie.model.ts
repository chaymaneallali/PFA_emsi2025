// src/app/models/movie.models.ts
export interface Movie {
  movieId: number;
  title: string;
  genres: string[];
  poster_path: string;
  overview: string;
  release_year: number;
  language: string;
  duration: number;
  tmdb_rating: number;
  vote_count: number;
  avg_rating?: number;
  num_ratings?: number;
}

export interface MovieDetailsResponse {
  movie: Movie;
  recommendations: Movie[];
}