"""
UAV Pydantic schemas.

Request and response models for UAV endpoints.
"""

from typing import List, Optional
from pydantic import BaseModel, Field


class UAVSpecification(BaseModel):
    """UAV technical specification."""

    name: str = Field(..., description="Specification name")
    value: float = Field(..., description="Specification value")
    unit: str = Field(..., description="Unit of measurement")
    category: str = Field(..., description="Specification category")


class UAVPlatformBase(BaseModel):
    """Base UAV platform schema."""

    name: str = Field(..., description="Platform name")
    manufacturer: str = Field(..., description="Manufacturer name")
    country: str = Field(..., description="Manufacturing country")
    description: Optional[str] = Field(None, description="Platform description")


class UAVPlatformResponse(UAVPlatformBase):
    """UAV platform response schema."""

    id: str = Field(..., description="Platform ID")
    category: str = Field(..., description="UAV category (e.g., MALE, HALE)")
    specifications: List[UAVSpecification] = Field(default_factory=list)

    class Config:
        from_attributes = True


class UAVListResponse(BaseModel):
    """UAV list response with pagination."""

    platforms: List[UAVPlatformResponse] = Field(default_factory=list)
    total: int = Field(..., description="Total number of platforms")
    skip: int = Field(..., description="Number of skipped records")
    limit: int = Field(..., description="Maximum records returned")
