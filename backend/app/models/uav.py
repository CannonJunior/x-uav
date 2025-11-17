"""
UAV Pydantic models.

Comprehensive data models for platform families, variants, and configurations.
"""

from typing import Optional, List, Dict, Any
from datetime import date
from pydantic import BaseModel, Field, HttpUrl


class PlatformFamilyBase(BaseModel):
    """Base model for platform family."""

    name: str = Field(..., description="Platform family name", example="Fury")
    manufacturer: str = Field(..., description="Manufacturer name", example="Anduril")
    program: Optional[str] = Field(None, description="Development program", example="CCA Increment 1")
    base_technology: Optional[str] = Field(None, description="Base technology description")
    description: Optional[str] = Field(None, description="Family description")
    country: Optional[str] = Field(None, description="Manufacturing country", example="United States")


class PlatformFamilyCreate(PlatformFamilyBase):
    """Model for creating platform family."""
    pass


class PlatformFamily(PlatformFamilyBase):
    """Complete platform family model."""

    key: str = Field(..., alias="_key", description="ArangoDB document key")
    id: str = Field(..., alias="_id", description="ArangoDB document ID")

    class Config:
        populate_by_name = True
        from_attributes = True


class PlatformVariantBase(BaseModel):
    """Base model for platform variant."""

    name: str = Field(..., description="Variant name", example="YFQ-44A")
    designation: str = Field(..., description="Military designation", example="YFQ-44A")
    airframe_type: Optional[str] = Field(None, description="Airframe type", example="Fixed-wing")
    development_status: Optional[str] = Field(
        None,
        description="Development status",
        example="Flight testing"
    )
    first_flight: Optional[str] = Field(None, description="First flight date", example="2025-10-31")
    description: Optional[str] = Field(None, description="Variant description")


class PlatformVariantCreate(PlatformVariantBase):
    """Model for creating platform variant."""
    family_key: str = Field(..., description="Platform family key")


class PlatformVariant(PlatformVariantBase):
    """Complete platform variant model."""

    key: str = Field(..., alias="_key", description="ArangoDB document key")
    id: str = Field(..., alias="_id", description="ArangoDB document ID")

    class Config:
        populate_by_name = True
        from_attributes = True


class MissionConfigurationBase(BaseModel):
    """Base model for mission configuration."""

    name: str = Field(..., description="Configuration name", example="Fury-ISR")
    mission_type: str = Field(..., description="Mission type", example="ISR")
    payload_description: Optional[str] = Field(
        None,
        description="Payload description",
        example="EO/IR sensor package, SAR radar"
    )
    estimated_cost_per_sortie: Optional[float] = Field(
        None,
        description="Estimated cost per sortie in USD",
        example=45000.0
    )


class MissionConfigurationCreate(MissionConfigurationBase):
    """Model for creating mission configuration."""
    variant_key: str = Field(..., description="Platform variant key")


class MissionConfiguration(MissionConfigurationBase):
    """Complete mission configuration model."""

    key: str = Field(..., alias="_key", description="ArangoDB document key")
    id: str = Field(..., alias="_id", description="ArangoDB document ID")

    class Config:
        populate_by_name = True
        from_attributes = True


class CountryBase(BaseModel):
    """Base model for country."""

    name: str = Field(..., description="Country name", example="United States")
    iso_code: str = Field(..., description="ISO 3166-1 alpha-2 code", example="US")
    region: Optional[str] = Field(None, description="Geographic region", example="North America")
    nato_member: bool = Field(default=False, description="NATO membership status")


class CountryCreate(CountryBase):
    """Model for creating country."""
    pass


class Country(CountryBase):
    """Complete country model."""

    key: str = Field(..., alias="_key", description="ArangoDB document key")
    id: str = Field(..., alias="_id", description="ArangoDB document ID")

    class Config:
        populate_by_name = True
        from_attributes = True


class ManufacturerBase(BaseModel):
    """Base model for manufacturer."""

    name: str = Field(..., description="Manufacturer name", example="Anduril Industries")
    headquarters: Optional[str] = Field(None, description="Headquarters location", example="Costa Mesa, CA")
    country: Optional[str] = Field(None, description="Country", example="United States")
    type: Optional[str] = Field(
        None,
        description="Manufacturer type",
        example="Private defense technology company"
    )


class ManufacturerCreate(ManufacturerBase):
    """Model for creating manufacturer."""
    pass


class Manufacturer(ManufacturerBase):
    """Complete manufacturer model."""

    key: str = Field(..., alias="_key", description="ArangoDB document key")
    id: str = Field(..., alias="_id", description="ArangoDB document ID")

    class Config:
        populate_by_name = True
        from_attributes = True


class MissionBase(BaseModel):
    """Base model for mission type."""

    name: str = Field(..., description="Mission name", example="ISR")
    category: Optional[str] = Field(
        None,
        description="Mission category",
        example="Intelligence, Surveillance, Reconnaissance"
    )
    description: Optional[str] = Field(None, description="Mission description")


class MissionCreate(MissionBase):
    """Model for creating mission."""
    pass


class Mission(MissionBase):
    """Complete mission model."""

    key: str = Field(..., alias="_key", description="ArangoDB document key")
    id: str = Field(..., alias="_id", description="ArangoDB document ID")

    class Config:
        populate_by_name = True
        from_attributes = True


class SensorBase(BaseModel):
    """Base model for sensor."""

    name: str = Field(..., description="Sensor name", example="MTS-B")
    type: str = Field(..., description="Sensor type", example="EO/IR")
    manufacturer: Optional[str] = Field(None, description="Manufacturer")
    specifications: Optional[Dict[str, Any]] = Field(default_factory=dict)


class SensorCreate(SensorBase):
    """Model for creating sensor."""
    pass


class Sensor(SensorBase):
    """Complete sensor model."""

    key: str = Field(..., alias="_key", description="ArangoDB document key")
    id: str = Field(..., alias="_id", description="ArangoDB document ID")

    class Config:
        populate_by_name = True
        from_attributes = True


class WeaponBase(BaseModel):
    """Base model for weapon."""

    name: str = Field(..., description="Weapon name", example="AGM-114 Hellfire")
    type: str = Field(..., description="Weapon type", example="Air-to-ground missile")
    manufacturer: Optional[str] = Field(None, description="Manufacturer")
    specifications: Optional[Dict[str, Any]] = Field(default_factory=dict)


class WeaponCreate(WeaponBase):
    """Model for creating weapon."""
    pass


class Weapon(WeaponBase):
    """Complete weapon model."""

    key: str = Field(..., alias="_key", description="ArangoDB document key")
    id: str = Field(..., alias="_id", description="ArangoDB document ID")

    class Config:
        populate_by_name = True
        from_attributes = True


class SpecificationBase(BaseModel):
    """Base model for specification."""

    category: str = Field(..., description="Specification category", example="Performance")
    name: str = Field(..., description="Specification name", example="Max Speed")
    value: float = Field(..., description="Specification value", example=482.0)
    unit: str = Field(..., description="Unit of measurement", example="km/h")


class SpecificationCreate(SpecificationBase):
    """Model for creating specification."""
    pass


class Specification(SpecificationBase):
    """Complete specification model."""

    key: str = Field(..., alias="_key", description="ArangoDB document key")
    id: str = Field(..., alias="_id", description="ArangoDB document ID")

    class Config:
        populate_by_name = True
        from_attributes = True
