from typing import Optional
from datetime import date
from pydantic import BaseModel

class ProductionDataBase(BaseModel):
    well_id: int
    date: date
    oil_volume: Optional[float] = None
    gas_volume: Optional[float] = None
    water_volume: Optional[float] = None

class ProductionDataCreate(ProductionDataBase):
    pass

class ProductionDataUpdate(ProductionDataBase):
    well_id: Optional[int] = None
    date: Optional[date] = None

class ProductionDataResponse(BaseModel):
    well_name: str
    date: date
    oil_volume: Optional[float] = None
    region: str

    class Config:
        from_attributes = True
