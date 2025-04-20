from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import date

from app.api import deps
from app.schemas.production import ProductionDataCreate, ProductionDataUpdate, ProductionData
from app.models.production import ProductionData as ProductionDataModel

router = APIRouter()

@router.get("/", response_model=List[ProductionData])
def read_production_data(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
):
    """
    Retrieve production data.
    """
    return db.query(ProductionDataModel).offset(skip).limit(limit).all()

@router.post("/", response_model=ProductionData)
def create_production_data(
    *,
    db: Session = Depends(deps.get_db),
    production_in: ProductionDataCreate,
):
    """
    Create new production data entry.
    """
    production = ProductionDataModel(**production_in.model_dump())
    db.add(production)
    db.commit()
    db.refresh(production)
    return production

@router.get("/well/{well_id}", response_model=List[ProductionData])
def read_well_production(
    *,
    db: Session = Depends(deps.get_db),
    well_id: int,
    start_date: date = None,
    end_date: date = None,
):
    """
    Get production data for a specific well.
    """
    query = db.query(ProductionDataModel).filter(ProductionDataModel.well_id == well_id)
    if start_date:
        query = query.filter(ProductionDataModel.date >= start_date)
    if end_date:
        query = query.filter(ProductionDataModel.date <= end_date)
    return query.all()

@router.put("/{production_id}", response_model=ProductionData)
def update_production_data(
    *,
    db: Session = Depends(deps.get_db),
    production_id: int,
    production_in: ProductionDataUpdate,
):
    """
    Update production data.
    """
    production = db.query(ProductionDataModel).filter(ProductionDataModel.id == production_id).first()
    if not production:
        raise HTTPException(status_code=404, detail="Production data not found")
    for field, value in production_in.model_dump(exclude_unset=True).items():
        setattr(production, field, value)
    db.add(production)
    db.commit()
    db.refresh(production)
    return production

@router.delete("/{production_id}")
def delete_production_data(
    *,
    db: Session = Depends(deps.get_db),
    production_id: int,
):
    """
    Delete production data.
    """
    production = db.query(ProductionDataModel).filter(ProductionDataModel.id == production_id).first()
    if not production:
        raise HTTPException(status_code=404, detail="Production data not found")
    db.delete(production)
    db.commit()
    return {"ok": True} 