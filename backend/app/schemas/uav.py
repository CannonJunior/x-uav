"""
Pydantic schemas for UAV data models.

Defines request and response models for the API.
"""

from datetime import date, datetime
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class UAV(BaseModel):
    """
    UAV data model.

    Represents a complete UAV record with all specifications.
    """

    # Primary Key
    id: int

    # Identification & Classification
    designation: str = Field(..., description="Official model designation")
    name: Optional[str] = Field(None, description="Common name or nickname")
    manufacturer: Optional[str] = Field(None, description="Primary contractor/manufacturer")
    country_of_origin: Optional[str] = Field(None, description="Nation of origin")
    nato_class: Optional[str] = Field(None, description="NATO classification")
    type: Optional[str] = Field(None, description="UAV type (MALE, HALE, UCAV, etc.)")
    operational_status: Optional[str] = Field(None, description="Current operational status")
    initial_operating_capability: Optional[date] = Field(None, description="IOC date")
    total_units_produced: Optional[int] = Field(None, description="Total units manufactured")

    # Physical Characteristics
    wingspan_meters: Optional[float] = Field(None, description="Wingspan in meters")
    wingspan_feet: Optional[float] = Field(None, description="Wingspan in feet")
    length_meters: Optional[float] = Field(None, description="Length in meters")
    length_feet: Optional[float] = Field(None, description="Length in feet")
    height_meters: Optional[float] = Field(None, description="Height in meters")
    height_feet: Optional[float] = Field(None, description="Height in feet")
    empty_weight_kg: Optional[float] = Field(None, description="Empty weight in kg")
    empty_weight_lbs: Optional[float] = Field(None, description="Empty weight in lbs")
    max_takeoff_weight_kg: Optional[float] = Field(None, description="Max takeoff weight in kg")
    max_takeoff_weight_lbs: Optional[float] = Field(None, description="Max takeoff weight in lbs")
    payload_capacity_kg: Optional[float] = Field(None, description="Payload capacity in kg")
    payload_capacity_lbs: Optional[float] = Field(None, description="Payload capacity in lbs")
    fuel_capacity_kg: Optional[float] = Field(None, description="Fuel capacity in kg")
    fuel_capacity_gallons: Optional[float] = Field(None, description="Fuel capacity in gallons")
    airframe_type: Optional[str] = Field(None, description="Airframe design type")

    # Propulsion
    engine_type: Optional[str] = Field(None, description="Type of engine")
    engine_manufacturer: Optional[str] = Field(None, description="Engine manufacturer")
    engine_model: Optional[str] = Field(None, description="Engine model")
    thrust_hp: Optional[int] = Field(None, description="Thrust/power in horsepower")
    thrust_lbs: Optional[int] = Field(None, description="Thrust in pounds")
    number_of_engines: Optional[int] = Field(None, description="Number of engines")
    propeller_configuration: Optional[str] = Field(None, description="Propeller configuration")

    # Performance
    cruise_speed_kmh: Optional[float] = Field(None, description="Cruise speed in km/h")
    cruise_speed_mph: Optional[float] = Field(None, description="Cruise speed in mph")
    cruise_speed_knots: Optional[float] = Field(None, description="Cruise speed in knots")
    max_speed_kmh: Optional[float] = Field(None, description="Max speed in km/h")
    max_speed_mph: Optional[float] = Field(None, description="Max speed in mph")
    max_speed_mach: Optional[float] = Field(None, description="Max speed in Mach")
    service_ceiling_meters: Optional[float] = Field(None, description="Service ceiling in meters")
    service_ceiling_feet: Optional[float] = Field(None, description="Service ceiling in feet")
    range_km: Optional[float] = Field(None, description="Range in kilometers")
    range_miles: Optional[float] = Field(None, description="Range in miles")
    range_nm: Optional[float] = Field(None, description="Range in nautical miles")
    endurance_hours: Optional[float] = Field(None, description="Endurance in hours")
    combat_radius_km: Optional[float] = Field(None, description="Combat radius in km")
    combat_radius_nm: Optional[float] = Field(None, description="Combat radius in nm")

    # Mission Capabilities
    primary_function: Optional[str] = Field(None, description="Primary mission role")
    mission_types: Optional[List[str]] = Field(None, description="List of mission types")
    armament: Optional[List[str]] = Field(None, description="Compatible weapons")
    max_weapons_load_kg: Optional[float] = Field(None, description="Max weapons load in kg")
    max_weapons_load_lbs: Optional[float] = Field(None, description="Max weapons load in lbs")
    hardpoints: Optional[int] = Field(None, description="Number of hardpoints")
    internal_weapons_bays: Optional[bool] = Field(None, description="Has internal weapons bays")

    # Sensors & Avionics
    sensor_suite: Optional[List[str]] = Field(None, description="List of sensors")
    radar_type: Optional[str] = Field(None, description="Radar system type")
    communications: Optional[str] = Field(None, description="Communication systems")
    datalink_type: Optional[str] = Field(None, description="Datalink standard")
    stealth_features: Optional[str] = Field(None, description="Stealth features")
    autonomy_level: Optional[str] = Field(None, description="Autonomy level")

    # Operational Details
    operators: Optional[List[str]] = Field(None, description="Operating countries/orgs")
    export_countries: Optional[List[str]] = Field(None, description="Export destinations")
    crew_size_remote: Optional[int] = Field(None, description="Remote crew size")
    ground_control_station: Optional[str] = Field(None, description="GCS type")
    launch_method: Optional[str] = Field(None, description="Launch method")
    recovery_method: Optional[str] = Field(None, description="Recovery method")

    # Economic
    unit_cost_usd: Optional[float] = Field(None, description="Unit cost in USD")
    program_cost_usd: Optional[float] = Field(None, description="Total program cost")
    fiscal_year: Optional[int] = Field(None, description="Fiscal year for cost data")

    # Visual Assets
    imagery_urls: Optional[Dict[str, str]] = Field(None, description="Image URLs")
    silhouette_url: Optional[str] = Field(None, description="Silhouette URL")
    model_urls: Optional[Dict[str, str]] = Field(None, description="3D model URLs")
    scale_factor: Optional[int] = Field(None, description="Scale factor for visualization")

    # Additional Information
    notable_features: Optional[List[str]] = Field(None, description="Notable features")
    combat_history: Optional[str] = Field(None, description="Combat history")
    variants: Optional[List[Any]] = Field(None, description="Variants")
    notes: Optional[str] = Field(None, description="Additional notes")

    # Metadata
    created_at: Optional[datetime] = Field(None, description="Creation timestamp")
    updated_at: Optional[datetime] = Field(None, description="Last update timestamp")

    class Config:
        """Pydantic configuration."""
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "designation": "MQ-9",
                "name": "Reaper",
                "manufacturer": "General Atomics Aeronautical Systems, Inc.",
                "country_of_origin": "United States",
                "type": "MALE UCAV",
                "wingspan_meters": 20.1,
                "endurance_hours": 27,
            }
        }


class UAVList(BaseModel):
    """
    List of UAVs response model.

    Used for endpoints returning multiple UAVs.
    """

    total: int = Field(..., description="Total number of UAVs")
    uavs: List[UAV] = Field(..., description="List of UAV records")


class UAVCompareRequest(BaseModel):
    """
    Request model for comparing UAVs.

    Used for POST /api/uavs/compare endpoint.
    """

    designations: List[str] = Field(
        ...,
        description="List of UAV designations to compare",
        min_length=1,
        max_length=10,
        example=["MQ-9", "RQ-4", "TB2"]
    )


class UAVSearchRequest(BaseModel):
    """
    Request model for searching UAVs.

    Used for POST /api/uavs/search endpoint.
    """

    country: Optional[str] = Field(None, description="Filter by country")
    type: Optional[str] = Field(None, description="Filter by UAV type")
    status: Optional[str] = Field(None, description="Filter by operational status")
    nato_class: Optional[str] = Field(None, description="Filter by NATO class")

    class Config:
        """Pydantic configuration."""
        json_schema_extra = {
            "example": {
                "country": "United States",
                "type": "MALE",
                "status": "Active"
            }
        }


class HealthResponse(BaseModel):
    """
    Health check response model.

    Used for GET /api/health endpoint.
    """

    status: str = Field(..., description="Service status")
    version: str = Field(..., description="API version")
    database: str = Field(..., description="Database status")


class StatsResponse(BaseModel):
    """
    Statistics response model.

    Used for GET /api/stats endpoint.
    """

    total: int = Field(..., description="Total number of UAVs")
    by_country: List[Dict[str, Any]] = Field(..., description="Count by country")
    by_type: List[Dict[str, Any]] = Field(..., description="Count by type")
    by_status: List[Dict[str, Any]] = Field(..., description="Count by status")
