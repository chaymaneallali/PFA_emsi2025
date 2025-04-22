// // src/app/service/jwt.interceptor.ts
// import { Injectable } from '@angular/core';
// import {
//   HttpRequest,
//   HttpHandler,
//   HttpEvent,
//   HttpInterceptor
// } from '@angular/common/http';
// import { AuthService } from './auth.service';
// import { Observable } from 'rxjs';

// @Injectable()
// export class JwtInterceptor implements HttpInterceptor {
//   constructor(private authService: AuthService) {}

//   intercept(request: HttpRequest<unknown>, next: HttpHandler): Observable<HttpEvent<unknown>> {
//     // Don't add token on login or register endpoints
//     if (
//       request.url.endsWith('/account/login') ||
//       request.url.endsWith('/account/register')
//     ) {
//       return next.handle(request);
//     }

//     // Otherwise, attach the token (if present)
//     const token = this.authService.getToken();
//     if (token) {
//       request = request.clone({
//         setHeaders: {
//           Authorization: `Bearer ${token}`
//         }
//       });
//     }

//     return next.handle(request);
//   }
// }


// src/app/service/jwt.interceptor.ts
import { Injectable } from '@angular/core';
import {
  HttpRequest,
  HttpHandler,
  HttpEvent,
  HttpInterceptor
} from '@angular/common/http';
import { AuthService } from './auth.service';
import { Observable, throwError } from 'rxjs';
import { catchError } from 'rxjs/operators';

@Injectable()
export class JwtInterceptor implements HttpInterceptor {
  constructor(private authService: AuthService) {}

  intercept(request: HttpRequest<unknown>, next: HttpHandler): Observable<HttpEvent<unknown>> {
    // Skip adding auth header on login/register
    if (
      request.url.endsWith('/account/login') ||
      request.url.endsWith('/account/register')
    ) {
      return next.handle(request);
    }

    // Attach token if present
    const token = this.authService.getToken();
    if (token) {
      request = request.clone({
        setHeaders: { Authorization: `Bearer ${token}` }
      });
    }

    // Catch 401 responses
    return next.handle(request).pipe(
      catchError(err => {
        if (err.status === 401) {
          // Token expired or unauthorized—force logout
          this.authService.logout();
        }
        return throwError(() => err);
      })
    );
  }
}
