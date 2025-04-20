from typing import Generator
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.deps import get_db

# Database dependency
def get_db_dependency() -> Generator[Session, None, None]:
    """
    Get database session dependency.
    """
    return get_db()
