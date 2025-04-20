from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()

class ChatbotRequest(BaseModel):
    message: str

class ChatbotResponse(BaseModel):
    response: str

@router.post("/", response_model=ChatbotResponse)
async def chatbot_response(request: ChatbotRequest):
    """
    Process a chatbot request and return a response.
    """
    responses = {
        "help": "I can help you with information about wells, production data, and analytics. Try asking about specific wells, production volumes, or trends.",
        "wells": "We have information about multiple wells including their location, production rates, and historical data.",
        "production": "Production data includes oil, gas, and water volumes for each well over time.",
        "analytics": "You can view analytics like total production by field, average production per well, and production trends.",
        "default": "I'm here to help! Try asking about wells, production data, available fields, or viewing trends."
    }
    
    message = request.message.lower()
    
    if "help" in message:
        return {"response": responses["help"]}
    elif "well" in message:
        return {"response": responses["wells"]}
    elif "product" in message:
        return {"response": responses["production"]}
    elif "analytic" in message or "statistic" in message or "trend" in message:
        return {"response": responses["analytics"]}
    else:
        return {"response": responses["default"]} 