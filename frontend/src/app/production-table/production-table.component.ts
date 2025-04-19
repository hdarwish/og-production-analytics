import { Component, Input } from '@angular/core';
import { CommonModule } from '@angular/common';

interface ProductionData {
  well_name: string;
  date: string;
  production_volume: number;
  region: string;
}

@Component({
  selector: 'app-production-table',
  standalone: true,
  imports: [CommonModule],
  template: `
    <div class="card">
      <div class="card-body">
        <h5 class="card-title">Production Data</h5>
        <div class="table-responsive">
          <table class="table">
            <thead>
              <tr>
                <th class="text-left">Name</th>
                <th class="text-left">Volume</th>
                <th class="text-left">Region</th>
                <th class="text-left">Date</th>
              </tr>
            </thead>
            <tbody>
              <tr *ngFor="let item of data">
                <td>{{ item.well_name }}</td>
                <td>{{ item.production_volume | number:'1.0-2' }}</td>
                <td>{{ item.region }}</td>
                <td>{{ item.date | date }}</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  `,
  styles: [`
    .table {
      width: 100%;
      margin-bottom: 0;
      background-color: white;
    }
    .card {
      margin-bottom: 20px;
    }
    .table-responsive {
      max-height: 400px;
      overflow-y: auto;
    }
    .text-left {
      text-align: left !important;
    }
  `]
})
export class ProductionTableComponent {
  @Input() data: ProductionData[] = [];
} 