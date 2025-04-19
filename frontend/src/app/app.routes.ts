import { Routes } from '@angular/router';
import { DashboardComponent } from './dashboard/dashboard.component';

export const routes: Routes = [
  { path: '', component: DashboardComponent },
  { 
    path: 'map', 
    loadComponent: () => import('./map/map.component').then(m => m.MapComponent)
  }
]; 