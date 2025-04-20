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
- PostgreSQL
- SQLAlchemy
- Alembic
- Docker

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
│   │   ├── api/         # API endpoints
│   │   ├── core/        # Core functionality
│   │   ├── db/          # Database models and migrations
│   │   ├── models/      # SQLAlchemy models
│   │   ├── schemas/     # Pydantic schemas
│   │   └── services/    # Business logic
│   ├── alembic/         # Database migrations
│   ├── Dockerfile       # Backend container definition
│   ├── docker-compose.yaml # Container orchestration
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

### Option 1: Docker Setup (Recommended)
```bash
# Start services
cd backend
docker-compose up --build

# Run migrations
docker-compose exec api alembic upgrade head
```

### Option 2: Manual Setup

#### Backend Setup
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

3. Set up environment variables:
   Create `.env` file in backend directory with:
   ```env
   POSTGRES_SERVER=localhost
   POSTGRES_USER=postgres
   POSTGRES_PASSWORD=postgres
   POSTGRES_DB=og_production
   POSTGRES_PORT=5432
   BACKEND_PORT=8000
   ```

4. Initialize database:
   ```bash
   # Make sure PostgreSQL is running
   alembic upgrade head
   ```

5. Run the server:
   ```bash
   uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
   ```

#### Database Setup (Manual)
```bash
# 1. Install PostgreSQL
# Follow your OS-specific installation instructions

# 2. Create database
createdb og_production

# 3. Create user (if needed)
createuser -P postgres  # Set password when prompted

# 4. Grant privileges
psql -d og_production -c "GRANT ALL PRIVILEGES ON DATABASE og_production TO postgres;"
```

#### Frontend Setup
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
- `POST /api/wells`
  - Create new well
- `PUT /api/wells/{id}`
  - Update well data
- `DELETE /api/wells/{id}`
  - Delete well

### Production Data
- `GET /api/production`
  - Returns filtered production data
  - Query Parameters:
    - start_date: Filter by start date
    - end_date: Filter by end date
    - well_name: Filter by well name
    - region: Filter by region
  - Response includes: well_name, date, production_volume, region
- `POST /api/production`
  - Create new production record
- `PUT /api/production/{id}`
  - Update production data
- `DELETE /api/production/{id}`
  - Delete production record

## Security Features
- Environment variable management
- Database credentials protection
- CORS configuration
- Input validation
- Error handling
- Secure API endpoints

## Performance Optimizations
- Database indexing
- Query optimization
- Lazy loading for map component
- Efficient data processing
- Cached preflight requests
- Optimized API responses
- Container resource management


### Chatbot
- `POST /api/chatbot`
  - Handles user queries
  - Request body: { message: string }
  - Returns predefined responses


## License

MIT 