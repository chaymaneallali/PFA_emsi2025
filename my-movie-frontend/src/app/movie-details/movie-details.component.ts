// // src/app/movie-details/movie-details.component.ts
// import { Component, OnInit } from '@angular/core';
// import { ActivatedRoute } from '@angular/router';
// import { NavbarComponent } from '../navbar/navbar.component';
// import { MovieService } from '../service/movie.service';
// import { CommonModule } from '@angular/common';
// import { AuthService } from '../service/auth.service';


// @Component({
//   standalone: true,
//   imports: [CommonModule, NavbarComponent],
//   templateUrl: './movie-details.component.html',
//   styleUrls: ['./movie-details.component.css']
// })
// export class MovieDetailsComponent implements OnInit {
//   movie: any;
//   recommendations: any[] = [];
//   loading = true;
//   userRating: number | null = null;
//   newRating = 0;
//   hybridRecommendations: any[] = [];

//   error = '';



  

//   constructor(public authService:AuthService ,  private route: ActivatedRoute, private movieService: MovieService) {}

//   ngOnInit(): void {
//     const movieId = this.route.snapshot.paramMap.get('id');
//     if (movieId) {
//       this.loadMovieDetails(+movieId);
//       if (this.authService.isAuthenticated()) {
//         this.loadUserRating(+movieId); // Load rating only if authenticated
//       }
//     } else {
//       this.handleError('Invalid movie ID');
//     }
//   }

  


//   rateMovie(): void {
//     this.movieService.rateMovie(this.movie.movieId, this.newRating).subscribe({
//       next: () => {
//         this.userRating = this.newRating;
//         this.newRating = 0;
//         this.loadMovieDetails(this.movie.movieId); // Refresh data
//       },
//       error: () => console.error('Failed to submit rating')
//     });
//   }

  

//   private handleError(message: string): void {
//     this.error = message;
//     this.loading = false;
//     console.error(message);
//   }


//   // movie-details.component.ts
//   private loadMovieDetails(movieId: number): void {
//     this.movieService.getMovieDetails(movieId).subscribe({
//       next: (response) => {
//         this.movie = response.movie;
//         this.recommendations = response.recommendations || [];
//         this.loading = false;
//       },
//       error: (err) => {
//         if (err.status === 404) {
//           this.handleError('Movie not found');
//         } else {
//           this.handleError('Failed to load details');
//         }
//       }
//     });
//   }


// private loadUserRating(movieId: number): void {
//   this.movieService.getUserRating(movieId).subscribe({
//     next: (rating) => this.userRating = rating,
//     error: (err) => {
//       if (err.status === 404) {
//         this.userRating = null; // No rating exists
//       } else {
//         console.error('Rating load error:', err);
//       }
//     }
//   });
// }

// private transformMovieData(movies: any[]): any[] {
//   return movies.map(movie => ({
//     movieId: movie.movieId || movie.id,
//     title: movie.title,
//     genres: movie.genres || [],
//     poster_path: movie.poster_path || 'assets/no-image.jpg',
//     avg_rating: movie.avg_rating || 0,
//     num_ratings: movie.num_ratings || 0
//   }));
// }


// }








// src/app/movie-details/movie-details.component.ts
import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { NavbarComponent } from '../navbar/navbar.component';
import { MovieService } from '../service/movie.service';
import { CommonModule } from '@angular/common';
import { AuthService } from '../service/auth.service';

import { Router } from '@angular/router';

@Component({
  standalone: true,
  imports: [CommonModule, NavbarComponent],
  templateUrl: './movie-details.component.html',
  styleUrls: ['./movie-details.component.css']
})
export class MovieDetailsComponent implements OnInit {
  movie: any;
  recommendations: any[] = [];
  loading = true;
  userRating: number | null = null;
  newRating = 0;
  hybridRecommendations: any[] = [];

  error = '';


  errors ={
    hybrid:''
  };

  loadingStates = {
    hybrid : true
  };



  

  constructor(public authService:AuthService ,  private route: ActivatedRoute, private movieService: MovieService , private router: Router) {}

  ngOnInit(): void {
    const movieId = this.route.snapshot.paramMap.get('id');
    if (movieId) {
      const id = +movieId;
      this.loadMovieDetails(id);
      this.loadHybridRecommendations(); // ✅ Add this
      if (this.authService.isAuthenticated()) {
        this.loadUserRating(id);
      }
    } else {
      this.handleError('Invalid movie ID');
    }
  }
  


  private loadHybridRecommendations(): void {
    this.movieService.getHybridRecommendations().subscribe({
      next: (movies) => {
        this.hybridRecommendations = this.transformMovieData(movies);
        this.loadingStates.hybrid = false;
      },
      error: () => {
        this.errors.hybrid = 'Failed to load hybrid recommendations';
        this.loadingStates.hybrid = false;
      }
    });
  }
  
  viewMovieDetails(movieId: number): void {
    this.router.navigate(['/movies', movieId]);
  }
  


  rateMovie(): void {
    this.movieService.rateMovie(this.movie.movieId, this.newRating).subscribe({
      next: () => {
        this.userRating = this.newRating;
        this.newRating = 0;
        this.loadMovieDetails(this.movie.movieId); // Refresh data
      },
      error: () => console.error('Failed to submit rating')
    });
  }

  

  private handleError(message: string): void {
    this.error = message;
    this.loading = false;
    console.error(message);
  }


  private loadMovieDetails(movieId: number): void {
    this.movieService.getMovieDetails(movieId).subscribe({
      next: (response) => {
        this.movie = response.movie;
        this.recommendations = response.recommendations || [];
        this.loading = false;
      },
      error: (err) => {
        if (err.status === 404) {
          this.handleError('Movie not found');
        } else {
          this.handleError('Failed to load details');
        }
      }
    });
  }


private loadUserRating(movieId: number): void {
  this.movieService.getUserRating(movieId).subscribe({
    next: (rating) => this.userRating = rating,
    error: (err) => {
      if (err.status === 404) {
        this.userRating = null; 
      } else {
        console.error('Rating load error:', err);
      }
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

markAsWatched(): void {
  const userId = this.authService.getUserId();
  if (!userId) return;
  this.movieService.markMovieAsWatched(this.movie.movieId, userId)
    .subscribe({
      next: res => console.log('Watched:', res),
      error: err => console.error(err)
    });
}

markAsToWatch(): void {
  const userId = this.authService.getUserId();
  if (!userId) return;
  this.movieService.markMovieAsToWatch(this.movie.movieId, userId)
    .subscribe({
      next: res => console.log('To‑Watch:', res),
      error: err => console.error(err)
    });
}

}







