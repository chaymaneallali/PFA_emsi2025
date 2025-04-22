


// src/app/service/movie.service.ts
import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, of, catchError, throwError } from 'rxjs';
import { AuthService } from './auth.service';
import { MovieDetailsResponse } from '../model/movie.model';

@Injectable({ providedIn: 'root' })
export class MovieService {
  private apiUrl = 'http://localhost:8090/api/movies';

  constructor(private http: HttpClient, private authService: AuthService) {}

  // Get Top Rated Movies (horizontally scrolling list)
  // point at your Spring Boot route:
getTopRated(): Observable<any[]> {
  return this.http.get<any[]>(`${this.apiUrl}/top-rated`)
    .pipe(
      catchError(error => {
        console.error('Error fetching top rated:', error);
        return throwError(() => new Error('Failed to load top rated movies'));
      })
    );
}

  

  // Get Hybrid Recommendations (horizontally scrolling list)
  getHybridRecommendations(): Observable<any[]> {
    const token = this.authService.getToken();
    if (!token) throw new Error('No token available');

    const decoded = this.authService.jwtHelper.decodeToken(token);
    console.log('Decoded token:', decoded);  // <-- Temporary log
    const userId = decoded?.userId || decoded?.sub;
    if (!userId) throw new Error('User ID not found in token');
    return this.http.get<any[]>(`${this.apiUrl}/recommendations/hybrid/${userId}`).pipe(
      catchError(error => {
        console.error('Error fetching hybrid recommendations:', error);
        return throwError(() => new Error('Failed to load recommendations'));
      })
    );
  }

  // Get All Movies (vertical list)
  getAllMovies(page: number = 1, perPage: number = 100): Observable<any> {
    return this.http.get<any>(`${this.apiUrl}?page=${page}&per_page=${perPage}`).pipe(
      catchError(error => {
        console.error('Error fetching all movies:', error);
        return throwError(() => new Error('Failed to load movies'));
      })
    );
  }

  getMovieDetails(movieId: number): Observable<MovieDetailsResponse> {
    return this.http.get<MovieDetailsResponse>(`${this.apiUrl}/${movieId}`).pipe(
      catchError(error => {
        if (error.status === 404) {
          return throwError(() => new Error('Movie not found'));
        }
        return throwError(() => new Error('Server error'));
      })
    );
  }

  getCollaborativeRecommendations(): Observable<any[]> {
    const token = this.authService.getToken();
    if (!token) throw new Error('No token available');

    const decoded = this.authService.jwtHelper.decodeToken(token);
    const userId = decoded?.userId || decoded?.sub;
    if (!userId) throw new Error('User ID not found in token');

    return this.http.get<any[]>(`${this.apiUrl}/recommendations/collaborative/${userId}`).pipe(
      catchError(error => {
        console.error('Error fetching collaborative recommendations:', error);
        return throwError(() => new Error('Failed to load recommendations'));
      })
    );
  }

  getUserRating(movieId: number): Observable<number | null> {
    return this.http.get<number>(`${this.apiUrl}/${movieId}/rating`).pipe(
      catchError(error => {
        if (error.status === 404) {
          return of(null); // No rating exists
        }
        return throwError(() => new Error('Failed to fetch rating'));
      })
    );
  }

  rateMovie(movieId: number, rating: number): Observable<any> {
    return this.http.post(`${this.apiUrl}/${movieId}/rate`, { rating }).pipe(
      catchError(error => {
        console.error('Error submitting rating:', error);
        return throwError(() => new Error('Failed to submit rating'));
      })
    );
  }

  // Corrected endpoint: remove extra '/movies'
  markMovieAsWatched(movieId: number, userId: number): Observable<any> {
    return this.http.post(`${this.apiUrl}/${movieId}/watched?userId=${userId}`, {});
  }

  markMovieAsToWatch(movieId: number, userId: number): Observable<any> {
    return this.http.post(`${this.apiUrl}/${movieId}/to-watch?userId=${userId}`, {});
  }
}


