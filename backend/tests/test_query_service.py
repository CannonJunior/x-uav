"""
Tests for query service.

Validates graph traversal patterns and query correctness.
"""

import pytest
from pathlib import Path
import sys

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.db.arangodb import arango_connection
from app.db.schema import init_schema
from app.services.import_service import import_cca_data
from app.services.query_service import QueryService


@pytest.fixture(scope="module")
def test_db():
    """
    Set up test database with CCA data.

    Yields:
        ArangoDB database instance
    """
    # Connect to test database
    db = arango_connection.connect()

    # Initialize schema
    init_schema(db)

    # Import test data
    import_cca_data(db)

    yield db

    # Teardown: Could drop collections here if needed
    # For now, we'll keep data for inspection


@pytest.fixture
def query_service(test_db):
    """
    Create query service instance.

    Args:
        test_db: Test database fixture

    Returns:
        QueryService instance
    """
    return QueryService(test_db)


class TestPlatformConfigurations:
    """Test platform configuration queries."""

    def test_fury_configurations(self, query_service):
        """
        Test retrieving all Fury configurations.

        Expected: 4 configurations (ISR, Strike, EW, Decoy)
        """
        results = query_service.get_platform_configurations("fury")

        assert len(results) == 4, "Fury should have 4 configurations"

        # Validate structure
        for config in results:
            assert "family" in config
            assert "variant" in config
            assert "configuration" in config
            assert "mission_type" in config
            assert "payload" in config
            assert "cost_per_sortie" in config

        # Check specific configurations exist
        config_names = {r["configuration"] for r in results}
        expected = {"Fury-ISR", "Fury-Strike", "Fury-EW", "Fury-Decoy"}
        assert config_names == expected

    def test_gambit_configurations(self, query_service):
        """
        Test retrieving all Gambit configurations.

        Expected: 4 configurations across 3 variants
        """
        results = query_service.get_platform_configurations("gambit")

        assert len(results) >= 4, "Gambit should have at least 4 configurations"

        # Verify variants
        variants = {r["designation"] for r in results}
        assert "YFQ-42A" in variants  # Gambit 1
        assert "Gambit 4" in variants
        assert "Gambit 6" in variants

    def test_nonexistent_family(self, query_service):
        """Test querying non-existent platform family."""
        results = query_service.get_platform_configurations("nonexistent")

        assert len(results) == 0


class TestVariantTechnologies:
    """Test variant technology queries."""

    def test_fury_technologies(self, query_service):
        """
        Test retrieving technologies for YFQ-44A Fury.

        Expected: Lattice OS, Hivemind AI, MOSA
        """
        results = query_service.get_variant_technologies("yfq-44a")

        assert len(results) == 3, "YFQ-44A should implement 3 technologies"

        tech_names = {r["technology"] for r in results}
        expected = {"Lattice OS", "Hivemind AI", "MOSA"}
        assert tech_names == expected

        # Validate structure
        for tech in results:
            assert "variant" in tech
            assert "technology" in tech
            assert "type" in tech
            assert "maturity" in tech
            assert "description" in tech

    def test_x_bat_technologies(self, query_service):
        """
        Test retrieving technologies for X-BAT.

        Expected: Hivemind AI
        """
        results = query_service.get_variant_technologies("x-bat-1")

        assert len(results) == 1
        assert results[0]["technology"] == "Hivemind AI"

    def test_variant_without_technologies(self, query_service):
        """Test variant with no explicit technology implementations."""
        results = query_service.get_variant_technologies("gambit-1")

        # Gambit-1 may or may not have technologies depending on data
        # Just verify no error occurs
        assert isinstance(results, list)


class TestSupplyChain:
    """Test supply chain queries."""

    def test_fury_supply_chain(self, query_service):
        """
        Test Fury supply chain.

        Expected: Anduril (manufacturer) + Shield AI (autonomy provider)
        """
        result = query_service.get_supply_chain("yfq-44a")

        assert result is not None
        assert result["variant"] == "YFQ-44A Fury"
        assert result["family"] == "Fury"
        assert result["manufacturer"]["name"] == "Anduril Industries"
        assert len(result["autonomy_providers"]) == 1
        assert result["autonomy_providers"][0]["name"] == "Shield AI"

    def test_gambit_supply_chain(self, query_service):
        """
        Test Gambit supply chain.

        Expected: General Atomics (manufacturer) + RTX (autonomy for Gambit-1)
        """
        result = query_service.get_supply_chain("gambit-1")

        assert result is not None
        assert result["manufacturer"]["name"] == "General Atomics Aeronautical Systems"

        # RTX provides autonomy for Gambit-1
        providers = result["autonomy_providers"]
        if providers:
            assert any(p["name"] == "RTX Corporation" for p in providers)

    def test_nonexistent_variant(self, query_service):
        """Test supply chain for non-existent variant."""
        result = query_service.get_supply_chain("nonexistent")

        assert result == {}


class TestMissionCapablePlatforms:
    """Test mission-capable platform queries."""

    def test_isr_capable_platforms(self, query_service):
        """
        Test finding ISR-capable platforms.

        Expected: Multiple platforms (Fury, Gambit-4, Ghost Bat, X-BAT)
        """
        results = query_service.get_mission_capable_platforms("isr")

        assert len(results) >= 4, "Multiple platforms should support ISR"

        # Verify expected families
        families = {r["family"] for r in results}
        assert "Fury" in families
        assert "Gambit" in families

        # Validate structure
        for platform in results:
            assert "family" in platform
            assert "variant" in platform
            assert "configuration" in platform
            assert "manufacturer" in platform
            assert "payload" in platform
            assert "cost_per_sortie" in platform

    def test_strike_capable_platforms(self, query_service):
        """Test finding strike-capable platforms."""
        results = query_service.get_mission_capable_platforms("strike")

        assert len(results) >= 3

        # All should have strike-related payloads
        for platform in results:
            payload = platform["payload"].lower()
            assert any(
                keyword in payload
                for keyword in ["strike", "munitions", "weapons", "missile"]
            )

    def test_air_to_air_platforms(self, query_service):
        """Test finding air-to-air capable platforms."""
        results = query_service.get_mission_capable_platforms("air-to-air")

        assert len(results) >= 1

        # Should include Gambit-1
        config_names = {r["configuration"] for r in results}
        assert "Gambit 1 Air-to-Air" in config_names


class TestProgramPlatforms:
    """Test program platform queries."""

    def test_cca_increment_1_platforms(self, query_service):
        """
        Test platforms in CCA Increment 1.

        Expected: Fury and Gambit families
        """
        results = query_service.get_program_platforms("cca-increment-1")

        assert len(results) == 2, "CCA Increment 1 should have 2 platform families"

        families = {r["family"] for r in results}
        assert "Fury" in families
        assert "Gambit" in families

        # Validate program details
        for platform in results:
            assert platform["program"] == "CCA Increment 1"
            assert platform["budget"] == 6000000000
            assert "variants" in platform
            assert len(platform["variants"]) > 0

    def test_nonexistent_program(self, query_service):
        """Test querying non-existent program."""
        results = query_service.get_program_platforms("nonexistent-program")

        assert len(results) == 0


class TestConfigurationProvenance:
    """Test configuration provenance queries."""

    def test_fury_isr_provenance(self, query_service):
        """
        Test complete provenance for Fury-ISR configuration.

        Validates full chain: Config → Variant → Family → Manufacturer → Program
        """
        result = query_service.get_configuration_provenance("fury-isr")

        assert result is not None

        # Configuration details
        assert result["configuration"] == "Fury-ISR"
        assert result["cost_per_sortie"] == 45000

        # Mission details
        assert result["mission"]["type"] == "ISR"
        assert result["mission"]["category"] == "Intelligence, Surveillance, Reconnaissance"

        # Variant details
        assert result["variant"]["name"] == "YFQ-44A Fury"
        assert result["variant"]["designation"] == "YFQ-44A"
        assert result["variant"]["airframe_type"] == "Fixed-wing"

        # Family details
        assert result["family"]["name"] == "Fury"

        # Manufacturer details
        assert result["manufacturer"]["name"] == "Anduril Industries"
        assert result["manufacturer"]["headquarters"] == "Costa Mesa, California"

        # Program details
        assert result["program"] is not None
        assert result["program"]["name"] == "CCA Increment 1"
        assert result["program"]["budget"] == 6000000000

        # Technologies
        assert len(result["technologies"]) == 3
        assert "Lattice OS" in result["technologies"]
        assert "Hivemind AI" in result["technologies"]
        assert "MOSA" in result["technologies"]

    def test_gambit_strike_provenance(self, query_service):
        """Test provenance for Gambit-6 Strike configuration."""
        result = query_service.get_configuration_provenance("gambit-6-strike")

        assert result is not None
        assert result["configuration"] == "Gambit 6 Strike"
        assert result["mission"]["type"] == "Strike"
        assert result["manufacturer"]["name"] == "General Atomics Aeronautical Systems"

    def test_nonexistent_configuration(self, query_service):
        """Test provenance for non-existent configuration."""
        result = query_service.get_configuration_provenance("nonexistent-config")

        assert result is None


class TestTechnologyAdoption:
    """Test technology adoption queries."""

    def test_hivemind_adoption(self, query_service):
        """
        Test Hivemind AI adoption.

        Expected: YFQ-44A Fury and X-BAT
        """
        results = query_service.get_technology_adoption("hivemind-ai")

        assert len(results) >= 2

        variants = {r["variant"] for r in results}
        assert "YFQ-44A Fury" in variants
        assert "X-BAT" in variants

    def test_lattice_os_adoption(self, query_service):
        """Test Lattice OS adoption."""
        results = query_service.get_technology_adoption("lattice-os")

        assert len(results) >= 1

        # Should be adopted by Fury
        families = {r["family"] for r in results}
        assert "Fury" in families

    def test_centaur_ai_adoption(self, query_service):
        """Test Centaur AI adoption."""
        results = query_service.get_technology_adoption("centaur-ai")

        assert len(results) >= 1

        # CA-1 Europa uses Centaur AI
        variants = {r["variant"] for r in results}
        assert "CA-1 Europa" in variants


class TestManufacturerPortfolio:
    """Test manufacturer portfolio queries."""

    def test_anduril_portfolio(self, query_service):
        """
        Test Anduril portfolio.

        Expected: Fury family (manufactured) + YFQ-44A (no autonomy provided)
        """
        result = query_service.get_manufacturer_portfolio("anduril")

        assert result is not None
        assert result["manufacturer"] == "Anduril Industries"
        assert result["type"] == "Private defense technology company"
        assert result["headquarters"] == "Costa Mesa, California"

        # Should manufacture Fury
        assert len(result["platforms"]) >= 1
        family_names = {p["family"] for p in result["platforms"]}
        assert "Fury" in family_names

    def test_shield_ai_portfolio(self, query_service):
        """
        Test Shield AI portfolio.

        Expected: X-BAT (manufactured) + YFQ-44A (autonomy provided)
        """
        result = query_service.get_manufacturer_portfolio("shield-ai")

        assert result is not None
        assert result["manufacturer"] == "Shield AI"

        # Should provide autonomy to Fury
        autonomy_variants = {a["variant"] for a in result["autonomy_systems"]}
        assert "YFQ-44A Fury" in autonomy_variants

    def test_general_atomics_portfolio(self, query_service):
        """Test General Atomics portfolio."""
        result = query_service.get_manufacturer_portfolio("general-atomics")

        assert result is not None

        # Should manufacture Gambit family
        family_names = {p["family"] for p in result["platforms"]}
        assert "Gambit" in family_names


class TestPlatformSearch:
    """Test platform search queries."""

    def test_search_by_airframe_type(self, query_service):
        """Test searching by airframe type."""
        results = query_service.search_platforms(airframe_type="Fixed-wing")

        assert len(results) >= 3

        # All should be fixed-wing
        for platform in results:
            assert platform["airframe_type"] == "Fixed-wing"

    def test_search_by_status(self, query_service):
        """Test searching by development status."""
        results = query_service.search_platforms(
            development_status="Flight testing"
        )

        assert len(results) >= 2

        # All should be in flight testing
        for platform in results:
            assert platform["status"] == "Flight testing"

    def test_search_by_mission_type(self, query_service):
        """Test searching by mission capability."""
        results = query_service.search_platforms(mission_type="ISR")

        assert len(results) >= 4

        # All should support ISR
        for platform in results:
            assert platform["mission_type"] == "ISR"

    def test_search_combined_filters(self, query_service):
        """Test searching with multiple filters."""
        results = query_service.search_platforms(
            airframe_type="Fixed-wing",
            development_status="Flight testing",
            mission_type="ISR",
        )

        assert len(results) >= 1

        # All should match all criteria
        for platform in results:
            assert platform["airframe_type"] == "Fixed-wing"
            assert platform["status"] == "Flight testing"
            assert platform["mission_type"] == "ISR"

    def test_search_no_filters(self, query_service):
        """Test searching without filters."""
        results = query_service.search_platforms()

        assert len(results) >= 7  # Should return all variants


class TestEdgeCases:
    """Test edge cases and error handling."""

    def test_empty_results_graceful(self, query_service):
        """Test that empty results are handled gracefully."""
        result = query_service.get_supply_chain("nonexistent-variant")
        assert result == {}

        result = query_service.get_configuration_provenance("nonexistent-config")
        assert result is None

    def test_query_consistency(self, query_service):
        """Test that repeated queries return consistent results."""
        results1 = query_service.get_platform_configurations("fury")
        results2 = query_service.get_platform_configurations("fury")

        assert len(results1) == len(results2)
        assert results1 == results2

    def test_case_sensitive_keys(self, query_service):
        """Test that queries are case-sensitive for keys."""
        results_lower = query_service.get_platform_configurations("fury")
        results_upper = query_service.get_platform_configurations("FURY")

        assert len(results_lower) > 0
        assert len(results_upper) == 0  # Keys are lowercase
