"""
API v1 router.

Aggregates all API v1 endpoints.
"""

from fastapi import APIRouter

from app.api.v1.endpoints import uavs, graph, search

api_router = APIRouter()

# Include endpoint routers
api_router.include_router(uavs.router, prefix="/uavs", tags=["UAVs"])
api_router.include_router(graph.router, prefix="/graph", tags=["Graph"])
api_router.include_router(search.router, prefix="/search", tags=["Search"])
