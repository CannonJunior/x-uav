# UAV Data Model Specification

## Overview
This document defines the comprehensive data model for the X-UAV comparison web application. The model is designed to accommodate military and government UAVs from various nations with diverse specifications and capabilities.

## Core Data Fields

### Identification & Classification
- **designation**: Official model designation (e.g., "MQ-9", "RQ-4", "TB2")
- **name**: Common name or nickname (e.g., "Reaper", "Global Hawk", "Bayraktar")
- **manufacturer**: Primary contractor/manufacturer
- **country_of_origin**: Nation of origin
- **nato_class**: NATO classification (Class I, II, III)
- **type**: UAV type (MALE, HALE, UCAV, Tactical, Stealth, etc.)
- **operational_status**: Current status (Active, Retired, Development, Experimental)
- **initial_operating_capability**: Date of IOC
- **total_units_produced**: Number of units manufactured

### Physical Characteristics
- **wingspan_meters**: Wingspan in meters
- **wingspan_feet**: Wingspan in feet
- **length_meters**: Overall length in meters
- **length_feet**: Overall length in feet
- **height_meters**: Height in meters
- **height_feet**: Height in feet
- **empty_weight_kg**: Empty weight in kilograms
- **empty_weight_lbs**: Empty weight in pounds
- **max_takeoff_weight_kg**: Maximum takeoff weight in kilograms
- **max_takeoff_weight_lbs**: Maximum takeoff weight in pounds
- **payload_capacity_kg**: Payload capacity in kilograms
- **payload_capacity_lbs**: Payload capacity in pounds
- **fuel_capacity_kg**: Fuel capacity in kilograms
- **fuel_capacity_gallons**: Fuel capacity in gallons
- **airframe_type**: Design type (Fixed-wing, Rotary-wing, Flying wing, Blended body)

### Propulsion
- **engine_type**: Type of engine (Turboprop, Turbofan, Piston, Rocket, etc.)
- **engine_manufacturer**: Engine manufacturer
- **engine_model**: Specific engine model
- **thrust_hp**: Thrust/power in horsepower
- **thrust_lbs**: Thrust in pounds
- **number_of_engines**: Number of engines
- **propeller_configuration**: Propeller type and configuration

### Performance
- **cruise_speed_kmh**: Cruise speed in km/h
- **cruise_speed_mph**: Cruise speed in mph
- **cruise_speed_knots**: Cruise speed in knots
- **max_speed_kmh**: Maximum speed in km/h
- **max_speed_mph**: Maximum speed in mph
- **max_speed_mach**: Maximum speed in Mach (if applicable)
- **service_ceiling_meters**: Service ceiling in meters
- **service_ceiling_feet**: Service ceiling in feet
- **range_km**: Operational range in kilometers
- **range_miles**: Operational range in miles
- **range_nm**: Operational range in nautical miles
- **endurance_hours**: Maximum endurance in hours
- **combat_radius_km**: Combat radius in kilometers
- **combat_radius_nm**: Combat radius in nautical miles

### Mission Capabilities
- **primary_function**: Primary mission role
- **mission_types**: List of mission types (ISR, Strike, SEAD, Reconnaissance, etc.)
- **armament**: List of compatible weapons systems
- **max_weapons_load_kg**: Maximum weapons load in kilograms
- **max_weapons_load_lbs**: Maximum weapons load in pounds
- **hardpoints**: Number of weapons hardpoints
- **internal_weapons_bays**: Boolean for internal weapons storage

### Sensors & Avionics
- **sensor_suite**: List of sensors (EO/IR, SAR, GMTI, etc.)
- **radar_type**: Radar system type
- **communications**: Communication systems (LOS, BLOS, Satellite)
- **datalink_type**: Datalink standard (NATO STANAG, proprietary, etc.)
- **stealth_features**: Stealth/low-observable features
- **autonomy_level**: Level of autonomous operation

### Operational Details
- **operators**: List of countries/organizations operating the UAV
- **export_countries**: Countries to which the system has been exported
- **crew_size_remote**: Number of remote operators required
- **ground_control_station**: GCS type/description
- **launch_method**: Launch method (Catapult, Runway, Air-launched, etc.)
- **recovery_method**: Recovery method (Arrested landing, Runway, Parachute, etc.)

### Economic
- **unit_cost_usd**: Unit cost in USD (with fiscal year)
- **program_cost_usd**: Total program cost
- **fiscal_year**: Fiscal year for cost data

### Visual Assets (for future implementation)
- **imagery_url**: Path to accurate imagery
- **silhouette_url**: Path to overhead silhouette (scaled)
- **model_3d_url**: Path to 3D model file
- **scale_factor**: Relative scale factor for visualization

### Additional Information
- **notable_features**: List of distinctive features or capabilities
- **combat_history**: Notable operational deployments
- **variants**: List of variants and their differences
- **notes**: Additional notes and information

## Data Types & Validation

### Numeric Fields
- All weight, dimension, and performance metrics should support decimal values
- Optional fields for imperial and metric units
- Validation ranges based on realistic UAV parameters

### Text Fields
- Designation: Max 20 characters
- Name: Max 100 characters
- Manufacturer: Max 100 characters
- Primary function: Max 500 characters

### List Fields
- Mission types, armament, sensors: JSON arrays
- Operators, export countries: JSON arrays

### Date Fields
- ISO 8601 format (YYYY-MM-DD)

## UAVs Identified for Initial Database

### United States
1. **MQ-9 Reaper** - MALE UCAV
2. **RQ-4 Global Hawk** - HALE ISR
3. **MQ-1 Predator** - MALE ISR/Strike
4. **RQ-170 Sentinel** - Stealth ISR
5. **X-47B** - Stealth UCAV Demonstrator

### Turkey
6. **Bayraktar TB2** - MALE UCAV

### China
7. **Wing Loong II** - MALE UCAV
8. **CH-4 Rainbow** - MALE UCAV
9. **GJ-11 Sharp Sword** - Stealth UCAV
10. **WZ-8** - Supersonic Reconnaissance

### United Kingdom
11. **Watchkeeper WK450** - Tactical ISR

### Israel
12. **Hermes 450** - MALE ISR
13. **Heron TP** - MALE ISR

### Russia
14. **Orion/Sirius** - MALE UCAV
15. **Korsar** - Tactical ISR
16. **Forpost-R** - MALE ISR

## Future Expansion
- Additional UAVs from other nations
- Historical/retired UAVs for comparison
- Experimental/prototype systems
- Commercial UAVs adapted for government use
