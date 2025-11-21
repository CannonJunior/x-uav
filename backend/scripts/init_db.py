#!/usr/bin/env python3
"""
Database initialization script for X-UAV application.

Creates DuckDB database with schema and loads initial UAV data.
"""

import json
import sys
from pathlib import Path
from typing import Dict, List, Any

import duckdb


def get_project_root() -> Path:
    """
    Get the project root directory.

    Returns:
        Path: Project root directory
    """
    # Script is in backend/scripts, so go up 2 levels
    return Path(__file__).parent.parent.parent


def load_schema(schema_path: Path) -> str:
    """
    Load SQL schema from file.

    Args:
        schema_path (Path): Path to schema.sql file

    Returns:
        str: SQL schema content

    Raises:
        FileNotFoundError: If schema file doesn't exist
    """
    if not schema_path.exists():
        raise FileNotFoundError(f"Schema file not found: {schema_path}")

    with open(schema_path, 'r', encoding='utf-8') as f:
        return f.read()


def load_initial_data(data_path: Path) -> List[Dict[str, Any]]:
    """
    Load initial UAV data from JSON file.

    Args:
        data_path (Path): Path to initial_uavs.json file

    Returns:
        List[Dict[str, Any]]: List of UAV records

    Raises:
        FileNotFoundError: If data file doesn't exist
        json.JSONDecodeError: If JSON is invalid
    """
    if not data_path.exists():
        raise FileNotFoundError(f"Data file not found: {data_path}")

    with open(data_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def convert_json_fields(record: Dict[str, Any], json_fields: List[str]) -> Dict[str, Any]:
    """
    Convert JSON array/object fields to JSON strings for DuckDB.

    Args:
        record (Dict[str, Any]): Record to convert
        json_fields (List[str]): List of field names that contain JSON

    Returns:
        Dict[str, Any]: Record with JSON fields converted
    """
    converted = record.copy()
    for field in json_fields:
        if field in converted and converted[field] is not None:
            if isinstance(converted[field], (list, dict)):
                converted[field] = json.dumps(converted[field])

    return converted


UAV_JSON_FIELDS = [
    'mission_types', 'armament', 'sensor_suite', 'operators',
    'export_countries', 'notable_features', 'imagery_urls',
    'model_urls', 'variants'
]

ARMAMENT_JSON_FIELDS = [
    'launch_platform_types', 'variants', 'notable_features'
]


def insert_record(
    conn: duckdb.DuckDBPyConnection,
    table_name: str,
    record: Dict[str, Any],
    json_fields: List[str],
    id_field: str = 'designation'
) -> None:
    """
    Insert a single record into a database table.

    Args:
        conn (duckdb.DuckDBPyConnection): Database connection
        table_name (str): Name of the table
        record (Dict[str, Any]): Record to insert
        json_fields (List[str]): Fields containing JSON data
        id_field (str): Field name to use for error messages
    """
    # Get valid column names from the table schema
    schema_result = conn.execute(f"PRAGMA table_info('{table_name}')").fetchall()
    valid_columns = {row[1] for row in schema_result}

    # Convert JSON fields
    record_data = convert_json_fields(record, json_fields)

    # Filter to only include valid columns
    filtered_data = {k: v for k, v in record_data.items() if k in valid_columns}

    # Build column names and placeholders
    columns = list(filtered_data.keys())
    placeholders = ['?' for _ in columns]
    values = [filtered_data[col] for col in columns]

    # Construct INSERT statement
    insert_sql = f"""
        INSERT INTO {table_name} ({', '.join(columns)})
        VALUES ({', '.join(placeholders)})
    """

    try:
        conn.execute(insert_sql, values)
    except Exception as e:
        print(f"Error inserting into {table_name} ({record.get(id_field, 'UNKNOWN')}): {e}")
        raise


def insert_uav(conn: duckdb.DuckDBPyConnection, uav: Dict[str, Any]) -> None:
    """
    Insert a single UAV record into the database.

    Args:
        conn (duckdb.DuckDBPyConnection): Database connection
        uav (Dict[str, Any]): UAV record to insert
    """
    insert_record(conn, 'uavs', uav, UAV_JSON_FIELDS, 'designation')


def insert_armament(conn: duckdb.DuckDBPyConnection, armament: Dict[str, Any]) -> None:
    """
    Insert a single armament record into the database.

    Args:
        conn (duckdb.DuckDBPyConnection): Database connection
        armament (Dict[str, Any]): Armament record to insert
    """
    insert_record(conn, 'armaments', armament, ARMAMENT_JSON_FIELDS, 'designation')


def insert_uav_armament(conn: duckdb.DuckDBPyConnection, ua: Dict[str, Any]) -> None:
    """
    Insert a single UAV-armament relationship record.

    Args:
        conn (duckdb.DuckDBPyConnection): Database connection
        ua (Dict[str, Any]): UAV-armament relationship record
    """
    insert_record(conn, 'uav_armaments', ua, [], 'uav_designation')


def init_database(
    db_path: Path,
    schema_path: Path,
    uavs_path: Path,
    armaments_path: Path,
    uav_armaments_path: Path
) -> None:
    """
    Initialize the UAV database with all data.

    Args:
        db_path (Path): Path to database file
        schema_path (Path): Path to schema.sql file
        uavs_path (Path): Path to initial_uavs.json file
        armaments_path (Path): Path to armaments.json file
        uav_armaments_path (Path): Path to uav_armaments.json file

    Raises:
        Exception: If database initialization fails
    """
    print("🚀 Initializing X-UAV database...")

    # Ensure database directory exists
    db_path.parent.mkdir(parents=True, exist_ok=True)

    # Connect to DuckDB
    print(f"📂 Connecting to database: {db_path}")
    conn = duckdb.connect(str(db_path))

    try:
        # Load and execute schema
        print("📋 Loading schema...")
        schema_sql = load_schema(schema_path)
        conn.execute(schema_sql)
        print("✅ Schema created successfully")

        # Load and insert UAVs
        print("\n📦 Loading UAV data...")
        uavs_data = load_initial_data(uavs_path)
        print(f"   Found {len(uavs_data)} UAVs to load")
        print("💾 Inserting UAV records...")
        for i, uav in enumerate(uavs_data, 1):
            designation = uav.get('designation', 'UNKNOWN')
            print(f"   [{i}/{len(uavs_data)}] {designation}")
            insert_uav(conn, uav)
        result = conn.execute("SELECT COUNT(*) FROM uavs").fetchone()
        print(f"✅ Loaded {result[0] if result else 0} UAVs")

        # Load and insert armaments
        print("\n🔫 Loading armament data...")
        armaments_data = load_initial_data(armaments_path)
        print(f"   Found {len(armaments_data)} armaments to load")
        print("💾 Inserting armament records...")
        for i, armament in enumerate(armaments_data, 1):
            designation = armament.get('designation', 'UNKNOWN')
            print(f"   [{i}/{len(armaments_data)}] {designation}")
            insert_armament(conn, armament)
        result = conn.execute("SELECT COUNT(*) FROM armaments").fetchone()
        print(f"✅ Loaded {result[0] if result else 0} armaments")

        # Load and insert UAV-armament relationships
        print("\n🔗 Loading UAV-armament relationships...")
        ua_data = load_initial_data(uav_armaments_path)
        print(f"   Found {len(ua_data)} relationships to load")
        print("💾 Inserting relationship records...")
        for ua in ua_data:
            insert_uav_armament(conn, ua)
        result = conn.execute("SELECT COUNT(*) FROM uav_armaments").fetchone()
        print(f"✅ Loaded {result[0] if result else 0} UAV-armament relationships")

        # Show UAV summary by country
        print("\n📊 UAV Summary by Country:")
        summary = conn.execute("""
            SELECT country_of_origin, COUNT(*) as count
            FROM uavs
            GROUP BY country_of_origin
            ORDER BY count DESC
        """).fetchall()
        for country, count in summary:
            print(f"   {country}: {count}")

        # Show UAV summary by type
        print("\n📊 UAV Summary by Type:")
        type_summary = conn.execute("""
            SELECT type, COUNT(*) as count
            FROM uavs
            WHERE type IS NOT NULL
            GROUP BY type
            ORDER BY count DESC
        """).fetchall()
        for uav_type, count in type_summary:
            print(f"   {uav_type}: {count}")

        # Show armament summary by type
        print("\n📊 Armament Summary by Type:")
        armament_summary = conn.execute("""
            SELECT weapon_type, COUNT(*) as count
            FROM armaments
            GROUP BY weapon_type
            ORDER BY count DESC
        """).fetchall()
        for weapon_type, count in armament_summary:
            print(f"   {weapon_type}: {count}")

    except Exception as e:
        print(f"❌ Error during database initialization: {e}")
        raise
    finally:
        conn.close()

    print("\n✅ Database initialization complete!")
    print(f"📍 Database location: {db_path}")


def main() -> int:
    """
    Main entry point for database initialization.

    Returns:
        int: Exit code (0 for success, 1 for failure)
    """
    try:
        # Get project paths
        project_root = get_project_root()
        db_path = project_root / "backend" / "data_db" / "uavs.duckdb"
        schema_path = project_root / "backend" / "db" / "schema.sql"
        uavs_path = project_root / "backend" / "data" / "initial_uavs.json"
        armaments_path = project_root / "backend" / "data" / "armaments.json"
        uav_armaments_path = project_root / "backend" / "data" / "uav_armaments.json"

        # Initialize database
        init_database(db_path, schema_path, uavs_path, armaments_path, uav_armaments_path)

        return 0

    except FileNotFoundError as e:
        print(f"❌ File not found: {e}")
        return 1
    except json.JSONDecodeError as e:
        print(f"❌ Invalid JSON in data file: {e}")
        return 1
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
