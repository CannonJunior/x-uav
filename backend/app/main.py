"""
Main FastAPI application for X-UAV backend.

Provides REST API endpoints for UAV data access and comparison.
"""

from typing import List

from fastapi import FastAPI, HTTPException, Path as FastAPIPath
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from .config import settings
from .database import db
from .schemas import (
    HealthResponse,
    StatsResponse,
    UAV,
    UAVCompareRequest,
    UAVList,
    UAVSearchRequest,
)

# Create FastAPI application
app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="API for comparing military and government UAVs worldwide",
    docs_url="/docs",
    redoc_url="/redoc",
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", tags=["Root"])
async def root():
    """
    Root endpoint.

    Returns:
        dict: Welcome message and API information
    """
    return {
        "message": "Welcome to X-UAV API",
        "version": settings.VERSION,
        "docs": "/docs",
        "api": settings.API_V1_PREFIX,
    }


@app.get(f"{settings.API_V1_PREFIX}/health", response_model=HealthResponse, tags=["Health"])
async def health_check():
    """
    Health check endpoint.

    Returns:
        HealthResponse: Service health status
    """
    try:
        # Test database connection
        stats = db.get_stats()
        database_status = f"OK ({stats['total']} UAVs)"
    except Exception as e:
        database_status = f"ERROR: {str(e)}"

    return HealthResponse(
        status="healthy",
        version=settings.VERSION,
        database=database_status,
    )


@app.get(f"{settings.API_V1_PREFIX}/stats", response_model=StatsResponse, tags=["Statistics"])
async def get_statistics():
    """
    Get database statistics.

    Returns:
        StatsResponse: Statistics including counts by country, type, status
    """
    try:
        stats = db.get_stats()
        return StatsResponse(**stats)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching statistics: {str(e)}")


@app.get(f"{settings.API_V1_PREFIX}/uavs", response_model=UAVList, tags=["UAVs"])
async def list_uavs():
    """
    List all UAVs.

    Returns:
        UAVList: List of all UAV records
    """
    try:
        uavs = db.get_all_uavs()
        return UAVList(total=len(uavs), uavs=uavs)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching UAVs: {str(e)}")


@app.get(
    f"{settings.API_V1_PREFIX}/uavs/{{designation}}",
    response_model=UAV,
    tags=["UAVs"]
)
async def get_uav(
    designation: str = FastAPIPath(..., description="UAV designation (e.g., MQ-9)")
):
    """
    Get specific UAV by designation.

    Args:
        designation: UAV designation code

    Returns:
        UAV: UAV record

    Raises:
        HTTPException: 404 if UAV not found
    """
    try:
        uav = db.get_uav_by_designation(designation)
        if uav is None:
            raise HTTPException(
                status_code=404,
                detail=f"UAV with designation '{designation}' not found"
            )
        return UAV(**uav)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching UAV: {str(e)}")


@app.post(f"{settings.API_V1_PREFIX}/uavs/compare", response_model=UAVList, tags=["UAVs"])
async def compare_uavs(request: UAVCompareRequest):
    """
    Compare multiple UAVs.

    Args:
        request: Comparison request with list of designations

    Returns:
        UAVList: List of UAVs for comparison
    """
    try:
        uavs = db.compare_uavs(request.designations)
        return UAVList(total=len(uavs), uavs=uavs)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error comparing UAVs: {str(e)}")


@app.post(f"{settings.API_V1_PREFIX}/uavs/search", response_model=UAVList, tags=["UAVs"])
async def search_uavs(request: UAVSearchRequest):
    """
    Search UAVs with filters.

    Args:
        request: Search request with filter parameters

    Returns:
        UAVList: Filtered list of UAVs
    """
    try:
        uavs = db.search_uavs(
            country=request.country,
            uav_type=request.type,
            status=request.status,
            nato_class=request.nato_class,
        )
        return UAVList(total=len(uavs), uavs=uavs)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error searching UAVs: {str(e)}")


@app.get(
    f"{settings.API_V1_PREFIX}/filters/countries",
    response_model=List[str],
    tags=["Filters"]
)
async def get_countries():
    """
    Get list of all countries.

    Returns:
        List[str]: List of country names
    """
    try:
        return db.get_countries()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching countries: {str(e)}")


@app.get(
    f"{settings.API_V1_PREFIX}/filters/types",
    response_model=List[str],
    tags=["Filters"]
)
async def get_types():
    """
    Get list of all UAV types.

    Returns:
        List[str]: List of UAV types
    """
    try:
        return db.get_types()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching types: {str(e)}")


# =====================================================
# ARMAMENT ENDPOINTS
# =====================================================

@app.get(f"{settings.API_V1_PREFIX}/armaments", tags=["Armaments"])
async def list_armaments():
    """
    List all armaments.

    Returns:
        dict: List of all armament records
    """
    try:
        armaments = db.get_all_armaments()
        return {"total": len(armaments), "armaments": armaments}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching armaments: {str(e)}")


@app.get(
    f"{settings.API_V1_PREFIX}/armaments/{{designation}}",
    tags=["Armaments"]
)
async def get_armament(
    designation: str = FastAPIPath(..., description="Armament designation (e.g., AGM-114)")
):
    """
    Get specific armament by designation.

    Args:
        designation: Armament designation code

    Returns:
        dict: Armament record

    Raises:
        HTTPException: 404 if armament not found
    """
    try:
        armament = db.get_armament_by_designation(designation)
        if armament is None:
            raise HTTPException(
                status_code=404,
                detail=f"Armament with designation '{designation}' not found"
            )
        return armament
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching armament: {str(e)}")


@app.get(f"{settings.API_V1_PREFIX}/armaments/search", tags=["Armaments"])
async def search_armaments(
    weapon_type: str = None,
    weapon_class: str = None,
    country: str = None,
    guidance_type: str = None
):
    """
    Search armaments with filters.

    Args:
        weapon_type: Filter by type (Missile, Bomb, etc.)
        weapon_class: Filter by class (Air-to-Ground, etc.)
        country: Filter by country of origin
        guidance_type: Filter by guidance type

    Returns:
        dict: Filtered list of armaments
    """
    try:
        armaments = db.search_armaments(
            weapon_type=weapon_type,
            weapon_class=weapon_class,
            country=country,
            guidance_type=guidance_type
        )
        return {"total": len(armaments), "armaments": armaments}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error searching armaments: {str(e)}")


@app.get(
    f"{settings.API_V1_PREFIX}/uavs/{{designation}}/armaments",
    tags=["UAV Armaments"]
)
async def get_uav_armaments(
    designation: str = FastAPIPath(..., description="UAV designation (e.g., MQ-9)")
):
    """
    Get all armaments compatible with a specific UAV.

    Args:
        designation: UAV designation code

    Returns:
        dict: List of armaments with integration details
    """
    try:
        armaments = db.get_armaments_for_uav(designation)
        return {"uav_designation": designation, "total": len(armaments), "armaments": armaments}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching UAV armaments: {str(e)}")


@app.get(
    f"{settings.API_V1_PREFIX}/armaments/{{designation}}/uavs",
    tags=["UAV Armaments"]
)
async def get_armament_uavs(
    designation: str = FastAPIPath(..., description="Armament designation (e.g., AGM-114)")
):
    """
    Get all UAVs that can carry a specific armament.

    Args:
        designation: Armament designation code

    Returns:
        dict: List of UAVs with integration details
    """
    try:
        uavs = db.get_uavs_for_armament(designation)
        return {"armament_designation": designation, "total": len(uavs), "uavs": uavs}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching armament UAVs: {str(e)}")


@app.get(
    f"{settings.API_V1_PREFIX}/filters/weapon-types",
    response_model=List[str],
    tags=["Filters"]
)
async def get_weapon_types():
    """Get list of all weapon types."""
    try:
        return db.get_weapon_types()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching weapon types: {str(e)}")


@app.get(
    f"{settings.API_V1_PREFIX}/filters/weapon-classes",
    response_model=List[str],
    tags=["Filters"]
)
async def get_weapon_classes():
    """Get list of all weapon classes."""
    try:
        return db.get_weapon_classes()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching weapon classes: {str(e)}")


# Error handlers
@app.exception_handler(404)
async def not_found_handler(request, exc):
    """
    Handle 404 errors.

    Args:
        request: HTTP request
        exc: Exception

    Returns:
        JSONResponse: 404 error response
    """
    return JSONResponse(
        status_code=404,
        content={"detail": "Resource not found"}
    )


@app.exception_handler(500)
async def internal_error_handler(request, exc):
    """
    Handle 500 errors.

    Args:
        request: HTTP request
        exc: Exception

    Returns:
        JSONResponse: 500 error response
    """
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"}
    )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.RELOAD,
    )
