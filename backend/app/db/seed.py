import csv
from datetime import datetime
from pathlib import Path
from typing import List

from sqlalchemy.orm import Session

from app.models.well import Well
from app.models.production import ProductionData
from app.core.config import settings

def read_sample_data() -> List[dict]:
    """Read sample data from CSV file."""
    data_file = Path(settings.DATA_DIR) / settings.SAMPLE_DATA_FILE
    wells = {}
    production_data = []
    
    with open(data_file, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Create well if not exists
            if row['well_name'] not in wells:
                wells[row['well_name']] = {
                    'name': row['well_name'],
                    'latitude': float(row['latitude']),
                    'longitude': float(row['longitude']),
                    'region': row['region']
                }
            
            # Add production data
            production_data.append({
                'well_name': row['well_name'],
                'date': datetime.strptime(row['date'], '%Y-%m-%d').date(),
                'oil_volume': float(row['production_volume']),
                'gas_volume': 0.0,  # Default values for gas and water
                'water_volume': 0.0
            })
    
    return list(wells.values()), production_data

def seed_database(db: Session) -> None:
    """Seed the database with sample data."""
    # Check if data already exists
    existing_wells = db.query(Well).count()
    if existing_wells > 0:
        print("Data already exists, skipping seeding.")
        return

    wells_data, production_data = read_sample_data()
    
    # Create wells
    wells = {}
    for well_data in wells_data:
        well = Well(**well_data)
        db.add(well)
        db.flush()  # Get the well ID
        wells[well.name] = well
    
    # Create production data
    for prod_data in production_data:
        well_name = prod_data.pop('well_name')
        well = wells[well_name]
        production = ProductionData(well_id=well.id, **prod_data)
        db.add(production)
    
    db.commit() 