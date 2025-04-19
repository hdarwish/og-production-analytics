import { Component, Input, OnChanges } from '@angular/core';
import { NgxChartsModule } from '@swimlane/ngx-charts';
import { CommonModule } from '@angular/common';

interface ProductionData {
  well_name: string;
  date: string;
  production_volume: number;
  region: string;
}

interface ChartData {
  name: string;
  value: number;
}

@Component({
  selector: 'app-production-chart',
  standalone: true,
  imports: [CommonModule, NgxChartsModule],
  template: `
    <div class="card">
      <div class="card-body">
        <h5 class="card-title">Daily Production Volume</h5>
        <ngx-charts-bar-vertical
          [results]="chartData"
          [xAxis]="true"
          [yAxis]="true"
          [legend]="true"
          [showXAxisLabel]="true"
          [showYAxisLabel]="true"
          xAxisLabel="Date"
          yAxisLabel="Total Production Volume (bbl)"
          [showDataLabel]="true"
          [roundDomains]="true"
          [showGridLines]="true"
          [tooltipDisabled]="false"
          [yScaleMax]="yScaleMax"
          [yScaleMin]="0"
          [trimYAxisTicks]="false"
          [yAxisTicks]="yAxisTicks"
          [yAxisTickFormatting]="formatYAxis">
        </ngx-charts-bar-vertical>
      </div>
    </div>
  `,
  styles: [`
    :host {
      display: block;
      height: 400px;
    }
    .card {
      height: 100%;
    }
    .card-body {
      height: 100%;
      display: flex;
      flex-direction: column;
    }
    ngx-charts-bar-vertical {
      flex: 1;
    }
  `]
})
export class ProductionChartComponent implements OnChanges {
  @Input() data: ProductionData[] = [];
  chartData: ChartData[] = [];
  yScaleMax: number = 0;
  yAxisTicks: number[] = [];

  ngOnChanges() {
    this.processData();
  }

  private processData() {
    // Group and sum production volumes by date
    const dateMap = new Map<string, number>();
    
    this.data.forEach(item => {
      const currentTotal = dateMap.get(item.date) || 0;
      dateMap.set(item.date, currentTotal + item.production_volume);
    });

    // Convert to bar chart format and sort by date
    this.chartData = Array.from(dateMap.entries())
      .map(([date, totalVolume]) => ({
        name: date,
        value: totalVolume
      }))
      .sort((a, b) => a.name.localeCompare(b.name));

    // Calculate y-axis scale
    const maxValue = Math.max(...this.chartData.map(d => d.value));
    this.yScaleMax = Math.ceil(maxValue * 1.1); // Add 10% padding
    this.yAxisTicks = this.calculateYTicks(this.yScaleMax);
  }

  private calculateYTicks(max: number): number[] {
    const step = Math.ceil(max / 5);
    const ticks: number[] = [];
    for (let i = 0; i <= max; i += step) {
      ticks.push(i);
    }
    return ticks;
  }

  formatYAxis(value: number): string {
    return value.toLocaleString();
  }
}