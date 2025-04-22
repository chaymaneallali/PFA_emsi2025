// src/app/home/home.component.ts
import { Component, OnInit } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { Router } from '@angular/router';
import { NavbarComponent } from '../navbar/navbar.component';
import { MovieService } from '../service/movie.service';
import { CommonModule } from '@angular/common';

@Component({
  standalone: true,
  imports: [CommonModule, FormsModule, NavbarComponent],
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.css']
})
export class HomeComponent implements OnInit {
  searchTerm = '';
  topRatedMovies: any[] = [];
  hybridRecommendations: any[] = [];
  allMovies: any[] = [];
  collaborativeRecommendations: any[] = [];


  loading = {
    topRated: true,
    hybrid: true,
    allMovies: true,
    collaborative: true

  };

  errors = {
    topRated: '',
    hybrid: '',
    allMovies: '',
    collaborative: ''

  };

  constructor(private movieService: MovieService, private router: Router) {}

  ngOnInit(): void {
    this.loadInitialData();
  }

  private loadInitialData(): void {
    this.loadTopRated();
    this.loadHybridRecommendations();
    this.loadAllMovies();
    this.loadCollaborativeRecommendations(); // New

  }


  private loadCollaborativeRecommendations(): void {
    this.movieService.getCollaborativeRecommendations().subscribe({
      next: (movies) => {
        this.collaborativeRecommendations = this.transformMovieData(movies);
        this.loading.collaborative = false;
      },
      error: () => {
        this.handleError('collaborative', 'Failed to load recommendations');
      }
    });
  }



  private loadTopRated(): void {
    this.movieService.getTopRated().subscribe({
      next: (movies) => {
        this.topRatedMovies = this.transformMovieData(movies);
        this.loading.topRated = false;
      },
      error: () => {
        this.handleError('topRated', 'Failed to load top rated movies');
      }
    });
  }

  private loadHybridRecommendations(): void {
    this.movieService.getHybridRecommendations().subscribe({
      next: (movies) => {
        this.hybridRecommendations = this.transformMovieData(movies);
        this.loading.hybrid = false;
      },
      error: () => {
        this.handleError('hybrid', 'Failed to load recommendations');
      }
    });
  }

  private loadAllMovies(): void {
    this.movieService.getAllMovies().subscribe({
      next: (response) => {
        this.allMovies = this.transformMovieData(response.results);
        this.loading.allMovies = false;
      },
      error: () => {
        this.handleError('allMovies', 'Failed to load movies');
      }
    });
  }

  private transformMovieData(movies: any[]): any[] {
    return movies.map(movie => ({
      movieId: movie.movieId || movie.id,
      title: movie.title,
      genres: movie.genres || [],
      poster_path: movie.poster_path || 'assets/no-image.jpg',
      avg_rating: movie.avg_rating || 0,
      num_ratings: movie.num_ratings || 0
    }));
  }

  private handleError(section: keyof typeof this.errors, message: string): void {
    this.errors[section] = message;
    this.loading[section] = false;
    console.error(message);
  }

  viewMovieDetails(movieId: number): void {
    this.router.navigate(['/movies', movieId]);
  }

  searchMovies(): void {
    console.log('Search initiated for:', this.searchTerm);
    // Implement further search functionality as needed
  }
}
