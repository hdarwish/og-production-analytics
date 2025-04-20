/**
 * Shared interfaces for the application
 */

// Production data interface used in dashboard, charts, and tables
export interface ProductionData {
  well_name: string;
  date: string;
  oil_volume: number;
  region: string;
}

// Well data interface used in the map component
export interface WellData {
  id: number;
  name: string;
  latitude: number;
  longitude: number;
  region: string;
}

// Filter criteria for production data
export interface FilterCriteria {
  startDate: string;
  endDate: string;
  region: string;
  wellName: string;
} 