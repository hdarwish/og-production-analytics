from typing import Optional
from pydantic import BaseModel

class WellBase(BaseModel):
    name: str
    latitude: float
    longitude: float
    region: Optional[str] = None

class WellCreate(WellBase):
    pass

class WellUpdate(WellBase):
    name: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    region: Optional[str] = None

class Well(WellBase):
    id: int

    class Config:
        from_attributes = True

class WellResponse(WellBase):
    class Config:
        from_attributes = True
