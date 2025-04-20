import { Component, Input, OnChanges } from '@angular/core';
import { NgxChartsModule, LegendPosition } from '@swimlane/ngx-charts';
import { ProductionData } from '../shared/models';

@Component({
  selector: 'app-regional-chart',
  standalone: true,
  imports: [NgxChartsModule],
  template: `
    <div class="card">
      <div class="card-body">
        <h5 class="card-title">Production by Region</h5>
        <div class="chart-wrapper">
          <ngx-charts-pie-chart
            [results]="chartData"
            [legend]="true"
            [labels]="true"
            [doughnut]="true"
            [view]="[1000, 400]"
            [gradient]="true"
            [legendTitle]="'Regions'"
            [legendPosition]="LegendPosition.Below">
          </ngx-charts-pie-chart>
        </div>
      </div>
    </div>
  `,
  styles: [`
    :host {
      display: block;
      height: 100%;
    }

    .card {
      height: 100%;
    }

    .card-body {
      height: 100%;
      display: flex;
      flex-direction: column;
    }

    .chart-wrapper {
      flex: 1;
      display: flex;
      justify-content: center;
      align-items: center;
    }

    ngx-charts-pie-chart {
      width: 100%;
      height: 100%;
    }
  `]
})
export class RegionalChartComponent implements OnChanges {
  @Input() data: ProductionData[] = [];
  chartData: { name: string; value: number; }[] = [];
  LegendPosition = LegendPosition;

  ngOnChanges() {
    this.processData();
  }

  private processData() {
    const regionMap = new Map<string, number>();

    // Sum production by region
    this.data.forEach(item => {
      const currentValue = regionMap.get(item.region) || 0;
      regionMap.set(item.region, currentValue + item.oil_volume);
    });


    // Convert to chart format
    this.chartData = Array.from(regionMap.entries()).map(([region, volume]) => ({
      name: region,
      value: volume
    }));
  }
} 