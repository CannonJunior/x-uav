-- X-UAV Database Schema for DuckDB
-- UAV Comparison Application
-- Created: 2025-11-18
-- Updated: 2025-11-20 - Added armaments database and UAV variants

-- Drop existing tables if they exist
DROP TABLE IF EXISTS uav_armaments;
DROP TABLE IF EXISTS armaments;
DROP TABLE IF EXISTS uavs;

-- Main UAV table
CREATE TABLE uavs (
    -- Primary Key
    id INTEGER PRIMARY KEY,

    -- Identification & Classification
    designation VARCHAR(20) NOT NULL UNIQUE,
    name VARCHAR(100),
    manufacturer VARCHAR(100),
    country_of_origin VARCHAR(50),
    nato_class VARCHAR(20),
    type VARCHAR(50),
    operational_status VARCHAR(50) DEFAULT 'Active',
    initial_operating_capability DATE,
    total_units_produced INTEGER,

    -- Physical Characteristics
    wingspan_meters DECIMAL(6,2),
    wingspan_feet DECIMAL(6,2),
    length_meters DECIMAL(6,2),
    length_feet DECIMAL(6,2),
    height_meters DECIMAL(6,2),
    height_feet DECIMAL(6,2),
    empty_weight_kg DECIMAL(8,2),
    empty_weight_lbs DECIMAL(8,2),
    max_takeoff_weight_kg DECIMAL(8,2),
    max_takeoff_weight_lbs DECIMAL(8,2),
    payload_capacity_kg DECIMAL(8,2),
    payload_capacity_lbs DECIMAL(8,2),
    fuel_capacity_kg DECIMAL(8,2),
    fuel_capacity_gallons DECIMAL(8,2),
    airframe_type VARCHAR(50),

    -- Propulsion
    engine_type VARCHAR(50),
    engine_manufacturer VARCHAR(100),
    engine_model VARCHAR(100),
    thrust_hp INTEGER,
    thrust_lbs INTEGER,
    number_of_engines INTEGER,
    propeller_configuration VARCHAR(100),

    -- Performance
    cruise_speed_kmh DECIMAL(8,2),
    cruise_speed_mph DECIMAL(8,2),
    cruise_speed_knots DECIMAL(8,2),
    max_speed_kmh DECIMAL(8,2),
    max_speed_mph DECIMAL(8,2),
    max_speed_mach DECIMAL(4,2),
    service_ceiling_meters DECIMAL(8,2),
    service_ceiling_feet DECIMAL(8,2),
    range_km DECIMAL(8,2),
    range_miles DECIMAL(8,2),
    range_nm DECIMAL(8,2),
    endurance_hours DECIMAL(5,2),
    combat_radius_km DECIMAL(8,2),
    combat_radius_nm DECIMAL(8,2),

    -- Mission Capabilities
    primary_function TEXT,
    mission_types JSON,
    armament JSON,
    max_weapons_load_kg DECIMAL(8,2),
    max_weapons_load_lbs DECIMAL(8,2),
    hardpoints INTEGER,
    internal_weapons_bays BOOLEAN DEFAULT false,

    -- Sensors & Avionics
    sensor_suite JSON,
    radar_type VARCHAR(100),
    communications VARCHAR(200),
    datalink_type VARCHAR(100),
    stealth_features TEXT,
    autonomy_level VARCHAR(50),

    -- Operational Details
    operators JSON,
    export_countries JSON,
    crew_size_remote INTEGER,
    ground_control_station VARCHAR(200),
    launch_method VARCHAR(100),
    recovery_method VARCHAR(100),

    -- Economic
    unit_cost_usd DECIMAL(12,2),
    program_cost_usd DECIMAL(15,2),
    fiscal_year INTEGER,

    -- Visual Assets
    imagery_urls JSON,
    silhouette_url VARCHAR(500),
    model_urls JSON,
    scale_factor INTEGER DEFAULT 100,

    -- Additional Information
    notable_features JSON,
    combat_history TEXT,
    variants JSON,
    notes TEXT,

    -- Metadata
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indexes for performance
CREATE INDEX idx_uavs_designation ON uavs(designation);
CREATE INDEX idx_uavs_country ON uavs(country_of_origin);
CREATE INDEX idx_uavs_type ON uavs(type);
CREATE INDEX idx_uavs_status ON uavs(operational_status);
CREATE INDEX idx_uavs_country_type ON uavs(country_of_origin, type);

-- Create comparison view for quick access
CREATE OR REPLACE VIEW uav_comparison AS
SELECT
    designation,
    name,
    manufacturer,
    country_of_origin,
    type,
    wingspan_meters,
    length_meters,
    endurance_hours,
    range_km,
    max_speed_kmh,
    service_ceiling_meters,
    unit_cost_usd,
    operational_status
FROM uavs
WHERE operational_status = 'Active'
ORDER BY designation;

-- Create performance ranking view
CREATE OR REPLACE VIEW uav_performance AS
SELECT
    designation,
    name,
    endurance_hours,
    range_km,
    service_ceiling_meters,
    max_speed_kmh,
    -- Calculated performance score
    (COALESCE(endurance_hours, 0) * 0.3 +
     COALESCE(range_km, 0) / 1000 * 0.3 +
     COALESCE(service_ceiling_meters, 0) / 10000 * 0.2 +
     COALESCE(max_speed_kmh, 0) / 1000 * 0.2) AS performance_score
FROM uavs
WHERE operational_status = 'Active'
ORDER BY performance_score DESC;

-- =====================================================
-- ARMAMENTS DATABASE
-- =====================================================

-- Armaments table - stores all weapon systems
CREATE TABLE armaments (
    id INTEGER PRIMARY KEY,

    -- Identification
    designation VARCHAR(50) NOT NULL UNIQUE,
    name VARCHAR(100),
    manufacturer VARCHAR(100),
    country_of_origin VARCHAR(50),

    -- Classification
    weapon_type VARCHAR(50) NOT NULL,  -- 'Missile', 'Bomb', 'Rocket', 'Gun Pod'
    weapon_class VARCHAR(50),          -- 'Air-to-Ground', 'Air-to-Air', 'Anti-Tank', 'Precision Guided'
    guidance_type VARCHAR(100),        -- 'Laser', 'GPS/INS', 'Semi-Active Laser', 'IR', 'MMW Radar', etc.

    -- Physical Characteristics
    length_meters DECIMAL(6,3),
    length_inches DECIMAL(6,2),
    diameter_mm DECIMAL(6,2),
    diameter_inches DECIMAL(6,2),
    wingspan_meters DECIMAL(5,3),
    wingspan_inches DECIMAL(6,2),
    weight_kg DECIMAL(8,2),
    weight_lbs DECIMAL(8,2),

    -- Warhead
    warhead_type VARCHAR(100),         -- 'HEAT', 'HE-Frag', 'Tandem HEAT', 'Kinetic', 'Blast-Frag'
    warhead_weight_kg DECIMAL(6,2),
    warhead_weight_lbs DECIMAL(6,2),

    -- Performance
    range_km DECIMAL(8,2),
    range_miles DECIMAL(8,2),
    range_nm DECIMAL(8,2),
    max_speed_mach DECIMAL(4,2),
    max_speed_kmh DECIMAL(8,2),
    min_altitude_meters INTEGER,
    max_altitude_meters INTEGER,
    cep_meters DECIMAL(5,2),           -- Circular Error Probable (accuracy)

    -- Propulsion
    propulsion_type VARCHAR(50),       -- 'Solid Rocket', 'Turbojet', 'Unpowered/Glide', 'Ramjet'
    engine_model VARCHAR(100),

    -- Launch Parameters
    launch_platform_types JSON,        -- ['Fixed-Wing', 'Rotary-Wing', 'Ground', 'Naval']
    min_launch_altitude_ft INTEGER,
    max_launch_altitude_ft INTEGER,
    launch_weight_kg DECIMAL(8,2),

    -- Economics
    unit_cost_usd DECIMAL(12,2),
    year_introduced INTEGER,

    -- Status
    operational_status VARCHAR(50) DEFAULT 'Active',

    -- Additional Info
    variants JSON,
    notable_features JSON,
    combat_history TEXT,
    notes TEXT,

    -- Metadata
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- UAV-Armament relationship table (many-to-many)
CREATE TABLE uav_armaments (
    id INTEGER PRIMARY KEY,
    uav_designation VARCHAR(20) NOT NULL,
    armament_designation VARCHAR(50) NOT NULL,
    max_quantity INTEGER,              -- Max number of this weapon UAV can carry
    hardpoint_positions VARCHAR(100),  -- 'Wing pylons', 'Internal bay', 'Centerline', etc.
    integration_status VARCHAR(50),    -- 'Operational', 'Tested', 'Planned', 'Experimental'
    integration_date DATE,
    notes TEXT,
    UNIQUE(uav_designation, armament_designation)
);

-- Indexes for armaments
CREATE INDEX idx_armaments_designation ON armaments(designation);
CREATE INDEX idx_armaments_type ON armaments(weapon_type);
CREATE INDEX idx_armaments_class ON armaments(weapon_class);
CREATE INDEX idx_armaments_country ON armaments(country_of_origin);

-- Indexes for UAV-armament relationship
CREATE INDEX idx_uav_armaments_uav ON uav_armaments(uav_designation);
CREATE INDEX idx_uav_armaments_armament ON uav_armaments(armament_designation);

-- Create armament summary view
CREATE OR REPLACE VIEW armament_summary AS
SELECT
    designation,
    name,
    weapon_type,
    weapon_class,
    guidance_type,
    weight_kg,
    range_km,
    unit_cost_usd,
    operational_status
FROM armaments
ORDER BY weapon_type, designation;

-- Create UAV weapons capability view
CREATE OR REPLACE VIEW uav_weapons_capability AS
SELECT
    u.designation AS uav_designation,
    u.name AS uav_name,
    u.type AS uav_type,
    a.designation AS weapon_designation,
    a.name AS weapon_name,
    a.weapon_type,
    a.weapon_class,
    ua.max_quantity,
    ua.integration_status
FROM uavs u
JOIN uav_armaments ua ON u.designation = ua.uav_designation
JOIN armaments a ON ua.armament_designation = a.designation
ORDER BY u.designation, a.weapon_type;
