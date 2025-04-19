# Oil & Gas Production Analytics Dashboard

A full-stack web application for visualizing oil and gas production data with interactive filters, charts, and maps.

## Features

- Interactive data visualization
  - Production trends over time
  - Regional production distribution
  - Well location mapping
- Real-time filtering of production data
  - Date range selection
  - Well name filtering
  - Region-based filtering
- Geographic mapping of well locations
  - Interactive markers
  - Well information popups
  - Automatic bounds fitting
- Production trend analysis
  - Daily production volume
  - Regional distribution
  - Tabular data view
- Chatbot assistance
  - Quick help
  - Data filtering guidance
  - Feature explanations

## Tech Stack

### Backend
- Python 3.8+
- FastAPI
- Pandas
- CSV data storage

### Frontend
- Angular 17
- ngx-charts
- @bluehalo/ngx-leaflet
- Standalone Components
- CSS

## Project Structure

```
oil-production-analytics/
├── backend/              # FastAPI backend
│   ├── app/             # Application code
│   │   ├── main.py      # FastAPI application
│   │   └── data/        # Data processing
│   ├── data/            # Sample data files
│   └── requirements.txt # Python dependencies
├── frontend/            # Angular frontend
│   ├── src/            # Source code
│   │   ├── app/        # Application components
│   │   │   ├── dashboard/
│   │   │   ├── map/
│   │   │   ├── production-chart/
│   │   │   ├── regional-chart/
│   │   │   └── production-table/
│   │   └── styles/     # Global styles
│   └── package.json    # Node dependencies
├── docs/               # Documentation
│   └── application_workflow.md
└── README.md          # Project documentation
```

## Setup Instructions

### Backend Setup
1. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

3. Run the server:
   ```bash
   uvicorn app.main:app --reload
   ```

### Frontend Setup
1. Install dependencies:
   ```bash
   cd frontend
   pnpm install
   ```

2. Run the development server:
   ```bash
   pnpm start
   ```

## API Endpoints

### Well Data
- `GET /api/wells`
  - Returns well location data
  - Used for map visualization
  - Response includes: well_name, latitude, longitude, region

### Production Data
- `GET /api/production`
  - Returns filtered production data
  - Query Parameters:
    - start_date: Filter by start date
    - end_date: Filter by end date
    - well_name: Filter by well name
    - region: Filter by region
  - Response includes: well_name, date, production_volume, region

### Chatbot
- `POST /api/chatbot`
  - Handles user queries
  - Request body: { message: string }
  - Returns predefined responses

## Security Features
- CORS configuration with specific origins
- Input validation
- Error handling
- Secure API endpoints

## Performance Optimizations
- Lazy loading for map component
- Efficient data processing
- Cached preflight requests
- Optimized API responses

## License

MIT 