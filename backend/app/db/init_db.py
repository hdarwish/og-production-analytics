from sqlalchemy.orm import Session

from app.db.base import Base
from app.db.session import engine
from app.db.seed import seed_database

def init_db(db: Session) -> None:
    """Initialize the database with tables and seed data."""
    # Create all tables
    Base.metadata.create_all(bind=engine)
    
    # Seed the database with sample data
    seed_database(db) 