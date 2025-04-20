from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from app.db.base_class import Base

Base = declarative_base()

class ProductionData(Base):
    __tablename__ = "production_data"

    id = Column(Integer, primary_key=True, index=True)
    well_id = Column(Integer, ForeignKey("wells.id"), index=True)
    date = Column(Date, index=True)
    oil_volume = Column(Float)
    gas_volume = Column(Float)
    water_volume = Column(Float)
    well = relationship("Well", back_populates="production_data") 