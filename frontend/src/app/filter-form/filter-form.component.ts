import { Component, Output, EventEmitter } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';

interface FilterCriteria {
  startDate: string;
  endDate: string;
  region: string;
  wellName: string;
}

@Component({
  selector: 'app-filter-form',
  standalone: true,
  imports: [CommonModule, FormsModule],
  template: `
    <div class="filter-container">
      <form (ngSubmit)="onSubmit()" #filterForm="ngForm">
        <div class="filter-row">
          <div class="filter-group">
            <label for="startDate">Start Date</label>
            <input
              type="date"
              id="startDate"
              name="startDate"
              [(ngModel)]="filters.startDate"
              class="filter-input">
          </div>
          <div class="filter-group">
            <label for="endDate">End Date</label>
            <input
              type="date"
              id="endDate"
              name="endDate"
              [(ngModel)]="filters.endDate"
              class="filter-input">
          </div>
          <div class="filter-group">
            <label for="region">Region</label>
            <select
              id="region"
              name="region"
              [(ngModel)]="filters.region"
              class="filter-input">
              <option value="">All Regions</option>
              <option value="North">North</option>
              <option value="South">South</option>
              <option value="East">East</option>
              <option value="West">West</option>
            </select>
          </div>
          <div class="filter-group">
            <label for="wellName">Well Name</label>
            <input
              type="text"
              id="wellName"
              name="wellName"
              [(ngModel)]="filters.wellName"
              placeholder="Enter well name"
              class="filter-input">
          </div>
          <div class="filter-group">
            <button type="submit" class="filter-button">Apply Filters</button>
          </div>
        </div>
      </form>
    </div>
  `,
  styles: [`
    .filter-container {
      background: white;
      padding: 1.5rem;
      border-radius: 8px;
      box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
      margin-bottom: 1.5rem;
    }

    .filter-row {
      display: flex;
      flex-wrap: wrap;
      gap: 0.5rem;
      align-items: flex-end;
    }

    .filter-group {
      flex: 1;
      min-width: 150px;
      margin-bottom: 0.5rem;
    }

    label {
      display: block;
      margin-bottom: 0.5rem;
      color: #333;
      font-weight: 500;
      font-size: 0.9rem;
    }

    .filter-input {
      width: 100%;
      padding: 0.5rem;
      border: 1px solid #ddd;
      border-radius: 4px;
      font-size: 0.9rem;
      transition: all 0.3s ease;
      box-sizing: border-box;
    }

    select.filter-input {
      appearance: none;
      background-image: url("data:image/svg+xml;charset=UTF-8,%3csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='currentColor' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3e%3cpolyline points='6 9 12 15 18 9'%3e%3c/polyline%3e%3c/svg%3e");
      background-repeat: no-repeat;
      background-position: right 0.5rem center;
      background-size: 1em;
      padding-right: 2rem;
    }

    .filter-input:focus {
      outline: none;
      border-color: #6e8cc8;
      box-shadow: 0 0 0 2px rgba(26, 82, 118, 0.2);
    }

    .filter-input:hover {
      border-color: #6e8cc8;
    }

    .filter-button {
      background-color: #afbee1;
      color: white;
      border: none;
      padding: 0.5rem 1.5rem;
      border-radius: 4px;
      cursor: pointer;
      font-weight: 500;
      transition: all 0.3s ease;
      box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }

    .filter-button:hover {
      background-color: #6e8cc8;
      transform: translateY(-1px);
      box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }

    .filter-button:active {
      transform: translateY(0);
      box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }

    @media (max-width: 768px) {
      .filter-row {
        flex-direction: column;
      }
      
      .filter-group {
        width: 100%;
        margin-bottom: 0.5rem;
      }
    }
  `]
})
export class FilterFormComponent {
  @Output() filtersChanged = new EventEmitter<FilterCriteria>();

  filters: FilterCriteria = {
    startDate: '',
    endDate: '',
    region: '',
    wellName: ''
  };

  onSubmit() {
    this.filtersChanged.emit(this.filters);
  }
}