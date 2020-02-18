from fastapi import APIRouter

#from app.api.api_v1.endpoints.user import router as user_router
from app.api.v1.endpoints.login import router as login_router
from app.api.v1.endpoints.broker import router as broker_router
from app.api.v1.endpoints.property import router as property_router

api_routers = APIRouter()
api_routers.include_router(login_router, tags=["Login"])
api_routers.include_router(broker_router, tags=["Brokers"], prefix="/brokers")
api_routers.include_router(property_router, tags=["Properties"], prefix="/properties")