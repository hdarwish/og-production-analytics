import { Component, OnInit, PLATFORM_ID, Inject, NgZone } from '@angular/core';
import { CommonModule, isPlatformBrowser } from '@angular/common';
import { HttpClient } from '@angular/common/http';
import { LeafletModule } from '@bluehalo/ngx-leaflet';
import * as L from 'leaflet';
import { environment } from '../../environments/environment';
import { WellData } from '../shared/models';

@Component({
  selector: 'app-map',
  standalone: true,
  imports: [CommonModule, LeafletModule],
  template: `
    <div class="map-page">
      <div class="map-header">
        <h1>Oil & Gas Production Map</h1>
        <p class="subtitle">Interactive map showing well locations</p>
      </div>
      <div class="map-wrapper" *ngIf="isBrowser">
        <div leaflet
             [leafletOptions]="options"
             [leafletLayers]="layers"
             (leafletMapReady)="onMapReady($event)">
        </div>
      </div>
      <div *ngIf="!isBrowser" class="map-placeholder">
        Loading map...
      </div>
    </div>
  `,
  styles: [`
    .map-page {
      height: calc(100vh - 200px);
      display: flex;
      flex-direction: column;
      background: white;
      border-radius: 8px;
      box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }

    .map-header {
      padding: 1.5rem;
      border-bottom: 1px solid #e5e5e5;
      background-color: #f8f9fa;
      text-align: center;
      font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }

    .map-header h1 {
      margin: 0;
      font-size: 1.75rem;
      color: #0014dc;
      font-weight: 500;
    }

    .map-header .subtitle {
      margin: 0.5rem 0 0;
      color: #666;
      font-size: 1rem;
    }

    .map-wrapper {
      flex: 1;
      position: relative;
      background-color: #f8f9fa;
    }

    .map-wrapper > div {
      position: absolute;
      top: 0;
      left: 0;
      right: 0;
      bottom: 0;
    }

    .map-placeholder {
      flex: 1;
      display: flex;
      align-items: center;
      justify-content: center;
      color: #666;
      font-size: 1.1rem;
      background-color: #f8f9fa;
    }

    :host ::ng-deep .popup-content {
      padding: 0.5rem;
      
      h4 {
        margin: 0 0 0.5rem 0;
        color: #0014dc;
        font-size: 1rem;
        font-weight: 500;
      }
      
      p {
        margin: 0;
        color: #666;
        font-size: 0.9rem;
        
        strong {
          color: #0014dc;
        }
      }
    }
  `]
})
export class MapComponent implements OnInit {
  isBrowser: boolean;
  options = {
    layers: [
      L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        maxZoom: 18,
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
      })
    ],
    zoom: 8,
    center: L.latLng(24.4782545, 54.379262), // Abu Dhabi center
    zoomControl: true,
    attributionControl: true
  };

  layers: L.Layer[] = [];
  private map!: L.Map;

  constructor(
    private http: HttpClient,
    @Inject(PLATFORM_ID) platformId: Object,
    private zone: NgZone
  ) {
    this.isBrowser = isPlatformBrowser(platformId);
  }

  ngOnInit() {
    if (this.isBrowser) {
      this.loadWellData();
    }
  }

  onMapReady(map: L.Map) {
    console.log('Map ready');
    this.map = map;
    // Ensure map is properly initialized
    this.zone.run(() => {
      this.map.invalidateSize();
    });
  }

  private loadWellData() {
    console.log('Loading well data...');
    this.http.get<WellData[]>(`${environment.apiUrl}/wells`)
      .subscribe({
        next: (data) => {
          console.log('Raw data received:', JSON.stringify(data, null, 2));
          
          // Validate and clean the data
          const validData = data.filter(item => {
            const isValid = item && 
              typeof item.name === 'string' &&
              typeof item.latitude === 'number' && 
              typeof item.longitude === 'number' &&
              typeof item.region === 'string';
            
            if (!isValid) {
              console.warn('Invalid data item:', item);
            }
            return isValid;
          });
          
          console.log('Validated data:', JSON.stringify(validData, null, 2));
          
          if (validData.length === 0) {
            console.error('No valid data found');
            return;
          }
          
          this.zone.run(() => {
            this.addMarkers(validData);
            this.fitBounds(validData);
          });
        },
        error: (error) => {
          console.error('Error loading well data:', error);
        }
      });
  }

  private addMarkers(data: WellData[]) {
    console.log('Adding markers...');
    console.log('Input data:', JSON.stringify(data, null, 2));
    
    // Clear existing layers
    this.layers = [];
    
    // Add base layer
    const baseLayer = L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      maxZoom: 18,
      attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
    });
    this.layers.push(baseLayer);
    console.log('Base layer added');
    
    // Add markers
    data.forEach(item => {
      try {
        if (item.latitude && item.longitude) {
          console.log('Creating marker for:', item.name, 'at', item.latitude, item.longitude);
          const latLng = L.latLng(item.latitude, item.longitude);
          
          const marker = L.marker(latLng, {
            icon: L.icon({
              iconUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon.png',
              iconRetinaUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon-2x.png',
              shadowUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-shadow.png',
              iconSize: [25, 41],
              iconAnchor: [12, 41],
              popupAnchor: [1, -34],
              shadowSize: [41, 41]
            })
          }).bindPopup(`
            <div class="popup-content">
              <h4>${item.name}</h4>
              <p><strong>Region:</strong> ${item.region}</p>
            </div>
          `);
          
          this.layers.push(marker);
          console.log('Marker added to layers:', marker.getLatLng());
        } else {
          console.warn('Invalid coordinates for well:', item.name, 'lat:', item.latitude, 'lng:', item.longitude);
        }
      } catch (error) {
        console.error('Error creating marker for well:', item.name, error);
      }
    });

    console.log('Final layers array length:', this.layers.length);
    console.log('Map bounds:', this.map.getBounds());
  }

  private fitBounds(data: WellData[]) {
    console.log('Fitting bounds...');
    const validPoints = data.filter(item => item.latitude && item.longitude);
    console.log('Valid points count:', validPoints.length);
    
    if (validPoints.length === 0) {
      console.error('No valid points to fit bounds');
      return;
    }
    
    const bounds = L.latLngBounds(
      validPoints.map(item => L.latLng(item.latitude, item.longitude))
    );
    
    if (!bounds.isValid()) {
      console.error('Invalid bounds:', bounds);
      return;
    }

    console.log('Fitting bounds to:', bounds);
    this.zone.run(() => {
      this.map.fitBounds(bounds, {
        padding: [50, 50],
        maxZoom: 12
      });
    });
  }
} 