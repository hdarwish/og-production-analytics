from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base_class import Base

class Well(Base):
    __tablename__ = "wells"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    latitude = Column(Float)
    longitude = Column(Float)
    field = Column(String, index=True)
    operator = Column(String, index=True)
    production_rate = Column(Float)
    last_updated = Column(DateTime)
    production_data = relationship("ProductionData", back_populates="well") 