// src/app/service/auth.service.ts
import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Router } from '@angular/router';
import { JwtHelperService } from '@auth0/angular-jwt';

@Injectable({ providedIn: 'root' })
export class AuthService {
  private apiUrl = 'http://localhost:8090/account';

  constructor(
    private http: HttpClient,
    private router: Router,
    public jwtHelper: JwtHelperService
  ) {}

  login(credentials: { username: string; password: string }) {
    return this.http.post(`${this.apiUrl}/login`, credentials);
  }

  register(userData: any) {
    return this.http.post(`${this.apiUrl}/register`, userData);
  }

  logout() {
    localStorage.removeItem('token');
    this.router.navigate(['/login']);
  }


  
  isAuthenticated(): boolean {
    const token = this.getToken();
    if (!token) {
      return false;
    }
    // If expired, clear and redirect
    if (this.jwtHelper.isTokenExpired(token)) {
      this.logout();
      return false;
    }
    return true;
  }
  // isAuthenticated(): boolean {
  //   const token = this.getToken();
  //   if (!token) return false;
  //   if (this.jwtHelper.isTokenExpired(token)) {
  //     this.logout();   // clears storage & navigates to login
  //     return false;
  //   }
  //   return true;
  // }
  

  getToken() {
    return localStorage.getItem('token');
  }

  getUserId(): number | null {
    const token = this.getToken();
    if (!token) return null;
    const decoded: any = this.jwtHelper.decodeToken(token);
    return decoded.userId || decoded.sub || null;
  }


  getUserName(): string {
    const token = this.getToken();
    if (token) {
      const decoded = this.jwtHelper.decodeToken(token);
      return decoded.userName || decoded.sub || 'Account';
    }
    return 'Account';
  }


  
}
