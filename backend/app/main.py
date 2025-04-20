from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
from app.core.config import settings
from app.api.v1.router import api_router
from app.db.session import SessionLocal
from app.db.init_db import init_db
from app.core.logging import setup_logging

# Setup logging
logger = setup_logging()

# Initialize the FastAPI app
app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
)

# Configure CORS
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

# Include API router
app.include_router(api_router, prefix=settings.API_V1_STR)

# Create data directory if it doesn't exist
os.makedirs(settings.DATA_DIR, exist_ok=True)

# Initialize database and seed data
@app.on_event("startup")
def startup_event():
    """
    Initialize the database on startup.
    """
    logger.info("Initializing database")
    db = SessionLocal()
    try:
        init_db(db)
    finally:
        db.close()
    logger.info("Database initialized successfully")

@app.get("/")
async def root():
    """
    Root endpoint - health check and basic info.
    """
    return {
        "status": "online",
        "app_name": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "api_docs": "/docs",
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True) 