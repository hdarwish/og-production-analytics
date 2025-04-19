import { Component } from '@angular/core';
import { RouterModule } from '@angular/router';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [CommonModule, RouterModule],
  template: `
    <nav class="navbar">
      <div class="nav-container">
        <div class="nav-brand">
          <span class="brand-text">Oil & Gas Production System</span>
        </div>
        <div class="nav-links">
          <a routerLink="/" routerLinkActive="active" [routerLinkActiveOptions]="{exact: true}">Dashboard</a>
          <a routerLink="/map" routerLinkActive="active">Map</a>
        </div>
      </div>
    </nav>
    <div class="content-container">
      <router-outlet></router-outlet>
    </div>
  `,
  styles: [`
    :host {
      display: flex;
      flex-direction: column;
      min-height: 100vh;
    }

    .navbar {
      border-radius: 4px;
      background-color: #0014dc;
      padding: 1rem 0;
      box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }

    .nav-container {
      margin: 0 auto;
      padding: 0 1rem;
      display: flex;
      justify-content: space-between;
      align-items: center;
      font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }

    .nav-brand {
      .brand-text {
        color: white;
        font-size: 1.25rem;
        font-weight: 500;
        text-decoration: none;
      }
    }

    .nav-links {
      display: flex;
      gap: 2rem;

      a {
        color: rgba(255, 255, 255, 0.8);
        text-decoration: none;
        font-size: 1rem;
        transition: color 0.2s ease;
        position: relative;

        &:hover {
          color: white;
        }

        &.active {
          color: white;
          
          &::after {
            content: '';
            position: absolute;
            bottom: -4px;
            left: 0;
            width: 100%;
            height: 2px;
            background-color: white;
          }
        }
      }
    }

    .content-container {
      flex: 1;
      width: 100%;
    }
  `]
})

export class AppComponent {
  title = 'frontend';
}
