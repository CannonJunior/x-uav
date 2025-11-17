#!/usr/bin/env python
"""
Database initialization script.

Initializes the ArangoDB schema and imports initial CCA platform data.
"""

import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.db.arangodb import arango_connection
from app.db.schema import init_schema
from app.services.import_service import import_cca_data


def main():
    """Main initialization function."""
    print("\n" + "="*60)
    print("X-UAV Database Initialization")
    print("="*60 + "\n")

    # Connect to database
    print("Connecting to ArangoDB...")
    db = arango_connection.connect()
    print(f"✓ Connected to database: {db.name}\n")

    # Initialize schema
    graph = init_schema(db)
    print(f"✓ Graph '{graph.name}' initialized\n")

    # Import CCA data
    stats = import_cca_data(db)

    print("\n" + "="*60)
    print("Database initialization complete!")
    print("="*60 + "\n")

    print("Next steps:")
    print("  1. Start the backend: uv run uvicorn app.main:app --reload")
    print("  2. Visit API docs: http://localhost:8000/docs")
    print("  3. Explore ArangoDB: http://localhost:8529\n")


if __name__ == "__main__":
    main()
