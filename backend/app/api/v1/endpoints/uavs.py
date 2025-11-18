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
    limit: int = 100,
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
    # Query all UAV variants with their family and manufacturer information
    query = """
    FOR variant IN platform_variants
        LET family = FIRST(
            FOR f IN 1..1 OUTBOUND variant belongs_to_family
                RETURN f
        )
        LET manufacturer = FIRST(
            FOR m IN 1..1 OUTBOUND family manufactured_by
                RETURN m
        )
        SORT variant.name
        LIMIT @skip, @limit
        RETURN {
            id: variant._key,
            name: variant.name,
            manufacturer: manufacturer ? manufacturer.name : family.manufacturer,
            country: family ? family.country : "Unknown",
            description: variant.description,
            category: variant.airframe_type,
            designation: variant.designation,
            development_status: variant.development_status,
            first_flight: variant.first_flight,
            specifications: []
        }
    """

    # Get total count
    count_query = "RETURN LENGTH(platform_variants)"

    try:
        # Execute queries
        cursor = db.aql.execute(query, bind_vars={"skip": skip, "limit": limit})
        count_cursor = db.aql.execute(count_query)

        platforms = list(cursor)
        total = next(count_cursor)

        return UAVListResponse(
            platforms=platforms,
            total=total,
            skip=skip,
            limit=limit
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database query failed: {str(e)}")


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
