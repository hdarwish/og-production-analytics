from typing import Optional
from datetime import datetime
from pydantic import BaseModel

class WellBase(BaseModel):
    name: str
    latitude: float
    longitude: float
    field: Optional[str] = None
    operator: Optional[str] = None
    production_rate: Optional[float] = None

class WellCreate(WellBase):
    pass

class WellUpdate(WellBase):
    name: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None

class Well(WellBase):
    id: int
    last_updated: Optional[datetime] = None

    class Config:
        from_attributes = True
