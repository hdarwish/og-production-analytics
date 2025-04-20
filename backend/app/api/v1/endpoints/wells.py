from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api import deps
from app.schemas.well import WellCreate, WellUpdate, Well
from app.models.well import Well as WellModel

router = APIRouter()

@router.get("/", response_model=List[Well])
def read_wells(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
):
    """
    Retrieve wells.
    """
    return db.query(WellModel).offset(skip).limit(limit).all()

@router.post("/", response_model=Well)
def create_well(
    *,
    db: Session = Depends(deps.get_db),
    well_in: WellCreate,
):
    """
    Create new well.
    """
    well = WellModel(**well_in.model_dump())
    db.add(well)
    db.commit()
    db.refresh(well)
    return well

@router.get("/{well_id}", response_model=Well)
def read_well(
    *,
    db: Session = Depends(deps.get_db),
    well_id: int,
):
    """
    Get well by ID.
    """
    well = db.query(WellModel).filter(WellModel.id == well_id).first()
    if not well:
        raise HTTPException(status_code=404, detail="Well not found")
    return well

@router.put("/{well_id}", response_model=Well)
def update_well(
    *,
    db: Session = Depends(deps.get_db),
    well_id: int,
    well_in: WellUpdate,
):
    """
    Update well.
    """
    well = db.query(WellModel).filter(WellModel.id == well_id).first()
    if not well:
        raise HTTPException(status_code=404, detail="Well not found")
    for field, value in well_in.model_dump(exclude_unset=True).items():
        setattr(well, field, value)
    db.add(well)
    db.commit()
    db.refresh(well)
    return well

@router.delete("/{well_id}")
def delete_well(
    *,
    db: Session = Depends(deps.get_db),
    well_id: int,
):
    """
    Delete well.
    """
    well = db.query(WellModel).filter(WellModel.id == well_id).first()
    if not well:
        raise HTTPException(status_code=404, detail="Well not found")
    db.delete(well)
    db.commit()
    return {"ok": True} 