from typing import Generator
from fastapi import Depends
from sqlalchemy.orm import Session

from app.db.deps import get_db

# Database dependency
def get_db_dependency() -> Session:
    """
    Get database session dependency.
    """
    return Depends(get_db)
