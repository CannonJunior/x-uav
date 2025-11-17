"""
ArangoDB schema initialization.

Defines collections, edge definitions, and graph structure for the UAV database.
"""

from typing import Dict, List
from arango.database import StandardDatabase
from arango.graph import Graph


# Collection definitions
VERTEX_COLLECTIONS = {
    "platform_families": {
        "description": "UAV platform families (e.g., Fury, Gambit, Ghost Bat)",
        "schema": {
            "type": "object",
            "properties": {
                "_key": {"type": "string"},
                "name": {"type": "string"},
                "manufacturer": {"type": "string"},
                "program": {"type": "string"},
                "base_technology": {"type": "string"},
                "description": {"type": "string"},
                "country": {"type": "string"},
            },
            "required": ["name", "manufacturer"]
        }
    },
    "platform_variants": {
        "description": "Specific UAV variants (e.g., YFQ-44A, Gambit 4, Gambit 6)",
        "schema": {
            "type": "object",
            "properties": {
                "_key": {"type": "string"},
                "name": {"type": "string"},
                "designation": {"type": "string"},
                "airframe_type": {"type": "string"},
                "development_status": {"type": "string"},
                "first_flight": {"type": "string"},
                "description": {"type": "string"},
            },
            "required": ["name"]
        }
    },
    "mission_configurations": {
        "description": "Mission-specific configurations (e.g., Fury-ISR, Gambit 6 Strike)",
        "schema": {
            "type": "object",
            "properties": {
                "_key": {"type": "string"},
                "name": {"type": "string"},
                "mission_type": {"type": "string"},
                "payload_description": {"type": "string"},
                "estimated_cost_per_sortie": {"type": "number"},
            },
            "required": ["name", "mission_type"]
        }
    },
    "platforms": {
        "description": "Legacy/simple platforms without variants",
        "schema": {
            "type": "object",
            "properties": {
                "_key": {"type": "string"},
                "name": {"type": "string"},
                "manufacturer": {"type": "string"},
                "country": {"type": "string"},
                "category": {"type": "string"},
                "first_flight": {"type": "string"},
                "status": {"type": "string"},
                "description": {"type": "string"},
            },
            "required": ["name", "manufacturer"]
        }
    },
    "countries": {
        "description": "Countries (manufacturers and operators)",
        "schema": {
            "type": "object",
            "properties": {
                "_key": {"type": "string"},
                "name": {"type": "string"},
                "iso_code": {"type": "string"},
                "region": {"type": "string"},
                "nato_member": {"type": "boolean"},
            },
            "required": ["name", "iso_code"]
        }
    },
    "manufacturers": {
        "description": "UAV manufacturers and autonomy providers",
        "schema": {
            "type": "object",
            "properties": {
                "_key": {"type": "string"},
                "name": {"type": "string"},
                "headquarters": {"type": "string"},
                "country": {"type": "string"},
                "type": {"type": "string"},
            },
            "required": ["name"]
        }
    },
    "missions": {
        "description": "Mission types (ISR, Strike, EW, etc.)",
        "schema": {
            "type": "object",
            "properties": {
                "_key": {"type": "string"},
                "name": {"type": "string"},
                "category": {"type": "string"},
                "description": {"type": "string"},
            },
            "required": ["name"]
        }
    },
    "sensors": {
        "description": "Sensor systems",
        "schema": {
            "type": "object",
            "properties": {
                "_key": {"type": "string"},
                "name": {"type": "string"},
                "type": {"type": "string"},
                "manufacturer": {"type": "string"},
                "specifications": {"type": "object"},
            },
            "required": ["name", "type"]
        }
    },
    "weapons": {
        "description": "Weapon systems",
        "schema": {
            "type": "object",
            "properties": {
                "_key": {"type": "string"},
                "name": {"type": "string"},
                "type": {"type": "string"},
                "manufacturer": {"type": "string"},
                "specifications": {"type": "object"},
            },
            "required": ["name", "type"]
        }
    },
    "military_units": {
        "description": "Military units operating UAVs",
        "schema": {
            "type": "object",
            "properties": {
                "_key": {"type": "string"},
                "name": {"type": "string"},
                "service_branch": {"type": "string"},
                "country": {"type": "string"},
                "base_location": {"type": "string"},
            },
            "required": ["name", "country"]
        }
    },
    "programs": {
        "description": "Development and procurement programs",
        "schema": {
            "type": "object",
            "properties": {
                "_key": {"type": "string"},
                "name": {"type": "string"},
                "country": {"type": "string"},
                "budget": {"type": "number"},
                "start_date": {"type": "string"},
                "status": {"type": "string"},
            },
            "required": ["name"]
        }
    },
    "technologies": {
        "description": "Technologies implemented in UAVs",
        "schema": {
            "type": "object",
            "properties": {
                "_key": {"type": "string"},
                "name": {"type": "string"},
                "type": {"type": "string"},
                "maturity_level": {"type": "string"},
                "description": {"type": "string"},
            },
            "required": ["name", "type"]
        }
    },
    "specifications": {
        "description": "Technical specifications",
        "schema": {
            "type": "object",
            "properties": {
                "_key": {"type": "string"},
                "category": {"type": "string"},
                "name": {"type": "string"},
                "value": {"type": "number"},
                "unit": {"type": "string"},
            },
            "required": ["name", "value", "unit"]
        }
    }
}


# Edge collection definitions
EDGE_COLLECTIONS = {
    # Variant hierarchy relationships
    "belongs_to_family": {
        "from": ["platform_variants"],
        "to": ["platform_families"],
        "description": "Variant belongs to platform family"
    },
    "has_variant": {
        "from": ["platform_families"],
        "to": ["platform_variants"],
        "description": "Platform family has variant"
    },
    "has_configuration": {
        "from": ["platform_variants"],
        "to": ["mission_configurations"],
        "description": "Variant has mission configuration"
    },
    "configured_from": {
        "from": ["mission_configurations"],
        "to": ["platform_variants"],
        "description": "Configuration is based on variant"
    },
    "configured_for": {
        "from": ["mission_configurations"],
        "to": ["missions"],
        "description": "Configuration is for specific mission"
    },

    # Standard platform relationships
    "manufactured_by": {
        "from": ["platform_families", "platforms"],
        "to": ["manufacturers"],
        "description": "Platform manufactured by company"
    },
    "manufactured_in": {
        "from": ["platform_families", "platforms"],
        "to": ["countries"],
        "description": "Platform manufactured in country"
    },
    "operated_by": {
        "from": ["platform_variants", "platforms"],
        "to": ["countries"],
        "description": "Platform operated by country"
    },
    "procured_by": {
        "from": ["platform_variants", "platforms"],
        "to": ["military_units"],
        "description": "Platform procured by military unit"
    },
    "performs_mission": {
        "from": ["mission_configurations", "platforms"],
        "to": ["missions"],
        "description": "Platform performs mission type"
    },
    "equipped_with": {
        "from": ["mission_configurations", "platforms"],
        "to": ["sensors"],
        "description": "Platform equipped with sensor"
    },
    "carries_weapon": {
        "from": ["mission_configurations", "platforms"],
        "to": ["weapons"],
        "description": "Platform carries weapon"
    },
    "developed_under": {
        "from": ["platform_families"],
        "to": ["programs"],
        "description": "Platform developed under program"
    },
    "implements_tech": {
        "from": ["platform_variants", "platforms"],
        "to": ["technologies"],
        "description": "Platform implements technology"
    },
    "has_specification": {
        "from": ["platform_variants", "mission_configurations", "platforms"],
        "to": ["specifications"],
        "description": "Platform has specification"
    },
    "competes_with": {
        "from": ["platform_families"],
        "to": ["platform_families"],
        "description": "Platform family competes with another"
    },
    "competes_with_config": {
        "from": ["mission_configurations"],
        "to": ["mission_configurations"],
        "description": "Mission configuration competes with another"
    },
    "derived_from": {
        "from": ["platform_variants"],
        "to": ["platform_variants"],
        "description": "Variant derived from predecessor"
    },
    "requires": {
        "from": ["technologies"],
        "to": ["technologies"],
        "description": "Technology requires other technology"
    },
    "exports_to": {
        "from": ["countries"],
        "to": ["countries"],
        "description": "Country exports to another country"
    },
    "supplies": {
        "from": ["manufacturers"],
        "to": ["programs"],
        "description": "Manufacturer supplies program"
    },
    "provides_autonomy": {
        "from": ["manufacturers"],
        "to": ["platform_variants"],
        "description": "Manufacturer provides autonomy software"
    }
}


def init_collections(db: StandardDatabase) -> None:
    """
    Initialize all vertex collections.

    Args:
        db: ArangoDB database instance
    """
    print("Creating vertex collections...")

    for collection_name, config in VERTEX_COLLECTIONS.items():
        if not db.has_collection(collection_name):
            collection = db.create_collection(collection_name)
            print(f"  ✓ Created collection: {collection_name}")
        else:
            print(f"  - Collection already exists: {collection_name}")


def init_edge_collections(db: StandardDatabase) -> None:
    """
    Initialize all edge collections.

    Args:
        db: ArangoDB database instance
    """
    print("Creating edge collections...")

    for edge_name, config in EDGE_COLLECTIONS.items():
        if not db.has_collection(edge_name):
            collection = db.create_collection(edge_name, edge=True)
            print(f"  ✓ Created edge collection: {edge_name}")
        else:
            print(f"  - Edge collection already exists: {edge_name}")


def init_graph(db: StandardDatabase, graph_name: str = "uav_graph") -> Graph:
    """
    Initialize UAV graph with all edge definitions.

    Args:
        db: ArangoDB database instance
        graph_name: Name of the graph

    Returns:
        Graph: Initialized graph instance
    """
    print(f"Creating graph: {graph_name}...")

    # Delete existing graph if it exists
    if db.has_graph(graph_name):
        db.delete_graph(graph_name, drop_collections=False)
        print(f"  - Deleted existing graph: {graph_name}")

    # Create graph with edge definitions
    edge_definitions = []
    for edge_name, config in EDGE_COLLECTIONS.items():
        edge_definitions.append({
            "edge_collection": edge_name,
            "from_vertex_collections": config["from"],
            "to_vertex_collections": config["to"]
        })

    graph = db.create_graph(graph_name, edge_definitions=edge_definitions)
    print(f"  ✓ Created graph with {len(edge_definitions)} edge definitions")

    return graph


def init_indexes(db: StandardDatabase) -> None:
    """
    Create indexes for performance optimization.

    Args:
        db: ArangoDB database instance
    """
    print("Creating indexes...")

    # Platform families
    if db.has_collection("platform_families"):
        db.collection("platform_families").add_hash_index(fields=["name"], unique=True)
        db.collection("platform_families").add_hash_index(fields=["manufacturer"])
        db.collection("platform_families").add_hash_index(fields=["program"])
        print("  ✓ Created indexes for platform_families")

    # Platform variants
    if db.has_collection("platform_variants"):
        db.collection("platform_variants").add_hash_index(fields=["name"])
        db.collection("platform_variants").add_hash_index(fields=["designation"], unique=True)
        print("  ✓ Created indexes for platform_variants")

    # Mission configurations
    if db.has_collection("mission_configurations"):
        db.collection("mission_configurations").add_hash_index(fields=["mission_type"])
        print("  ✓ Created indexes for mission_configurations")

    # Countries
    if db.has_collection("countries"):
        db.collection("countries").add_hash_index(fields=["iso_code"], unique=True)
        db.collection("countries").add_hash_index(fields=["name"], unique=True)
        print("  ✓ Created indexes for countries")


def init_schema(db: StandardDatabase) -> Graph:
    """
    Initialize complete database schema.

    Args:
        db: ArangoDB database instance

    Returns:
        Graph: Initialized graph instance
    """
    print("\n" + "="*60)
    print("Initializing X-UAV Database Schema")
    print("="*60 + "\n")

    init_collections(db)
    init_edge_collections(db)
    graph = init_graph(db)
    init_indexes(db)

    print("\n" + "="*60)
    print("Schema initialization complete!")
    print("="*60 + "\n")

    return graph
