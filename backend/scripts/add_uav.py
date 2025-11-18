#!/usr/bin/env python
"""
UAV Data Entry Tool

Interactive script for adding UAVs to the X-UAV database.
"""

import sys
import json
from pathlib import Path
from typing import Dict, Any, List, Optional

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.db.arangodb import arango_connection


class UAVDataEntry:
    """Interactive UAV data entry tool."""

    def __init__(self, db):
        """Initialize with database connection."""
        self.db = db

    def list_existing_uavs(self):
        """List all existing UAVs in the database."""
        print("\n" + "="*60)
        print("Existing UAVs in Database")
        print("="*60 + "\n")

        query = """
        FOR variant IN platform_variants
            LET family = FIRST(
                FOR f IN 1..1 OUTBOUND variant belongs_to_family
                    RETURN f
            )
            LET manufacturer = FIRST(
                FOR f IN platform_families
                    FILTER f._key == family._key
                    FOR m IN 1..1 OUTBOUND f manufactured_by
                        RETURN m
            )
            SORT variant.name
            RETURN {
                designation: variant.designation,
                name: variant.name,
                family: family.name,
                manufacturer: manufacturer.name,
                status: variant.development_status
            }
        """

        cursor = self.db.aql.execute(query)
        results = list(cursor)

        if not results:
            print("No UAVs found in database.\n")
            return

        print(f"{'Designation':<15} {'Name':<25} {'Family':<20} {'Manufacturer':<30} {'Status':<15}")
        print("-" * 105)

        for uav in results:
            print(f"{uav['designation']:<15} {uav['name']:<25} {uav['family']:<20} {uav['manufacturer']:<30} {uav['status']:<15}")

        print(f"\nTotal: {len(results)} UAVs\n")

    def add_variant_interactive(self):
        """Add a platform variant interactively."""
        print("\n" + "="*60)
        print("Add New Platform Variant")
        print("="*60 + "\n")

        # Get family
        families = list(self.db.collection('platform_families'))
        if not families:
            print("Error: No platform families found. Add a family first.")
            return

        print("Available Families:")
        for i, fam in enumerate(families, 1):
            print(f"  {i}. {fam['name']} ({fam.get('manufacturer', 'Unknown')})")

        fam_choice = input("\nSelect family number (or 'c' to cancel): ").strip()
        if fam_choice.lower() == 'c':
            return

        try:
            family_key = families[int(fam_choice) - 1]['_key']
        except (ValueError, IndexError):
            print("Invalid selection.")
            return

        # Collect variant data
        print("\nEnter Variant Details:")
        variant_data = {
            "_key": input("  Key (e.g., mq-9b-skyguardian): ").strip().lower().replace(" ", "-"),
            "name": input("  Name: ").strip(),
            "designation": input("  Designation (e.g., MQ-9B): ").strip(),
            "airframe_type": input("  Airframe Type (e.g., Fixed-wing, VTOL): ").strip(),
            "development_status": input("  Status (Development/Flight testing/Operational): ").strip(),
            "description": input("  Description: ").strip(),
        }

        first_flight = input("  First Flight Date (YYYY-MM-DD or leave blank): ").strip()
        variant_data["first_flight"] = first_flight if first_flight else None

        # Insert variant
        try:
            self.db.collection('platform_variants').insert(variant_data)
            print(f"\n✓ Variant '{variant_data['name']}' added successfully!")

            # Create edge to family
            edge_data = {
                "_from": f"platform_variants/{variant_data['_key']}",
                "_to": f"platform_families/{family_key}"
            }
            self.db.collection('belongs_to_family').insert(edge_data)
            print(f"✓ Linked to family '{families[int(fam_choice) - 1]['name']}'")

        except Exception as e:
            print(f"\n✗ Error adding variant: {e}")

    def add_from_json(self, json_file: Path):
        """Add UAVs from a JSON file."""
        print(f"\nImporting UAVs from: {json_file}")

        try:
            with open(json_file, 'r') as f:
                data = json.load(f)
        except Exception as e:
            print(f"Error reading file: {e}")
            return

        # Import variants
        variants = data.get('platform_variants', [])
        if not variants:
            print("No platform_variants found in JSON file.")
            return

        imported = 0
        errors = 0

        for variant in variants:
            try:
                self.db.collection('platform_variants').insert(variant, silent=True, overwrite=True)
                print(f"  ✓ Imported: {variant.get('name', variant.get('_key'))}")
                imported += 1
            except Exception as e:
                print(f"  ✗ Error importing {variant.get('_key')}: {e}")
                errors += 1

        print(f"\nImport complete: {imported} imported, {errors} errors")

    def create_json_template(self):
        """Create a JSON template for adding UAVs."""
        template = {
            "platform_families": [
                {
                    "_key": "example-family",
                    "name": "Example UAV Family",
                    "manufacturer": "Example Manufacturer",
                    "program": "Example Program",
                    "base_technology": "Description of core tech",
                    "description": "Description of the platform family",
                    "country": "Country"
                }
            ],
            "platform_variants": [
                {
                    "_key": "example-variant",
                    "name": "Example UAV Variant Name",
                    "designation": "XQ-##",
                    "airframe_type": "Fixed-wing / VTOL / Helicopter",
                    "development_status": "Development / Flight testing / Operational",
                    "first_flight": "2025-01-01 or null",
                    "description": "Description of this specific variant"
                }
            ],
            "mission_configurations": [
                {
                    "_key": "example-config",
                    "name": "Example Config Name",
                    "mission_type": "ISR / Strike / EW / etc",
                    "payload_description": "Description of payload and sensors",
                    "estimated_cost_per_sortie": 50000
                }
            ]
        }

        filename = Path("uav_template.json")
        with open(filename, 'w') as f:
            json.dump(template, f, indent=2)

        print(f"\n✓ Template created: {filename}")
        print("\nEdit this file with your UAV data, then import with:")
        print(f"  uv run python scripts/add_uav.py --import {filename}\n")


def main():
    """Main entry point."""
    import argparse

    parser = argparse.ArgumentParser(description="X-UAV Data Entry Tool")
    parser.add_argument('--list', action='store_true', help='List existing UAVs')
    parser.add_argument('--add', action='store_true', help='Add a UAV interactively')
    parser.add_argument('--import', dest='import_file', help='Import from JSON file')
    parser.add_argument('--template', action='store_true', help='Create a JSON template')

    args = parser.parse_args()

    # Connect to database
    print("\n" + "="*60)
    print("X-UAV Data Entry Tool")
    print("="*60)

    try:
        db = arango_connection.connect()
        print(f"✓ Connected to database: {db.name}\n")
    except Exception as e:
        print(f"✗ Database connection failed: {e}")
        sys.exit(1)

    tool = UAVDataEntry(db)

    # Execute requested action
    if args.list:
        tool.list_existing_uavs()
    elif args.add:
        tool.add_variant_interactive()
    elif args.import_file:
        tool.add_from_json(Path(args.import_file))
    elif args.template:
        tool.create_json_template()
    else:
        # Interactive menu
        while True:
            print("\nWhat would you like to do?")
            print("  1. List existing UAVs")
            print("  2. Add a new UAV variant")
            print("  3. Import from JSON file")
            print("  4. Create JSON template")
            print("  5. Exit")

            choice = input("\nChoice (1-5): ").strip()

            if choice == '1':
                tool.list_existing_uavs()
            elif choice == '2':
                tool.add_variant_interactive()
            elif choice == '3':
                filename = input("JSON file path: ").strip()
                tool.add_from_json(Path(filename))
            elif choice == '4':
                tool.create_json_template()
            elif choice == '5':
                print("\nGoodbye!")
                break
            else:
                print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
