"""
Graph query service.

Provides methods for traversing the X-UAV knowledge graph using AQL.
"""

from typing import List, Dict, Any, Optional
from arango.database import StandardDatabase
from arango.cursor import Cursor


class QueryService:
    """Service for querying the X-UAV knowledge graph."""

    def __init__(self, db: StandardDatabase):
        """
        Initialize query service.

        Args:
            db: ArangoDB database instance
        """
        self.db = db

    def get_platform_configurations(
        self, family_key: str
    ) -> List[Dict[str, Any]]:
        """
        Get all mission configurations for a platform family.

        Traversal pattern: Family → Variants → Configurations

        Args:
            family_key: Platform family identifier (e.g., "fury")

        Returns:
            List of configuration records with variant and mission details
        """
        query = """
        FOR family IN platform_families
            FILTER family._key == @family_key
            FOR variant IN 1..1 INBOUND family belongs_to_family
                FOR config IN 1..1 INBOUND variant configured_from
                    LET mission = FIRST(
                        FOR m IN 1..1 OUTBOUND config configured_for
                            RETURN m
                    )
                    RETURN DISTINCT {
                        family: family.name,
                        variant: variant.name,
                        designation: variant.designation,
                        configuration: config.name,
                        mission_type: mission.name,
                        mission_category: mission.category,
                        payload: config.payload_description,
                        cost_per_sortie: config.estimated_cost_per_sortie
                    }
        """
        cursor = self.db.aql.execute(query, bind_vars={"family_key": family_key})
        return list(cursor)

    def get_variant_technologies(
        self, variant_key: str
    ) -> List[Dict[str, Any]]:
        """
        Get all technologies implemented by a platform variant.

        Traversal pattern: Variant → Technologies

        Args:
            variant_key: Platform variant identifier (e.g., "yfq-44a")

        Returns:
            List of technology records
        """
        query = """
        FOR variant IN platform_variants
            FILTER variant._key == @variant_key
            FOR tech IN 1..1 OUTBOUND variant implements_tech
                RETURN DISTINCT {
                    variant: variant.name,
                    technology: tech.name,
                    type: tech.type,
                    maturity: tech.maturity_level,
                    description: tech.description
                }
        """
        cursor = self.db.aql.execute(query, bind_vars={"variant_key": variant_key})
        return list(cursor)

    def get_supply_chain(self, variant_key: str) -> Dict[str, Any]:
        """
        Get complete supply chain for a platform variant.

        Traversal pattern: Variant → Family → Manufacturer + Autonomy Providers

        Args:
            variant_key: Platform variant identifier (e.g., "yfq-44a")

        Returns:
            Supply chain details including manufacturer and autonomy providers
        """
        query = """
        FOR variant IN platform_variants
            FILTER variant._key == @variant_key

            LET family = FIRST(
                FOR f IN 1..1 OUTBOUND variant belongs_to_family
                    RETURN f
            )

            LET manufacturer = FIRST(
                FOR m IN 1..1 OUTBOUND family manufactured_by
                    RETURN m
            )

            LET autonomy_providers = (
                FOR provider IN 1..1 INBOUND variant provides_autonomy
                    RETURN DISTINCT {
                        name: provider.name,
                        type: provider.type,
                        headquarters: provider.headquarters
                    }
            )

            RETURN {
                variant: variant.name,
                designation: variant.designation,
                family: family.name,
                manufacturer: {
                    name: manufacturer.name,
                    type: manufacturer.type,
                    headquarters: manufacturer.headquarters,
                    country: manufacturer.country
                },
                autonomy_providers: autonomy_providers
            }
        """
        cursor = self.db.aql.execute(query, bind_vars={"variant_key": variant_key})
        results = list(cursor)
        return results[0] if results else {}

    def get_mission_capable_platforms(
        self, mission_key: str
    ) -> List[Dict[str, Any]]:
        """
        Find all platforms capable of performing a specific mission.

        Traversal pattern: Mission → Configurations → Variants → Families

        Args:
            mission_key: Mission type identifier (e.g., "isr", "strike")

        Returns:
            List of platforms capable of the mission
        """
        query = """
        FOR mission IN missions
            FILTER mission._key == @mission_key
            FOR config IN 1..1 INBOUND mission configured_for
                FOR variant IN 1..1 OUTBOUND config configured_from
                    FOR family IN 1..1 OUTBOUND variant belongs_to_family
                        FOR manufacturer IN 1..1 OUTBOUND family manufactured_by
                            RETURN DISTINCT {
                                family: family.name,
                                variant: variant.name,
                                designation: variant.designation,
                                configuration: config.name,
                                manufacturer: manufacturer.name,
                                payload: config.payload_description,
                                cost_per_sortie: config.estimated_cost_per_sortie,
                                status: variant.development_status
                            }
        """
        cursor = self.db.aql.execute(query, bind_vars={"mission_key": mission_key})
        return list(cursor)

    def get_program_platforms(self, program_key: str) -> List[Dict[str, Any]]:
        """
        Get all platforms developed under a specific program.

        Traversal pattern: Program → Families → Variants

        Args:
            program_key: Program identifier (e.g., "cca-increment-1")

        Returns:
            List of platforms in the program
        """
        query = """
        FOR program IN programs
            FILTER program._key == @program_key
            FOR family IN 1..1 INBOUND program developed_under
                FOR manufacturer IN 1..1 OUTBOUND family manufactured_by
                    LET variants = (
                        FOR variant IN 1..1 INBOUND family belongs_to_family
                            RETURN DISTINCT {
                                name: variant.name,
                                designation: variant.designation,
                                status: variant.development_status,
                                first_flight: variant.first_flight
                            }
                    )
                    RETURN DISTINCT {
                        program: program.name,
                        budget: program.budget,
                        family: family.name,
                        manufacturer: manufacturer.name,
                        variants: variants,
                        base_technology: family.base_technology
                    }
        """
        cursor = self.db.aql.execute(query, bind_vars={"program_key": program_key})
        return list(cursor)

    def get_configuration_provenance(
        self, config_key: str
    ) -> Optional[Dict[str, Any]]:
        """
        Get complete provenance chain for a mission configuration.

        Traversal pattern: Configuration → Variant → Family → Manufacturer + Program

        Args:
            config_key: Mission configuration identifier (e.g., "fury-isr")

        Returns:
            Complete provenance information or None if not found
        """
        query = """
        FOR config IN mission_configurations
            FILTER config._key == @config_key

            LET variant = FIRST(
                FOR v IN 1..1 OUTBOUND config configured_from
                    RETURN v
            )

            LET family = FIRST(
                FOR f IN 1..1 OUTBOUND variant belongs_to_family
                    RETURN f
            )

            LET manufacturer = FIRST(
                FOR m IN 1..1 OUTBOUND family manufactured_by
                    RETURN m
            )

            LET program = FIRST(
                FOR p IN 1..1 OUTBOUND family developed_under
                    RETURN p
            )

            LET mission = FIRST(
                FOR m IN 1..1 OUTBOUND config configured_for
                    RETURN m
            )

            LET technologies = (
                FOR tech IN 1..1 OUTBOUND variant implements_tech
                    RETURN DISTINCT tech.name
            )

            RETURN {
                configuration: config.name,
                mission: {
                    type: mission.name,
                    category: mission.category,
                    description: mission.description
                },
                variant: {
                    name: variant.name,
                    designation: variant.designation,
                    airframe_type: variant.airframe_type,
                    status: variant.development_status,
                    first_flight: variant.first_flight
                },
                family: {
                    name: family.name,
                    description: family.description,
                    base_technology: family.base_technology
                },
                manufacturer: {
                    name: manufacturer.name,
                    headquarters: manufacturer.headquarters,
                    type: manufacturer.type
                },
                program: program ? {
                    name: program.name,
                    budget: program.budget,
                    status: program.status,
                    start_date: program.start_date
                } : null,
                technologies: technologies,
                payload: config.payload_description,
                cost_per_sortie: config.estimated_cost_per_sortie
            }
        """
        cursor = self.db.aql.execute(query, bind_vars={"config_key": config_key})
        results = list(cursor)
        return results[0] if results else None

    def get_technology_adoption(self, tech_key: str) -> List[Dict[str, Any]]:
        """
        Find all platforms implementing a specific technology.

        Traversal pattern: Technology → Variants → Families

        Args:
            tech_key: Technology identifier (e.g., "hivemind-ai")

        Returns:
            List of platforms using the technology
        """
        query = """
        FOR tech IN technologies
            FILTER tech._key == @tech_key
            FOR variant IN 1..1 INBOUND tech implements_tech
                FOR family IN 1..1 OUTBOUND variant belongs_to_family
                    FOR manufacturer IN 1..1 OUTBOUND family manufactured_by
                        RETURN {
                            technology: tech.name,
                            variant: variant.name,
                            designation: variant.designation,
                            family: family.name,
                            manufacturer: manufacturer.name,
                            status: variant.development_status
                        }
        """
        cursor = self.db.aql.execute(query, bind_vars={"tech_key": tech_key})
        return list(cursor)

    def get_manufacturer_portfolio(
        self, manufacturer_key: str
    ) -> Dict[str, Any]:
        """
        Get complete portfolio for a manufacturer.

        Includes platforms manufactured and autonomy systems provided.

        Args:
            manufacturer_key: Manufacturer identifier (e.g., "anduril")

        Returns:
            Complete manufacturer portfolio
        """
        query = """
        FOR mfr IN manufacturers
            FILTER mfr._key == @manufacturer_key

            LET platforms = (
                FOR family IN 1..1 INBOUND mfr manufactured_by
                    LET variants = (
                        FOR variant IN 1..1 INBOUND family belongs_to_family
                            RETURN {
                                name: variant.name,
                                designation: variant.designation,
                                status: variant.development_status
                            }
                    )
                    RETURN {
                        family: family.name,
                        program: family.program,
                        variants: variants
                    }
            )

            LET autonomy_systems = (
                FOR variant IN 1..1 OUTBOUND mfr provides_autonomy
                    FOR family IN 1..1 OUTBOUND variant belongs_to_family
                        RETURN {
                            variant: variant.name,
                            family: family.name
                        }
            )

            RETURN {
                manufacturer: mfr.name,
                type: mfr.type,
                headquarters: mfr.headquarters,
                country: mfr.country,
                platforms: platforms,
                autonomy_systems: autonomy_systems
            }
        """
        cursor = self.db.aql.execute(
            query, bind_vars={"manufacturer_key": manufacturer_key}
        )
        results = list(cursor)
        return results[0] if results else {}

    def search_platforms(
        self,
        airframe_type: Optional[str] = None,
        development_status: Optional[str] = None,
        mission_type: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """
        Search platforms with optional filters.

        Args:
            airframe_type: Filter by airframe type (e.g., "Fixed-wing")
            development_status: Filter by status (e.g., "Flight testing")
            mission_type: Filter by mission capability (e.g., "ISR")

        Returns:
            List of matching platforms
        """
        filters = []
        bind_vars = {}

        if airframe_type:
            filters.append("variant.airframe_type == @airframe_type")
            bind_vars["airframe_type"] = airframe_type

        if development_status:
            filters.append("variant.development_status == @development_status")
            bind_vars["development_status"] = development_status

        filter_clause = (
            f"FILTER {' AND '.join(filters)}" if filters else ""
        )

        if mission_type:
            # Reason: Mission filtering requires joining through configurations
            query = f"""
            FOR variant IN platform_variants
                {filter_clause}
                FOR config IN 1..1 INBOUND variant configured_from
                    FILTER config.mission_type == @mission_type
                    FOR family IN 1..1 OUTBOUND variant belongs_to_family
                        FOR manufacturer IN 1..1 OUTBOUND family manufactured_by
                            RETURN DISTINCT {{
                                variant: variant.name,
                                designation: variant.designation,
                                airframe_type: variant.airframe_type,
                                status: variant.development_status,
                                family: family.name,
                                manufacturer: manufacturer.name,
                                mission_type: config.mission_type
                            }}
            """
            bind_vars["mission_type"] = mission_type
        else:
            query = f"""
            FOR variant IN platform_variants
                {filter_clause}
                FOR family IN 1..1 OUTBOUND variant belongs_to_family
                    FOR manufacturer IN 1..1 OUTBOUND family manufactured_by
                        RETURN {{
                            variant: variant.name,
                            designation: variant.designation,
                            airframe_type: variant.airframe_type,
                            status: variant.development_status,
                            family: family.name,
                            manufacturer: manufacturer.name
                        }}
            """

        cursor = self.db.aql.execute(query, bind_vars=bind_vars)
        return list(cursor)
