"""
Database connection and query utilities for X-UAV backend.

Provides DuckDB connection management and query methods.
"""

import json
from contextlib import contextmanager
from pathlib import Path
from typing import Any, Dict, Generator, List, Optional

import duckdb

from .config import settings


class Database:
    """
    Database connection manager for DuckDB.

    Handles connection pooling and query execution.
    """

    def __init__(self, db_path: Optional[Path] = None):
        """
        Initialize database manager.

        Args:
            db_path (Optional[Path]): Path to database file. Uses settings if not provided.
        """
        self.db_path = db_path or settings.database_path_absolute
        self._conn: Optional[duckdb.DuckDBPyConnection] = None

    @contextmanager
    def get_connection(self) -> Generator[duckdb.DuckDBPyConnection, None, None]:
        """
        Get database connection as context manager.

        Yields:
            duckdb.DuckDBPyConnection: Database connection

        Example:
            with db.get_connection() as conn:
                result = conn.execute("SELECT * FROM uavs").fetchall()
        """
        conn = duckdb.connect(str(self.db_path), read_only=True)
        try:
            yield conn
        finally:
            conn.close()

    def get_all_uavs(self) -> List[Dict[str, Any]]:
        """
        Retrieve all UAVs from database.

        Returns:
            List[Dict[str, Any]]: List of UAV records
        """
        with self.get_connection() as conn:
            result = conn.execute(
                "SELECT * FROM uavs ORDER BY designation"
            ).fetchall()

            # Get column names
            columns = [desc[0] for desc in conn.description]

            # Convert to list of dicts
            return [self._row_to_dict(row, columns) for row in result]

    def get_uav_by_designation(self, designation: str) -> Optional[Dict[str, Any]]:
        """
        Get specific UAV by designation.

        Args:
            designation (str): UAV designation (e.g., "MQ-9")

        Returns:
            Optional[Dict[str, Any]]: UAV record or None if not found
        """
        with self.get_connection() as conn:
            result = conn.execute(
                "SELECT * FROM uavs WHERE designation = ?",
                [designation]
            ).fetchone()

            if result is None:
                return None

            columns = [desc[0] for desc in conn.description]
            return self._row_to_dict(result, columns)

    def compare_uavs(self, designations: List[str]) -> List[Dict[str, Any]]:
        """
        Compare multiple UAVs.

        Args:
            designations (List[str]): List of UAV designations

        Returns:
            List[Dict[str, Any]]: Comparison data
        """
        if not designations:
            return []

        placeholders = ','.join(['?' for _ in designations])
        query = f"SELECT * FROM uavs WHERE designation IN ({placeholders}) ORDER BY designation"

        with self.get_connection() as conn:
            result = conn.execute(query, designations).fetchall()
            columns = [desc[0] for desc in conn.description]
            return [self._row_to_dict(row, columns) for row in result]

    def search_uavs(
        self,
        country: Optional[str] = None,
        uav_type: Optional[str] = None,
        status: Optional[str] = None,
        nato_class: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """
        Search UAVs with filters.

        Args:
            country (Optional[str]): Filter by country of origin
            uav_type (Optional[str]): Filter by UAV type
            status (Optional[str]): Filter by operational status
            nato_class (Optional[str]): Filter by NATO class

        Returns:
            List[Dict[str, Any]]: Matching UAVs
        """
        # Build dynamic query
        query = "SELECT * FROM uavs WHERE 1=1"
        params = []

        if country:
            query += " AND country_of_origin = ?"
            params.append(country)

        if uav_type:
            query += " AND type LIKE ?"
            params.append(f"%{uav_type}%")

        if status:
            query += " AND operational_status = ?"
            params.append(status)

        if nato_class:
            query += " AND nato_class = ?"
            params.append(nato_class)

        query += " ORDER BY designation"

        with self.get_connection() as conn:
            result = conn.execute(query, params).fetchall()
            columns = [desc[0] for desc in conn.description]
            return [self._row_to_dict(row, columns) for row in result]

    def get_countries(self) -> List[str]:
        """
        Get list of all countries in database.

        Returns:
            List[str]: List of country names
        """
        with self.get_connection() as conn:
            result = conn.execute(
                """
                SELECT DISTINCT country_of_origin
                FROM uavs
                WHERE country_of_origin IS NOT NULL
                ORDER BY country_of_origin
                """
            ).fetchall()
            return [row[0] for row in result]

    def get_types(self) -> List[str]:
        """
        Get list of all UAV types in database.

        Returns:
            List[str]: List of UAV types
        """
        with self.get_connection() as conn:
            result = conn.execute(
                """
                SELECT DISTINCT type
                FROM uavs
                WHERE type IS NOT NULL
                ORDER BY type
                """
            ).fetchall()
            return [row[0] for row in result]

    def get_stats(self) -> Dict[str, Any]:
        """
        Get database statistics.

        Returns:
            Dict[str, Any]: Statistics including counts by country, type, etc.
        """
        with self.get_connection() as conn:
            # Total count
            total = conn.execute("SELECT COUNT(*) FROM uavs").fetchone()[0]

            # By country
            by_country = conn.execute(
                """
                SELECT country_of_origin, COUNT(*) as count
                FROM uavs
                GROUP BY country_of_origin
                ORDER BY count DESC
                """
            ).fetchall()

            # By type
            by_type = conn.execute(
                """
                SELECT type, COUNT(*) as count
                FROM uavs
                WHERE type IS NOT NULL
                GROUP BY type
                ORDER BY count DESC
                """
            ).fetchall()

            # By status
            by_status = conn.execute(
                """
                SELECT operational_status, COUNT(*) as count
                FROM uavs
                WHERE operational_status IS NOT NULL
                GROUP BY operational_status
                ORDER BY count DESC
                """
            ).fetchall()

            return {
                "total": total,
                "by_country": [{"country": row[0], "count": row[1]} for row in by_country],
                "by_type": [{"type": row[0], "count": row[1]} for row in by_type],
                "by_status": [{"status": row[0], "count": row[1]} for row in by_status],
            }

    def _row_to_dict(self, row: tuple, columns: List[str]) -> Dict[str, Any]:
        """
        Convert database row to dictionary.

        Args:
            row (tuple): Database row
            columns (List[str]): Column names

        Returns:
            Dict[str, Any]: Row as dictionary with JSON fields parsed
        """
        result = {}
        for i, col in enumerate(columns):
            value = row[i]

            # Parse JSON fields
            if value is not None and col in [
                'mission_types', 'armament', 'sensor_suite', 'operators',
                'export_countries', 'notable_features', 'imagery_urls',
                'model_urls', 'variants'
            ]:
                try:
                    value = json.loads(value)
                except (json.JSONDecodeError, TypeError):
                    # Keep as string if parsing fails
                    pass

            result[col] = value

        return result


# Global database instance
db = Database()
