# Oil & Gas Production Analytics Backend

This is the backend service for the Oil & Gas Production Analytics application. It provides REST APIs for managing well and production data.

## Features

- Well management (CRUD operations)
- Production data tracking
- Production analytics and summaries
- Field-level analytics
- RESTful API with FastAPI
- PostgreSQL database with SQLAlchemy ORM
- Alembic database migrations

## Tech Stack

- Python 3.12+
- FastAPI
- SQLAlchemy
- PostgreSQL
- Alembic
- Pydantic
- Docker

## Setup

### Using Docker (Recommended)

The simplest way to set up the entire backend is using Docker Compose:

1. Make sure Docker and Docker Compose are installed on your system

2. Build and start the services:
   ```bash
   # From the backend directory
   docker-compose up -d
   ```

3. The API will be available at http://localhost:8000
   - The database migrations will run automatically on startup
   - The API server has hot-reload enabled for development

4. To stop the services:
   ```bash
   docker-compose down
   ```

5. To view logs:
   ```bash
   # View logs of all services
   docker-compose logs -f
   
   # View logs of specific service
   docker-compose logs -f api
   ```

### Manual Setup

If you prefer to set up without Docker:

1. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up the database:
   ```bash
   # Create PostgreSQL database
   createdb og_production

   # Run migrations
   alembic upgrade head
   ```

4. Create `.env` file:
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

5. Run the development server:
   ```bash
   uvicorn app.main:app --reload
   ```

## API Documentation

Once the server is running, you can access:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Project Structure

```
backend/
├── app/
│   ├── api/
│   │   ├── v1/
│   │   │   ├── endpoints/
│   │   │   │   ├── wells.py
│   │   │   │   ├── production.py
│   │   │   │   └── chatbot.py
│   │   │   └── router.py
│   │   └── deps.py
│   ├── core/
│   │   ├── config.py
│   │   ├── security.py
│   │   └── logging.py
│   ├── models/
│   │   ├── well.py
│   │   └── production.py
│   ├── schemas/
│   │   ├── well.py
│   │   └── production.py
│   ├── services/
│   │   └── production_service.py
│   └── db/
│       ├── base.py
│       ├── deps.py
│       ├── init_db.py
│       └── session.py
├── alembic/
│   └── versions/
├── tests/
│   └── api/
│       └── test_wells.py
├── Dockerfile
└── docker-compose.yaml
```

## Development

- Use `alembic revision --autogenerate -m "message"` to create new migrations
- Run tests with `pytest`
- Format code with `black .`
- Check types with `mypy .`

## Working with Docker

### Rebuilding the API Image

If you've made changes to the requirements or Dockerfile:

```bash
docker-compose build api
docker-compose up -d
```

### Accessing the PostgreSQL Database

```bash
# Connect to the database using psql in the container
docker-compose exec postgres psql -U postgres -d og_production

# Or if you have psql installed locally
psql -h localhost -U postgres -d og_production
```

### Running Migrations Manually

```bash
docker-compose exec api alembic upgrade head
``` 