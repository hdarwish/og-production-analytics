from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from sqlalchemy import select
from datetime import date
from app.core.logging import logger
from pydantic import ValidationError

from app.db.deps import get_db
from app.schemas.production import ProductionDataCreate, ProductionDataUpdate, ProductionDataResponse
from app.models.production import ProductionData as ProductionDataModel
from app.models.well import Well

router = APIRouter()

@router.get("/", response_model=List[ProductionDataResponse])
def read_production_data(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    region: Optional[str] = Query(None, description="Filter by region"),
    well_name: Optional[str] = Query(None, description="Filter by well name"),
    start_date: Optional[date] = Query(None, description="Filter by start date"),
    end_date: Optional[date] = Query(None, description="Filter by end date"),
):
    """
    Retrieve production data with well information and filtering options.
    """
    try:
        # Query production data with well information
        query = (
            db.query(ProductionDataModel, Well.name)
            .join(Well, ProductionDataModel.well_id == Well.id)
        )
        
        # Apply filters if provided
        if region:
            query = query.filter(Well.region == region)
        if well_name:
            query = query.filter(Well.name == well_name)
        if start_date:
            query = query.filter(ProductionDataModel.date >= start_date)
        if end_date:
            query = query.filter(ProductionDataModel.date <= end_date)
        
        # Apply pagination
        query = query.offset(skip).limit(limit)
        
        results = query.all()
        
        # Convert to response model with well information
        response_data = []
        for prod, well_name in results:
            response_data.append({
                "well_name": well_name,
                "date": prod.date,
                "oil_volume": prod.oil_volume,
                "region": prod.well.region if prod.well else None
            })
        
        return response_data
    except Exception as e:
        logger.error(f"Error retrieving production data: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving production data: {str(e)}"
        )

@router.post("/", response_model=ProductionDataResponse, status_code=status.HTTP_201_CREATED)
def create_production_data(
    *,
    db: Session = Depends(get_db),
    production_in: ProductionDataCreate,
):
    """
    Create new production data entry.
    """
    try:
        # First check if the well exists
        well = db.query(Well).filter(Well.id == production_in.well_id).first()
        if not well:
            logger.error(f"Well with ID {production_in.well_id} not found")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Well with ID {production_in.well_id} not found"
            )
        
        # Check if a record already exists for this well and date
        existing_record = (
            db.query(ProductionDataModel)
            .filter(
                ProductionDataModel.well_id == production_in.well_id,
                ProductionDataModel.date == production_in.date
            )
            .first()
        )
        
        if existing_record:
            logger.warning(f"Production data already exists for well_id={production_in.well_id} on date={production_in.date}")
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Production data already exists for well_id={production_in.well_id} on date={production_in.date}"
            )
        
        # Create new production data
        production_data = ProductionDataModel(**production_in.model_dump())
        db.add(production_data)
        
        try:
            db.commit()
            db.refresh(production_data)
        except Exception as e:
            db.rollback()
            logger.error(f"Database error when creating production data: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Database error when creating production data: {str(e)}"
            )
        
        # Return the response with well information
        return ProductionDataResponse(
            well_name=well.name,
            date=production_data.date,
            oil_volume=production_data.oil_volume,
            region=well.region
        )
        
    except ValidationError as e:
        logger.error(f"Validation error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Validation error: {str(e)}"
        )
    except HTTPException:
        # Re-raise HTTP exceptions to preserve their status codes and details
        raise
    except Exception as e:
        logger.error(f"Unexpected error creating production data: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Unexpected error creating production data: {str(e)}"
        )

@router.get("/well/{well_id}", response_model=List[ProductionDataResponse])
def read_well_production(
    *,
    db: Session = Depends(get_db),
    well_id: int,
    start_date: date = None,
    end_date: date = None,
):
    """
    Get production data for a specific well with region information.
    """
    try:
        # Check if well exists
        well = db.query(Well).filter(Well.id == well_id).first()
        if not well:
            logger.error(f"Well with ID {well_id} not found")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Well with ID {well_id} not found"
            )
            
        query = (
            db.query(ProductionDataModel, Well.region)
            .join(Well, ProductionDataModel.well_id == Well.id)
            .filter(ProductionDataModel.well_id == well_id)
        )
        
        if start_date:
            query = query.filter(ProductionDataModel.date >= start_date)
        if end_date:
            query = query.filter(ProductionDataModel.date <= end_date)
            
        results = query.all()
        return [
            ProductionDataResponse(
                well_name=prod.well.name,
                date=prod.date,
                oil_volume=prod.oil_volume,
                region=region
            )
            for prod, region in results
        ]
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving well production data: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving well production data: {str(e)}"
        )

@router.put("/{production_id}", response_model=ProductionDataResponse)
def update_production_data(
    *,
    db: Session = Depends(get_db),
    production_id: int,
    production_in: ProductionDataUpdate,
):
    """
    Update production data.
    """
    try:
        production = db.query(ProductionDataModel).filter(ProductionDataModel.id == production_id).first()
        if not production:
            logger.error(f"Production data with ID {production_id} not found")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Production data with ID {production_id} not found"
            )
        
        # Check if well_id is being updated and if the new well exists
        if production_in.well_id is not None and production_in.well_id != production.well_id:
            well = db.query(Well).filter(Well.id == production_in.well_id).first()
            if not well:
                logger.error(f"Well with ID {production_in.well_id} not found")
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Well with ID {production_in.well_id} not found"
                )
        
        # Update production data fields
        for field, value in production_in.model_dump(exclude_unset=True).items():
            setattr(production, field, value)
        
        try:
            db.add(production)
            db.commit()
            db.refresh(production)
        except Exception as e:
            db.rollback()
            logger.error(f"Database error when updating production data: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Database error when updating production data: {str(e)}"
            )
        
        # Get the well's region
        well = db.query(Well).filter(Well.id == production.well_id).first()
        return ProductionDataResponse(
            well_name=well.name,
            date=production.date,
            oil_volume=production.oil_volume,
            region=well.region
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error updating production data: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Unexpected error updating production data: {str(e)}"
        )

@router.delete("/{production_id}")
def delete_production_data(
    *,
    db: Session = Depends(get_db),
    production_id: int,
):
    """
    Delete production data.
    """
    try:
        production = db.query(ProductionDataModel).filter(ProductionDataModel.id == production_id).first()
        if not production:
            logger.error(f"Production data with ID {production_id} not found")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Production data with ID {production_id} not found"
            )
        
        try:
            db.delete(production)
            db.commit()
        except Exception as e:
            db.rollback()
            logger.error(f"Database error when deleting production data: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Database error when deleting production data: {str(e)}"
            )
            
        return {"ok": True}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error deleting production data: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Unexpected error deleting production data: {str(e)}"
        ) 