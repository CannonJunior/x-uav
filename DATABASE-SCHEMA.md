# Database Schema for X-UAV Application

## Database Technology: DuckDB

### Rationale
- **Zero-cost**: Free, open-source, embedded database
- **Local-first**: No cloud dependencies, runs entirely on localhost
- **High-performance**: Optimized for analytical queries (perfect for comparisons)
- **SQL Standard**: Full SQL support with advanced analytical functions
- **Easy Integration**: Python library available, simple deployment
- **Single File**: Entire database in one `.duckdb` file
- **No Server Required**: Embedded database, no separate server process

---

## Main Table: `uavs`

### Table Definition (SQL)

```sql
CREATE TABLE uavs (
    -- Primary Key
    id INTEGER PRIMARY KEY,

    -- Identification & Classification
    designation VARCHAR(20) NOT NULL UNIQUE,
    name VARCHAR(100),
    manufacturer VARCHAR(100),
    country_of_origin VARCHAR(50),
    nato_class VARCHAR(20),  -- Class I, II, III
    type VARCHAR(50),  -- MALE, HALE, UCAV, Tactical, Stealth, etc.
    operational_status VARCHAR(50),  -- Active, Retired, Development, Experimental
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
    airframe_type VARCHAR(50),  -- Fixed-wing, Rotary-wing, Flying wing, etc.

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
    mission_types JSON,  -- Array of mission types
    armament JSON,  -- Array of weapons
    max_weapons_load_kg DECIMAL(8,2),
    max_weapons_load_lbs DECIMAL(8,2),
    hardpoints INTEGER,
    internal_weapons_bays BOOLEAN,

    -- Sensors & Avionics
    sensor_suite JSON,  -- Array of sensors
    radar_type VARCHAR(100),
    communications VARCHAR(200),
    datalink_type VARCHAR(100),
    stealth_features TEXT,
    autonomy_level VARCHAR(50),

    -- Operational Details
    operators JSON,  -- Array of operating countries/organizations
    export_countries JSON,  -- Array of export destinations
    crew_size_remote INTEGER,
    ground_control_station VARCHAR(200),
    launch_method VARCHAR(100),
    recovery_method VARCHAR(100),

    -- Economic
    unit_cost_usd DECIMAL(12,2),
    program_cost_usd DECIMAL(15,2),
    fiscal_year INTEGER,

    -- Visual Assets
    imagery_urls JSON,  -- Object with different view URLs
    silhouette_url VARCHAR(500),
    model_urls JSON,  -- Object with low/high poly URLs
    scale_factor INTEGER DEFAULT 100,

    -- Additional Information
    notable_features JSON,  -- Array of distinctive features
    combat_history TEXT,
    variants JSON,  -- Array of variant information
    notes TEXT,

    -- Metadata
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

---

## Indexes for Performance

```sql
-- Index on designation for quick lookups
CREATE INDEX idx_uavs_designation ON uavs(designation);

-- Index on country for filtering by nation
CREATE INDEX idx_uavs_country ON uavs(country_of_origin);

-- Index on type for filtering by UAV type
CREATE INDEX idx_uavs_type ON uavs(type);

-- Index on operational status
CREATE INDEX idx_uavs_status ON uavs(operational_status);

-- Composite index for common queries
CREATE INDEX idx_uavs_country_type ON uavs(country_of_origin, type);
```

---

## Example Queries

### 1. Get all active UAVs
```sql
SELECT designation, name, manufacturer, country_of_origin, type
FROM uavs
WHERE operational_status = 'Active'
ORDER BY designation;
```

### 2. Compare UAVs by wingspan
```sql
SELECT
    designation,
    name,
    wingspan_meters,
    wingspan_feet,
    length_meters,
    length_feet
FROM uavs
ORDER BY wingspan_meters DESC;
```

### 3. Get all US military UAVs
```sql
SELECT *
FROM uavs
WHERE country_of_origin = 'United States'
  AND operational_status = 'Active'
ORDER BY initial_operating_capability DESC;
```

### 4. Performance comparison
```sql
SELECT
    designation,
    name,
    max_speed_kmh,
    service_ceiling_meters,
    endurance_hours,
    range_km
FROM uavs
ORDER BY endurance_hours DESC
LIMIT 10;
```

### 5. UAVs by cost
```sql
SELECT
    designation,
    name,
    manufacturer,
    unit_cost_usd,
    fiscal_year
FROM uavs
WHERE unit_cost_usd IS NOT NULL
ORDER BY unit_cost_usd DESC;
```

### 6. Combat UAVs (UCAVs)
```sql
SELECT
    designation,
    name,
    country_of_origin,
    armament,
    max_weapons_load_kg,
    hardpoints
FROM uavs
WHERE type LIKE '%UCAV%' OR type LIKE '%Combat%'
ORDER BY max_weapons_load_kg DESC;
```

---

## Sample Data Insert (MQ-9 Reaper)

```sql
INSERT INTO uavs (
    designation, name, manufacturer, country_of_origin, nato_class, type,
    operational_status, initial_operating_capability, total_units_produced,
    wingspan_meters, wingspan_feet, length_meters, length_feet,
    height_meters, height_feet, empty_weight_kg, empty_weight_lbs,
    max_takeoff_weight_kg, max_takeoff_weight_lbs,
    payload_capacity_kg, payload_capacity_lbs,
    fuel_capacity_kg, fuel_capacity_gallons,
    airframe_type, engine_type, engine_manufacturer, engine_model,
    thrust_hp, number_of_engines, propeller_configuration,
    cruise_speed_kmh, cruise_speed_mph, cruise_speed_knots,
    service_ceiling_meters, service_ceiling_feet,
    range_km, range_miles, range_nm,
    endurance_hours,
    primary_function, mission_types, armament,
    hardpoints, internal_weapons_bays,
    sensor_suite, communications, crew_size_remote,
    unit_cost_usd, fiscal_year,
    imagery_urls, silhouette_url, model_urls,
    notable_features, notes
) VALUES (
    'MQ-9', 'Reaper', 'General Atomics Aeronautical Systems, Inc.',
    'United States', 'Class III', 'MALE UCAV',
    'Active', '2007-10-01', 280,
    20.1, 66, 11, 36,
    3.8, 12.5, 2223, 4900,
    4760, 10500,
    1701, 3750,
    1814, 602,
    'Fixed-wing', 'Turboprop', 'Honeywell', 'TPE331-10GD',
    900, 1, 'Single pusher propeller',
    370, 230, 200,
    15240, 50000,
    1852, 1150, 1000,
    27,
    'Intelligence collection in support of strike, coordination and reconnaissance missions',
    '["ISR", "Strike", "Reconnaissance", "SEAD", "Close Air Support"]'::JSON,
    '["AGM-114 Hellfire missiles", "GBU-12 Paveway II", "GBU-38 JDAM"]'::JSON,
    6, false,
    '["EO/IR camera", "Synthetic Aperture Radar", "Laser designator"]'::JSON,
    'LOS and BLOS via satellite',
    2,
    56500000, 2011,
    '{"side": "/assets/images/uavs/mq-9/mq-9-side.png"}'::JSON,
    '/assets/silhouettes/mq-9-overhead.svg',
    '{"low_poly": "/assets/models/mq-9/mq-9-low.glb"}'::JSON,
    '["First UAV certified to file IFR flight plans", "Can carry both missiles and bombs", "27-hour endurance"]'::JSON,
    'The MQ-9 Reaper is a larger, more capable successor to the MQ-1 Predator. Projected end of service life: 2035.'
);
```

---

## Database File Location

```
/home/junior/src/x-uav/data/uavs.duckdb
```

---

## Python Integration Example

```python
import duckdb
from pathlib import Path

class UAVDatabase:
    """
    UAV Database interface using DuckDB.

    Provides methods for querying and managing UAV data.
    """

    def __init__(self, db_path: str = "data/uavs.duckdb"):
        """
        Initialize database connection.

        Args:
            db_path (str): Path to DuckDB database file
        """
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.conn = duckdb.connect(str(self.db_path))
        self._initialize_schema()

    def _initialize_schema(self):
        """Create tables and indexes if they don't exist."""
        # Execute schema creation SQL
        schema_sql = Path("schema.sql").read_text()
        self.conn.execute(schema_sql)

    def get_all_uavs(self):
        """
        Retrieve all UAVs.

        Returns:
            list: List of UAV records
        """
        return self.conn.execute("SELECT * FROM uavs ORDER BY designation").fetchall()

    def get_uav_by_designation(self, designation: str):
        """
        Get specific UAV by designation.

        Args:
            designation (str): UAV designation (e.g., "MQ-9")

        Returns:
            dict: UAV record
        """
        return self.conn.execute(
            "SELECT * FROM uavs WHERE designation = ?",
            [designation]
        ).fetchone()

    def compare_uavs(self, designations: list):
        """
        Compare multiple UAVs.

        Args:
            designations (list): List of UAV designations

        Returns:
            list: Comparison data
        """
        placeholders = ','.join(['?' for _ in designations])
        query = f"SELECT * FROM uavs WHERE designation IN ({placeholders})"
        return self.conn.execute(query, designations).fetchall()

    def search_uavs(self, filters: dict):
        """
        Search UAVs with filters.

        Args:
            filters (dict): Search filters

        Returns:
            list: Matching UAVs
        """
        # Build dynamic query based on filters
        # Implementation details...
        pass

    def close(self):
        """Close database connection."""
        self.conn.close()
```

---

## Migration Script

Location: `/backend/scripts/init_db.py`

```python
"""
Database initialization script for X-UAV application.

Creates DuckDB database with schema and loads initial UAV data.
"""

import duckdb
from pathlib import Path
import json

def init_database(db_path: str = "data/uavs.duckdb"):
    """
    Initialize the UAV database.

    Args:
        db_path (str): Path to database file
    """
    # Connect to DuckDB
    conn = duckdb.connect(db_path)

    # Read and execute schema
    schema_path = Path(__file__).parent.parent / "db" / "schema.sql"
    if schema_path.exists():
        schema_sql = schema_path.read_text()
        conn.execute(schema_sql)
        print("✓ Schema created")

    # Load initial data
    data_path = Path(__file__).parent.parent / "data" / "initial_uavs.json"
    if data_path.exists():
        with open(data_path) as f:
            uavs_data = json.load(f)

        # Insert each UAV
        for uav in uavs_data:
            # Insert logic here
            pass

        print(f"✓ Loaded {len(uavs_data)} UAVs")

    conn.close()
    print("✓ Database initialization complete")

if __name__ == "__main__":
    init_database()
```

---

## Advantages of DuckDB for This Application

1. **Zero Cost**: Free, open-source
2. **No Server**: Embedded database, runs in-process
3. **High Performance**: Optimized for analytical queries (aggregations, comparisons)
4. **SQL Support**: Full SQL standard compliance
5. **JSON Support**: Native JSON type for complex fields
6. **Easy Deployment**: Single file database
7. **Python Integration**: Excellent Python library
8. **ACID Compliance**: Full transactional support
9. **Analytical Functions**: Window functions, aggregations perfect for comparisons
10. **Local-First**: Aligns with project architecture (no cloud dependencies)

---

## Future Enhancements

### 1. Full-Text Search
```sql
-- Add full-text search capability for notes and descriptions
CREATE INDEX idx_uavs_fts ON uavs USING fts(notes, primary_function);
```

### 2. Comparison Views
```sql
-- Create materialized view for quick comparisons
CREATE VIEW uav_comparison AS
SELECT
    designation,
    name,
    type,
    wingspan_meters,
    endurance_hours,
    range_km,
    max_speed_kmh,
    service_ceiling_meters,
    unit_cost_usd
FROM uavs
WHERE operational_status = 'Active';
```

### 3. Performance Metrics
```sql
-- Add calculated performance score
ALTER TABLE uavs ADD COLUMN performance_score DECIMAL(5,2)
    GENERATED ALWAYS AS (
        (endurance_hours * 0.3) +
        (range_km / 1000 * 0.3) +
        (service_ceiling_meters / 10000 * 0.2) +
        (max_speed_kmh / 1000 * 0.2)
    );
```

---

## Backup Strategy

```bash
# Simple backup - just copy the .duckdb file
cp data/uavs.duckdb data/backups/uavs_$(date +%Y%m%d_%H%M%S).duckdb

# Export to JSON
duckdb data/uavs.duckdb "COPY uavs TO 'data/export/uavs.json' (FORMAT JSON)"

# Export to CSV
duckdb data/uavs.duckdb "COPY uavs TO 'data/export/uavs.csv' (HEADER, DELIMITER ',')"
```
