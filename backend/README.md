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

## Setup

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
│   │   │   │   └── production.py
│   │   │   └── router.py
│   │   └── deps.py
│   ├── core/
│   │   ├── config.py
│   │   └── security.py
│   ├── models/
│   │   ├── well.py
│   │   └── production.py
│   ├── schemas/
│   │   ├── well.py
│   │   └── production.py
│   └── services/
│       └── production_service.py
├── alembic/
│   └── versions/
└── tests/
    └── api/
        └── test_wells.py
```

## Development

- Use `alembic revision --autogenerate -m "message"` to create new migrations
- Run tests with `pytest`
- Format code with `black .`
- Check types with `mypy .` 