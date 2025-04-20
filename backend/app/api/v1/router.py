from fastapi import APIRouter
from app.api.v1.endpoints import wells, production, chatbot

api_router = APIRouter()

api_router.include_router(wells.router, prefix="/wells", tags=["wells"])
api_router.include_router(production.router, prefix="/production", tags=["production"])
api_router.include_router(chatbot.router, prefix="/chatbot", tags=["chatbot"])
