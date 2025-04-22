// src/app/login/login.component.ts
import { Component } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { Router, RouterLink } from '@angular/router';
import { AuthService } from '../service/auth.service';
import { CommonModule } from '@angular/common';

@Component({
  standalone: true,
  imports: [FormsModule, RouterLink, CommonModule],
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css']
})
export class LoginComponent {
  credentials = { username: '', password: '' };
  errorMessage = '';

  constructor(private authService: AuthService, private router: Router) {}

  onSubmit() {
    console.log('Sending credentials:', this.credentials);
    this.authService.login(this.credentials)
      .subscribe({
        next: (response: any) => {
          console.log('Login response:', response);
          localStorage.setItem('token', response.token);
          this.router.navigate(['/home']);
        },
        error: err => {
          console.error('Login error', err);
          this.errorMessage = `Login failed (${err.status}): ${err.error?.message || 'Invalid credentials'}`;
        }
      });
  }
}
