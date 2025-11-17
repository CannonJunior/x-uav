"""
Data import service.

Handles importing UAV data from JSON files into ArangoDB.
"""

import json
from pathlib import Path
from typing import Dict, Any, List
from arango.database import StandardDatabase
from arango.exceptions import DocumentInsertError


class ImportService:
    """Service for importing UAV data into the database."""

    def __init__(self, db: StandardDatabase):
        """
        Initialize import service.

        Args:
            db: ArangoDB database instance
        """
        self.db = db

    def import_json_file(self, file_path: Path) -> Dict[str, int]:
        """
        Import data from JSON file.

        Args:
            file_path: Path to JSON file

        Returns:
            Dictionary with import statistics
        """
        print(f"\nImporting data from: {file_path}")

        with open(file_path, 'r') as f:
            data = json.load(f)

        stats = {
            "countries": 0,
            "manufacturers": 0,
            "programs": 0,
            "missions": 0,
            "platform_families": 0,
            "platform_variants": 0,
            "mission_configurations": 0,
            "technologies": 0,
            "errors": 0
        }

        # Import vertex collections
        for collection_name, items in data.items():
            if not isinstance(items, list):
                continue

            collection = self.db.collection(collection_name)
            print(f"\nImporting {len(items)} items into {collection_name}...")

            for item in items:
                try:
                    collection.insert(item, silent=True, overwrite=True)
                    stats[collection_name] += 1
                    print(f"  ✓ Imported: {item.get('name', item.get('_key'))}")
                except DocumentInsertError as e:
                    print(f"  ✗ Error importing {item.get('_key')}: {e}")
                    stats["errors"] += 1

        return stats

    def create_relationships(self) -> Dict[str, int]:
        """
        Create relationships (edges) between entities.

        Returns:
            Dictionary with relationship statistics
        """
        print("\nCreating relationships...")

        stats = {
            "belongs_to_family": 0,
            "has_variant": 0,
            "has_configuration": 0,
            "configured_from": 0,
            "configured_for": 0,
            "manufactured_by": 0,
            "developed_under": 0,
            "provides_autonomy": 0,
            "implements_tech": 0,
            "errors": 0
        }

        # Platform families -> manufacturers
        self._create_edge(
            "manufactured_by",
            [
                ("fury", "anduril"),
                ("gambit", "general-atomics"),
                ("ghost-bat", "boeing"),
                ("x-bat", "shield-ai"),
                ("ca-1-europa", "helsing")
            ],
            "platform_families",
            "manufacturers",
            stats
        )

        # Platform families -> programs
        self._create_edge(
            "developed_under",
            [
                ("fury", "cca-increment-1"),
                ("gambit", "cca-increment-1")
            ],
            "platform_families",
            "programs",
            stats
        )

        # Variants -> families
        self._create_edge(
            "belongs_to_family",
            [
                ("yfq-44a", "fury"),
                ("gambit-1", "gambit"),
                ("gambit-4", "gambit"),
                ("gambit-6", "gambit"),
                ("mq-28a", "ghost-bat"),
                ("x-bat-1", "x-bat"),
                ("ca-1", "ca-1-europa")
            ],
            "platform_variants",
            "platform_families",
            stats
        )

        # Configurations -> variants
        self._create_edge(
            "configured_from",
            [
                ("fury-isr", "yfq-44a"),
                ("fury-strike", "yfq-44a"),
                ("fury-ew", "yfq-44a"),
                ("fury-decoy", "yfq-44a"),
                ("gambit-1-aa", "gambit-1"),
                ("gambit-4-isr", "gambit-4"),
                ("gambit-6-strike", "gambit-6"),
                ("gambit-6-ew", "gambit-6"),
                ("ghost-bat-isr", "mq-28a"),
                ("ghost-bat-ew", "mq-28a"),
                ("x-bat-isr", "x-bat-1"),
                ("x-bat-strike", "x-bat-1")
            ],
            "mission_configurations",
            "platform_variants",
            stats
        )

        # Configurations -> missions
        self._create_edge(
            "configured_for",
            [
                ("fury-isr", "isr"),
                ("fury-strike", "strike"),
                ("fury-ew", "electronic-warfare"),
                ("fury-decoy", "decoy"),
                ("gambit-1-aa", "air-to-air"),
                ("gambit-4-isr", "isr"),
                ("gambit-6-strike", "strike"),
                ("gambit-6-ew", "electronic-warfare"),
                ("ghost-bat-isr", "isr"),
                ("ghost-bat-ew", "electronic-warfare"),
                ("x-bat-isr", "isr"),
                ("x-bat-strike", "strike")
            ],
            "mission_configurations",
            "missions",
            stats
        )

        # Autonomy providers
        self._create_edge(
            "provides_autonomy",
            [
                ("shield-ai", "yfq-44a"),
                ("rtx", "gambit-1")
            ],
            "manufacturers",
            "platform_variants",
            stats
        )

        # Technologies
        self._create_edge(
            "implements_tech",
            [
                ("yfq-44a", "lattice-os"),
                ("yfq-44a", "hivemind-ai"),
                ("yfq-44a", "mosa"),
                ("x-bat-1", "hivemind-ai"),
                ("ca-1", "centaur-ai")
            ],
            "platform_variants",
            "technologies",
            stats
        )

        return stats

    def _create_edge(
        self,
        edge_collection: str,
        relationships: List[tuple],
        from_collection: str,
        to_collection: str,
        stats: Dict[str, int]
    ) -> None:
        """
        Create edges between documents.

        Args:
            edge_collection: Name of edge collection
            relationships: List of (from_key, to_key) tuples
            from_collection: Source collection name
            to_collection: Target collection name
            stats: Statistics dictionary to update
        """
        collection = self.db.collection(edge_collection)

        for from_key, to_key in relationships:
            try:
                edge = {
                    "_from": f"{from_collection}/{from_key}",
                    "_to": f"{to_collection}/{to_key}"
                }
                collection.insert(edge, silent=True)
                stats[edge_collection] += 1
                print(f"  ✓ Created edge: {from_key} -> {to_key}")
            except DocumentInsertError as e:
                print(f"  ✗ Error creating edge {from_key} -> {to_key}: {e}")
                stats["errors"] += 1


def import_cca_data(db: StandardDatabase) -> Dict[str, Any]:
    """
    Import CCA platform data.

    Args:
        db: ArangoDB database instance

    Returns:
        Import statistics
    """
    import_service = ImportService(db)

    # Import data from JSON file
    data_file = Path(__file__).parent.parent / "data" / "cca_platforms.json"
    vertex_stats = import_service.import_json_file(data_file)

    # Create relationships
    edge_stats = import_service.create_relationships()

    # Combine stats
    all_stats = {**vertex_stats, **edge_stats}

    print("\n" + "="*60)
    print("Import Complete!")
    print("="*60)
    print(f"\nVertices imported:")
    for key, value in vertex_stats.items():
        if key != "errors" and value > 0:
            print(f"  {key}: {value}")

    print(f"\nEdges created:")
    for key, value in edge_stats.items():
        if key != "errors" and value > 0:
            print(f"  {key}: {value}")

    if all_stats.get("errors", 0) > 0:
        print(f"\n⚠ Errors: {all_stats['errors']}")

    return all_stats
