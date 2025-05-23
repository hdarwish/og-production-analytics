from pydantic_settings import BaseSettings
from functools import lru_cache
from typing import List, Optional

class Settings(BaseSettings):
    PROJECT_NAME: str = "Oil & Gas Production Analytics"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    
    # CORS settings
    BACKEND_CORS_ORIGINS: List[str] = ["http://localhost:4200"]
    
    # Data settings
    DATA_DIR: str = "data"
    SAMPLE_DATA_FILE: str = "sample_data.csv"
    
    # Server settings
    BACKEND_PORT: str = "8000"
    
    # Database settings
    POSTGRES_SERVER: str 
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str 
    POSTGRES_DB: str 
    POSTGRES_PORT: str
    
    SQLALCHEMY_DATABASE_URI: Optional[str] = None
    
    @property
    def get_database_url(self) -> str:
        return f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_SERVER}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
    
    class Config:
        case_sensitive = True
        env_file = ".env"
        extra = "allow"  # Allow extra fields in environment variables

@lru_cache()
def get_settings() -> Settings:
    return Settings()

settings = get_settings()
settings.SQLALCHEMY_DATABASE_URI = settings.get_database_url 