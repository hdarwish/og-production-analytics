from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import pandas as pd
import os

app = FastAPI(title="Oil Production Analytics API")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],
    allow_credentials=True,
    allow_methods=["GET", "POST"],  
    allow_headers=["Content-Type", "Accept"],  
    max_age=3600 
)

class Well(BaseModel):
    well_name: str
    latitude: float
    longitude: float
    region: str

class ProductionData(BaseModel):
    well_name: str
    date: str
    production_volume: float
    region: str
    latitude: float
    longitude: float

class ChatbotRequest(BaseModel):
    message: str

# Load sample data
def load_sample_data():
    # Create sample data if it doesn't exist
    if not os.path.exists("data/sample_data.csv"):
        os.makedirs("data", exist_ok=True)
        data = {
            "well_name": ["Well-1", "Well-2", "Well-3"],
            "date": ["2023-01-01", "2023-01-02", "2023-01-03"],
            "production_volume": [1000, 1200, 1100],
            "latitude": [30.0, 30.1, 30.2],
            "longitude": [-95.0, -95.1, -95.2],
            "region": ["North", "South", "East"]
        }
        df = pd.DataFrame(data)
        df.to_csv("data/sample_data.csv", index=False)
    return pd.read_csv("data/sample_data.csv")

@app.get("/api/wells", response_model=List[Well])
async def get_wells():
    df = load_sample_data()
    wells = df[["well_name", "latitude", "longitude", "region"]].drop_duplicates()
    return wells.to_dict(orient="records")

@app.get("/api/production", response_model=List[ProductionData])
async def get_production(
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    well_name: Optional[str] = None,
    region: Optional[str] = None
):
    df = load_sample_data()

    if start_date:
        df = df[df["date"] >= start_date]
    if end_date:
        df = df[df["date"] <= end_date]
    if well_name:
        df = df[df["well_name"] == well_name]
    if region:
        df = df[df["region"] == region]
    
    return df[["well_name", "date", "production_volume", "region", "latitude", "longitude"]].to_dict(orient="records")

@app.post("/api/chatbot")
async def chatbot_response(request: ChatbotRequest):
    responses = {
        "default": "I'm here to help! Try asking about filtering data, available data, or viewing trends."
    }
    
    message = request.message.lower()
    return {"response": responses.get(message, responses["default"])}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 