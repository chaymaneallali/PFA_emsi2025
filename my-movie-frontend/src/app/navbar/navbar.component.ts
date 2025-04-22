// // src/app/navbar/navbar.component.ts
// import { Component } from '@angular/core';
// import { AuthService } from '../service/auth.service';
// import { Router } from '@angular/router';
// import { CommonModule } from '@angular/common';

// @Component({
//   selector: 'app-navbar',
//   standalone: true,
//   imports: [CommonModule],
//   template: `
//     <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
//       <div class="container">
//         <a class="navbar-brand" routerLink="/home">MyMovie</a>
//         <div *ngIf="authService.isAuthenticated()" class="ms-auto">
//           <button class="btn btn-danger" (click)="logout()">Logout</button>
//         </div>
//       </div>
//     </nav>
//   `,
// })
// export class NavbarComponent {
//   constructor(
//     public authService: AuthService,
//     private router: Router
//   ) {}

//   logout() {
//     this.authService.logout();
//     this.router.navigate(['/login']);
//   }
// }


// src/app/navbar/navbar.component.ts
import { Component } from '@angular/core';
import { AuthService } from '../service/auth.service';
import { Router } from '@angular/router';
import { CommonModule } from '@angular/common';
import { NgbDropdownModule } from '@ng-bootstrap/ng-bootstrap';

@Component({
  selector: 'app-navbar',
  standalone: true,
  imports: [CommonModule, NgbDropdownModule],
  template: `
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
      <div class="container">
        <a class="navbar-brand" routerLink="/home">MyMovie</a>
        
        <!-- Display the account dropdown if the user is authenticated -->
        <div *ngIf="authService.isAuthenticated()" class="ms-auto" ngbDropdown>
          <button class="btn btn-secondary" id="accountDropdown" ngbDropdownToggle>
            <i class="bi bi-person"></i>
            {{ authService.getUserName() }}
          </button>
          <div ngbDropdownMenu aria-labelledby="accountDropdown" class="dropdown-menu-end">
            <button ngbDropdownItem routerLink="/settings">Settings</button>
            <button ngbDropdownItem (click)="logout()">Logout</button>
          </div>
        </div>
      </div>
    </nav>
  `,
})
export class NavbarComponent {
  constructor(
    public authService: AuthService,
    private router: Router
  ) {}

  logout() {
    this.authService.logout();
    this.router.navigate(['/login']);
  }
}
