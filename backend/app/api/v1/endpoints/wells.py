from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import ValidationError

from app.db.deps import get_db
from app.schemas.well import WellCreate, WellUpdate, Well, WellResponse
from app.models.well import Well as WellModel
from app.core.logging import logger

router = APIRouter()

@router.get("/", response_model=List[WellResponse])
def read_wells(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
):
    """
    Retrieve wells.
    """
    try:
        wells = db.query(WellModel).offset(skip).limit(limit).all()
        logger.info(f"Retrieved {len(wells)} wells")
        return wells
    except Exception as e:
        logger.error(f"Error retrieving wells: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving wells: {str(e)}"
        )

@router.post("/", response_model=Well, status_code=status.HTTP_201_CREATED)
def create_well(
    *,
    db: Session = Depends(get_db),
    well_in: WellCreate,
):
    """
    Create new well.
    """
    try:
        # Check if well with same name already exists
        existing_well = db.query(WellModel).filter(WellModel.name == well_in.name).first()
        if existing_well:
            logger.warning(f"Well with name {well_in.name} already exists")
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Well with name {well_in.name} already exists"
            )

        well = WellModel(**well_in.model_dump())
        db.add(well)
        try:
            db.commit()
            db.refresh(well)
            logger.info(f"Created new well: {well.name}")
            return well
        except Exception as e:
            db.rollback()
            logger.error(f"Database error when creating well: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Database error when creating well: {str(e)}"
            )
    except ValidationError as e:
        logger.error(f"Validation error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Validation error: {str(e)}"
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error creating well: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Unexpected error creating well: {str(e)}"
        )

@router.get("/{well_id}", response_model=WellResponse)
def read_well(
    *,
    db: Session = Depends(get_db),
    well_id: int,
):
    """
    Get well by ID.
    """
    try:
        well = db.query(WellModel).filter(WellModel.id == well_id).first()
        if not well:
            logger.error(f"Well with ID {well_id} not found")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Well with ID {well_id} not found"
            )
        logger.info(f"Retrieved well: {well.name}")
        return well
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving well: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving well: {str(e)}"
        )

@router.put("/{well_id}", response_model=Well)
def update_well(
    *,
    db: Session = Depends(get_db),
    well_id: int,
    well_in: WellUpdate,
):
    """
    Update well.
    """
    try:
        well = db.query(WellModel).filter(WellModel.id == well_id).first()
        if not well:
            logger.error(f"Well with ID {well_id} not found")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Well with ID {well_id} not found"
            )

        # Check if new name conflicts with existing well
        if well_in.name and well_in.name != well.name:
            existing_well = db.query(WellModel).filter(WellModel.name == well_in.name).first()
            if existing_well:
                logger.warning(f"Well with name {well_in.name} already exists")
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail=f"Well with name {well_in.name} already exists"
                )

        for field, value in well_in.model_dump(exclude_unset=True).items():
            setattr(well, field, value)
        
        try:
            db.add(well)
            db.commit()
            db.refresh(well)
            logger.info(f"Updated well: {well.name}")
            return well
        except Exception as e:
            db.rollback()
            logger.error(f"Database error when updating well: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Database error when updating well: {str(e)}"
            )
    except ValidationError as e:
        logger.error(f"Validation error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Validation error: {str(e)}"
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error updating well: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Unexpected error updating well: {str(e)}"
        )

@router.delete("/{well_id}")
def delete_well(
    *,
    db: Session = Depends(get_db),
    well_id: int,
):
    """
    Delete well.
    """
    try:
        well = db.query(WellModel).filter(WellModel.id == well_id).first()
        if not well:
            logger.error(f"Well with ID {well_id} not found")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Well with ID {well_id} not found"
            )

        try:
            db.delete(well)
            db.commit()
            logger.info(f"Deleted well with ID: {well_id}")
            return {"ok": True}
        except Exception as e:
            db.rollback()
            logger.error(f"Database error when deleting well: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Database error when deleting well: {str(e)}"
            )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error deleting well: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Unexpected error deleting well: {str(e)}"
        ) 