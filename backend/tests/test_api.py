"""
Tests for X-UAV API endpoints.

Tests all REST API functionality.
"""

import pytest
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_root():
    """
    Test root endpoint.

    Expected: Returns welcome message with API info
    """
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "version" in data
    assert "X-UAV" in data["message"]


def test_health_check():
    """
    Test health check endpoint.

    Expected: Returns healthy status
    """
    response = client.get("/api/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "version" in data
    assert "database" in data


def test_get_statistics():
    """
    Test statistics endpoint.

    Expected: Returns database statistics
    """
    response = client.get("/api/stats")
    assert response.status_code == 200
    data = response.json()
    assert "total" in data
    assert "by_country" in data
    assert "by_type" in data
    assert "by_status" in data
    assert data["total"] > 0


def test_list_uavs():
    """
    Test list all UAVs endpoint.

    Expected: Returns list of all UAVs
    """
    response = client.get("/api/uavs")
    assert response.status_code == 200
    data = response.json()
    assert "total" in data
    assert "uavs" in data
    assert data["total"] > 0
    assert len(data["uavs"]) == data["total"]


def test_get_uav_existing():
    """
    Test get specific UAV endpoint with existing UAV.

    Expected: Returns UAV details for MQ-9
    """
    response = client.get("/api/uavs/MQ-9")
    assert response.status_code == 200
    data = response.json()
    assert data["designation"] == "MQ-9"
    assert data["name"] == "Reaper"
    assert data["country_of_origin"] == "United States"


def test_get_uav_not_found():
    """
    Test get specific UAV endpoint with non-existent UAV.

    Expected: Returns 404 error
    """
    response = client.get("/api/uavs/NONEXISTENT")
    assert response.status_code == 404
    data = response.json()
    assert "detail" in data


def test_compare_uavs():
    """
    Test compare UAVs endpoint.

    Expected: Returns comparison of multiple UAVs
    """
    response = client.post(
        "/api/uavs/compare",
        json={"designations": ["MQ-9", "RQ-4", "TB2"]}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["total"] >= 2  # At least 2 should exist
    assert "uavs" in data


def test_compare_uavs_empty():
    """
    Test compare UAVs endpoint with empty list.

    Expected: Returns validation error
    """
    response = client.post(
        "/api/uavs/compare",
        json={"designations": []}
    )
    assert response.status_code == 422  # Validation error


def test_search_uavs_by_country():
    """
    Test search UAVs by country.

    Expected: Returns UAVs from United States
    """
    response = client.post(
        "/api/uavs/search",
        json={"country": "United States"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["total"] > 0
    # Verify all results are from USA
    for uav in data["uavs"]:
        assert uav["country_of_origin"] == "United States"


def test_search_uavs_by_type():
    """
    Test search UAVs by type.

    Expected: Returns MALE UAVs
    """
    response = client.post(
        "/api/uavs/search",
        json={"type": "MALE"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["total"] > 0
    # Verify all results contain MALE in type
    for uav in data["uavs"]:
        if uav["type"]:
            assert "MALE" in uav["type"]


def test_search_uavs_no_filters():
    """
    Test search UAVs with no filters.

    Expected: Returns all UAVs
    """
    response = client.post(
        "/api/uavs/search",
        json={}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["total"] > 0


def test_get_countries():
    """
    Test get countries filter endpoint.

    Expected: Returns list of countries
    """
    response = client.get("/api/filters/countries")
    assert response.status_code == 200
    countries = response.json()
    assert isinstance(countries, list)
    assert len(countries) > 0
    assert "United States" in countries


def test_get_types():
    """
    Test get types filter endpoint.

    Expected: Returns list of UAV types
    """
    response = client.get("/api/filters/types")
    assert response.status_code == 200
    types = response.json()
    assert isinstance(types, list)
    assert len(types) > 0
