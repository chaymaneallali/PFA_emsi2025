import { Routes } from '@angular/router';
import { LoginComponent } from './login/login.component';
import { RegisterComponent } from './register/register.component';
import { HomeComponent } from './home/home.component';
import { MovieDetailsComponent } from './movie-details/movie-details.component';
import { AuthGuard } from './service/auth.guard';

export const routes: Routes = [
  // Unauthenticated
  { path: 'login', component: LoginComponent },
  { path: 'register', component: RegisterComponent },

  // Protected
  { path: 'home', component: HomeComponent, canActivate: [AuthGuard] },
  { path: 'movies/:id', component: MovieDetailsComponent, canActivate: [AuthGuard] },

  // Default & fallback
  { path: '', redirectTo: '/home', pathMatch: 'full' },
  { path: '**', redirectTo: '/home' }
];
