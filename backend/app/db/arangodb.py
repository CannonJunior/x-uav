"""
ArangoDB graph database connection and utilities.

Handles connections to ArangoDB for graph-based UAV data storage.
"""

from typing import Optional
from arango import ArangoClient
from arango.database import StandardDatabase
from arango.graph import Graph

from app.core.config import settings


class ArangoDBConnection:
    """
    ArangoDB connection manager.

    Manages connection lifecycle and provides access to database and graph objects.
    """

    def __init__(self):
        self.client: Optional[ArangoClient] = None
        self.db: Optional[StandardDatabase] = None
        self._graph: Optional[Graph] = None

    def connect(self) -> StandardDatabase:
        """
        Connect to ArangoDB and return database instance.

        Returns:
            StandardDatabase: ArangoDB database instance
        """
        self.client = ArangoClient(hosts=settings.graph_db_url)

        # Connect to system database first
        sys_db = self.client.db(
            '_system',
            username=settings.graph_db_username,
            password=settings.graph_db_password
        )

        # Create database if it doesn't exist
        if not sys_db.has_database(settings.graph_db_name):
            sys_db.create_database(settings.graph_db_name)

        # Connect to application database
        self.db = self.client.db(
            settings.graph_db_name,
            username=settings.graph_db_username,
            password=settings.graph_db_password
        )

        return self.db

    def get_database(self) -> StandardDatabase:
        """
        Get database instance, connecting if necessary.

        Returns:
            StandardDatabase: ArangoDB database instance
        """
        if self.db is None:
            self.connect()
        return self.db

    def get_graph(self, graph_name: str = "uav_graph") -> Graph:
        """
        Get or create UAV graph.

        Args:
            graph_name: Name of the graph (default: uav_graph)

        Returns:
            Graph: ArangoDB graph instance
        """
        db = self.get_database()

        if db.has_graph(graph_name):
            return db.graph(graph_name)

        # Create graph with initial structure
        return db.create_graph(graph_name)

    def disconnect(self):
        """Close ArangoDB connection."""
        if self.client:
            self.client.close()
        self.client = None
        self.db = None
        self._graph = None


# Global connection instance
arango_connection = ArangoDBConnection()


def get_arango_db() -> StandardDatabase:
    """
    Dependency injection for ArangoDB database.

    Returns:
        StandardDatabase: ArangoDB database instance
    """
    return arango_connection.get_database()


def get_uav_graph() -> Graph:
    """
    Dependency injection for UAV graph.

    Returns:
        Graph: UAV graph instance
    """
    return arango_connection.get_graph()
