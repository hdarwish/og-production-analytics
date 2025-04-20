import { Component, Inject, PLATFORM_ID, ViewChild } from '@angular/core';
import { CommonModule, isPlatformBrowser } from '@angular/common';
import { HttpClient } from '@angular/common/http';
import { FormsModule } from '@angular/forms';
import { ProductionTableComponent } from '../production-table/production-table.component';
import { ProductionChartComponent } from '../production-chart/production-chart.component';
import { RegionalChartComponent } from '../regional-chart/regional-chart.component';
import { FilterFormComponent } from '../filter-form/filter-form.component';
import { ChatbotComponent } from '../chatbot/chatbot.component';
import { environment } from '../../environments/environment';
import { ProductionData, FilterCriteria } from '../shared/models';

@Component({
  selector: 'app-dashboard',
  standalone: true,
  imports: [
    CommonModule,
    FormsModule,
    ProductionTableComponent,
    ProductionChartComponent,
    RegionalChartComponent,
    FilterFormComponent,
    ChatbotComponent
  ],
  template: `
    <div class="dashboard-container">
      <header class="dashboard-header">
        <h1>Oil & Gas Production Dashboard</h1>
        <p class="subtitle">production monitoring and analysis</p>
      </header>

      <section class="filter-section">
        <app-filter-form 
          (filtersChanged)="onFiltersChanged($event)"
        ></app-filter-form>
      </section>

      <section class="data-section">
        <div class="chart-container">
          <app-production-chart [data]="productionData"></app-production-chart>
        </div>
        <div class="table-container">
          <app-production-table [data]="productionData"></app-production-table>
        </div>
        <div class="regional-chart-container">
          <app-regional-chart [data]="productionData"></app-regional-chart>
        </div>
      </section>

      <app-chatbot></app-chatbot>
    </div>
  `,
  styles: [`
    .dashboard-container {
      display: flex;
      flex-direction: column;
      min-height: 100vh;
      background-color: #f5f7fa;
      font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
      padding: 20px;
      position: relative;
    }

    .dashboard-header {
      text-align: center;
      margin-bottom: 2rem;
      padding: 1.5rem;
      background-color: #f8f9fa;
      border-bottom: 1px solid #e5e5e5;
    }

    .dashboard-header h1 {
      margin: 0;
      font-size: 1.75rem;
      color: #0014dc;
      font-weight: 500;
    }

    .subtitle {
      margin: 0.5rem 0 0;
      color: #666;
      font-size: 1rem;
    }

    .filter-section {
      margin-bottom: 2rem;
      width: 100%;
    }

    .data-section {
      display: grid;
      grid-template-columns: 1fr;
      gap: 2rem;
      flex: 1;
    }

    @media (min-width: 992px) {
      .data-section {
        grid-template-columns: 2fr 1fr;
        grid-template-areas: 
          "chart table"
          "regional regional";
      }

      .chart-container {
        grid-area: chart;
      }

      .table-container {
        grid-area: table;
      }

      .regional-chart-container {
        grid-area: regional;
      }
    }

    .chart-container, .table-container {
      background: white;
      border-radius: 8px;
      padding: 1.5rem;
      box-shadow: 0 2px 15px rgba(0, 0, 0, 0.05);
    }

    .chart-container {
      min-height: 400px;
    }

    .regional-chart-container {
      background: white;
      border-radius: 8px;
      padding: 1.5rem;
      box-shadow: 0 2px 15px rgba(0, 0, 0, 0.05);
      min-height: 500px;
    }

    .dashboard-footer {
      text-align: center;
      margin-top: 2rem;
      padding: 1rem;
      color: #666;
      font-size: 0.9rem;
    }

    /* Chatbot Styles */
    .chatbot-container {
      position: fixed;
      bottom: 0px;
      right: 20px;
      width: 300px;
      background: white;
      border-radius: 8px;
      box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
      z-index: 1000;
      transition: all 0.3s ease;
    }

    .chatbot-header {
      padding: 10px 15px;
      background: #6e8cc8;
      color: white;
      border-radius: 8px 8px 0 0;
      cursor: pointer;
      display: flex;
      justify-content: space-between;
      align-items: center;
    }

    .chatbot-content {
      height: 0;
      overflow: hidden;
      transition: height 0.3s ease;
    }

    .chatbot-container.active .chatbot-content {
      height: 400px;
      display: flex;
      flex-direction: column;
    }

    .chat-messages {
      flex: 1;
      padding: 15px;
      overflow-y: auto;
    }

    .message {
      margin-bottom: 10px;
      padding: 8px 12px;
      border-radius: 4px;
      background: #f0f0f0;
      max-width: 80%;
    }

    .message.user {
      background: #6e8cc8;
      color: white;
      margin-left: auto;
    }

    .chat-input {
      padding: 10px;
      border-top: 1px solid #eee;
      display: flex;
      gap: 10px;
    }

    .chat-input input {
      flex: 1;
      padding: 8px;
      border: 1px solid #ddd;
      border-radius: 4px;
    }

    .chat-input button {
      padding: 8px 15px;
      background: #6e8cc8;
      color: white;
      border: none;
      border-radius: 4px;
      cursor: pointer;
    }

    .chat-input button:hover {
      background: #6e8cc8;
    }
  `]
})
export class DashboardComponent {
  productionData: ProductionData[] = [];
  lastUpdated: Date = new Date();
  isLoading = false;
  isChatbotOpen = false;
  userMessage = '';
  chatMessages: { text: string; isUser: boolean }[] = [];

  @ViewChild('chatInput') chatInput: any;

  constructor(
    private http: HttpClient,
    @Inject(PLATFORM_ID) private platformId: Object
  ) {
    if (isPlatformBrowser(this.platformId)) {
      this.fetchProductionData();
    }
  }

  onFiltersChanged(filters: FilterCriteria) {
    if (isPlatformBrowser(this.platformId)) {
      this.fetchProductionData(filters);
    }
  }

  refreshData() {
    if (isPlatformBrowser(this.platformId)) {
      this.fetchProductionData();
    }
  }

  toggleChatbot() {
    this.isChatbotOpen = !this.isChatbotOpen;
    if (this.isChatbotOpen) {
      setTimeout(() => {
        this.chatInput.nativeElement.focus();
      }, 0);
    }
  }

  sendMessage() {
    if (this.userMessage.trim() && isPlatformBrowser(this.platformId)) {
      this.chatMessages.push({ text: this.userMessage, isUser: true });
      this.getChatbotResponse(this.userMessage);
      this.userMessage = '';
    }
  }

  private getChatbotResponse(message: string) {
    if (!isPlatformBrowser(this.platformId)) return;
    
    this.http.post<{ response: string }>(`${environment.apiUrl}/chatbot`, { message })
      .subscribe({
        next: (data) => {
          this.chatMessages.push({ text: data.response, isUser: false });
        },
        error: (error) => {
          console.error('Error getting chatbot response:', error);
          this.chatMessages.push({ 
            text: "Sorry, I'm having trouble connecting to the server. Please try again later.", 
            isUser: false 
          });
        }
      });
  }

  private fetchProductionData(filters?: FilterCriteria) {
    if (!isPlatformBrowser(this.platformId)) return;

    this.isLoading = true;
    let url = `${environment.apiUrl}/production`;
    if (filters) {
      const params = new URLSearchParams();
      if (filters.startDate) params.append('start_date', filters.startDate);
      if (filters.endDate) params.append('end_date', filters.endDate);
      if (filters.region) params.append('region', filters.region);
      if (filters.wellName) params.append('well_name', filters.wellName);
      url += `?${params.toString()}`;
    }
    
    console.log('Fetching production data from:', url);
    
    this.http.get<ProductionData[]>(url).subscribe({
      next: (data) => {
        console.log('Received filtered production data:', data);
        console.log('Data length:', data.length);
        this.productionData = data;
        this.lastUpdated = new Date();
      },
      error: (error) => {
        console.error('Error fetching production data:', error);
      },
      complete: () => {
        this.isLoading = false;
      }
    });
  }
}