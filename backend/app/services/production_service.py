from typing import List, Optional, Tuple
from datetime import date
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.models.production import ProductionData
from app.models.well import Well

class ProductionService:
    @staticmethod
    def get_well_production_summary(
        db: Session,
        well_id: int,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
    ) -> dict:
        """
        Get production summary for a specific well.
        """
        query = db.query(
            func.sum(ProductionData.oil_volume).label("total_oil"),
            func.sum(ProductionData.gas_volume).label("total_gas"),
            func.sum(ProductionData.water_volume).label("total_water"),
            func.avg(ProductionData.oil_volume).label("avg_oil"),
            func.avg(ProductionData.gas_volume).label("avg_gas"),
            func.avg(ProductionData.water_volume).label("avg_water"),
        ).filter(ProductionData.well_id == well_id)

        if start_date:
            query = query.filter(ProductionData.date >= start_date)
        if end_date:
            query = query.filter(ProductionData.date <= end_date)

        result = query.first()
        
        return {
            "total_oil": float(result.total_oil) if result.total_oil else 0.0,
            "total_gas": float(result.total_gas) if result.total_gas else 0.0,
            "total_water": float(result.total_water) if result.total_water else 0.0,
            "avg_oil": float(result.avg_oil) if result.avg_oil else 0.0,
            "avg_gas": float(result.avg_gas) if result.avg_gas else 0.0,
            "avg_water": float(result.avg_water) if result.avg_water else 0.0,
        }

    @staticmethod
    def get_field_production_summary(
        db: Session,
        field: str,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
    ) -> dict:
        """
        Get production summary for a specific field.
        """
        query = db.query(
            func.sum(ProductionData.oil_volume).label("total_oil"),
            func.sum(ProductionData.gas_volume).label("total_gas"),
            func.sum(ProductionData.water_volume).label("total_water"),
        ).join(Well).filter(Well.field == field)

        if start_date:
            query = query.filter(ProductionData.date >= start_date)
        if end_date:
            query = query.filter(ProductionData.date <= end_date)

        result = query.first()
        
        return {
            "field": field,
            "total_oil": float(result.total_oil) if result.total_oil else 0.0,
            "total_gas": float(result.total_gas) if result.total_gas else 0.0,
            "total_water": float(result.total_water) if result.total_water else 0.0,
        }

    @staticmethod
    def get_top_producing_wells(
        db: Session,
        limit: int = 10,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
    ) -> List[Tuple[Well, float]]:
        """
        Get top producing wells based on oil production.
        """
        query = db.query(
            Well,
            func.sum(ProductionData.oil_volume).label("total_oil")
        ).join(ProductionData)

        if start_date:
            query = query.filter(ProductionData.date >= start_date)
        if end_date:
            query = query.filter(ProductionData.date <= end_date)

        return query.group_by(Well).order_by(func.sum(ProductionData.oil_volume).desc()).limit(limit).all()
