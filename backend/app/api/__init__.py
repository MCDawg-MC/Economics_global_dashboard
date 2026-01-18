"""
API Router - Aggregates all API endpoints
"""
from fastapi import APIRouter
from app.api.endpoints import countries, momentum, indicators

api_router = APIRouter()

# Include endpoint routers
api_router.include_router(
    countries.router,
    prefix="/countries",
    tags=["countries"]
)

api_router.include_router(
    momentum.router,
    prefix="/momentum",
    tags=["momentum"]
)

api_router.include_router(
    indicators.router,
    prefix="/indicators",
    tags=["indicators"]
)
