"""
UAV endpoints.

CRUD operations for UAV platforms, variants, and configurations.
"""

from typing import List
from fastapi import APIRouter, Depends, HTTPException
from arango.database import StandardDatabase

from app.db.arangodb import get_arango_db
from app.schemas.uav import UAVPlatformResponse, UAVListResponse

router = APIRouter()


@router.get("/", response_model=UAVListResponse)
async def list_uavs(
    skip: int = 0,
    limit: int = 20,
    db: StandardDatabase = Depends(get_arango_db)
):
    """
    List all UAV platforms.

    Args:
        skip: Number of records to skip (pagination)
        limit: Maximum number of records to return
        db: ArangoDB database instance

    Returns:
        UAVListResponse: List of UAV platforms with pagination info
    """
    # Query all platforms
    # TODO: Implement proper pagination with AQL

    return UAVListResponse(
        platforms=[],
        total=0,
        skip=skip,
        limit=limit
    )


@router.get("/{uav_id}", response_model=UAVPlatformResponse)
async def get_uav(
    uav_id: str,
    db: StandardDatabase = Depends(get_arango_db)
):
    """
    Get UAV platform by ID.

    Args:
        uav_id: UAV platform ID
        db: ArangoDB database instance

    Returns:
        UAVPlatformResponse: UAV platform details

    Raises:
        HTTPException: If UAV not found
    """
    # TODO: Implement UAV retrieval from ArangoDB

    raise HTTPException(status_code=404, detail="UAV not found")


@router.post("/", response_model=UAVPlatformResponse, status_code=201)
async def create_uav(
    # uav: UAVPlatformCreate,
    db: StandardDatabase = Depends(get_arango_db)
):
    """
    Create new UAV platform.

    Args:
        uav: UAV platform data
        db: ArangoDB database instance

    Returns:
        UAVPlatformResponse: Created UAV platform
    """
    # TODO: Implement UAV creation

    raise HTTPException(status_code=501, detail="Not implemented")
