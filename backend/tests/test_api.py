"""
API endpoint tests.
Tests the FastAPI endpoints using httpx test client.
"""
import pytest
from fastapi.testclient import TestClient
from main import app


@pytest.fixture
def client():
    """FastAPI test client."""
    return TestClient(app)


class TestHealthEndpoint:
    """Tests for health check endpoint."""

    def test_health_check(self, client):
        """Test /api/health endpoint."""
        response = client.get("/api/health")

        assert response.status_code == 200
        data = response.json()

        assert data["status"] == "ok"
        assert data["service"] == "Dashboard CRM API"

        print("✓ Health check endpoint working")


class TestRootEndpoint:
    """Tests for root endpoint."""

    def test_root(self, client):
        """Test / endpoint."""
        response = client.get("/")

        assert response.status_code == 200
        data = response.json()

        assert data["service"] == "Dashboard CRM API"
        assert data["version"] == "1.0.0"
        assert data["status"] == "running"

        print("✓ Root endpoint working")


class TestMetricsEndpoint:
    """Tests for /api/metrics endpoint."""

    def test_metrics_endpoint_2025(self, client, expected_verifications_2025):
        """
        Test POST /api/metrics with 2025 filters.

        Validates:
        - Returns 200 status
        - Data structure matches MetricsData model
        - Total verifications = 316414
        """
        payload = {
            "organization": None,
            "location": None,
            "verificationType": None,
            "dateRange": {
                "start": "2025-01-01",
                "end": "2025-12-31"
            }
        }

        response = client.post("/api/metrics", json=payload)

        assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.text}"

        data = response.json()

        # Validate structure
        assert "verifications" in data
        assert "controls" in data
        assert "questions" in data

        # Validate verifications
        assert data["verifications"]["total"] == expected_verifications_2025, (
            f"Expected {expected_verifications_2025} total verifications, "
            f"got {data['verifications']['total']}"
        )
        assert "nonCompliant" in data["verifications"]
        assert "percentage" in data["verifications"]

        # Validate controls
        assert data["controls"]["total"] > 0
        assert "nonCompliant" in data["controls"]
        assert "percentage" in data["controls"]

        # Validate questions
        assert data["questions"]["total"] > 0
        assert "nonCompliant" in data["questions"]
        assert "percentage" in data["questions"]

        print(f"\n✓ POST /api/metrics (2025):")
        print(f"  Verifications: {data['verifications']['total']} total, "
              f"{data['verifications']['percentage']}% non-compliant")
        print(f"  Controls: {data['controls']['total']} total, "
              f"{data['controls']['percentage']}% non-compliant")

    def test_metrics_endpoint_with_filters(self, client):
        """
        Test POST /api/metrics with organization filter.

        Validates that filters are applied correctly.
        """
        payload = {
            "organization": "Some Organization",  # This might not exist, but should not error
            "location": None,
            "verificationType": None,
            "dateRange": {
                "start": "2025-01-01",
                "end": "2025-12-31"
            }
        }

        response = client.post("/api/metrics", json=payload)

        # Should return 200 even if no data matches
        assert response.status_code == 200

        print("✓ POST /api/metrics with filters working")

    def test_metrics_endpoint_invalid_date(self, client):
        """
        Test POST /api/metrics with invalid date format.

        Should return validation error.
        """
        payload = {
            "organization": None,
            "location": None,
            "verificationType": None,
            "dateRange": {
                "start": "invalid-date",
                "end": "2025-12-31"
            }
        }

        response = client.post("/api/metrics", json=payload)

        # Should return 422 for validation error
        assert response.status_code == 422

        print("✓ POST /api/metrics validates date format")


class TestActionPrioritiesEndpoint:
    """Tests for /api/action-priorities endpoint."""

    def test_action_priorities_endpoint_2025(self, client):
        """
        Test POST /api/action-priorities with 2025 filters.

        Validates:
        - Returns 200 status
        - Returns list of priorities with category, count, and color
        """
        payload = {
            "organization": None,
            "location": None,
            "verificationType": None,
            "dateRange": {
                "start": "2025-01-01",
                "end": "2025-12-31"
            }
        }

        response = client.post("/api/action-priorities", json=payload)

        assert response.status_code == 200

        data = response.json()

        # Validate structure
        assert isinstance(data, list), "Response should be a list"
        assert len(data) > 0, "Should return at least one priority"

        # Validate first item
        first = data[0]
        assert "category" in first
        assert "count" in first
        assert "color" in first
        assert first["color"].startswith("#")

        print(f"\n✓ POST /api/action-priorities (2025):")
        for item in data:
            print(f"  {item['category']}: {item['count']} actions")


class TestActionsEndpoint:
    """Tests for /api/actions endpoint."""

    def test_actions_endpoint_default_pagination(self, client):
        """
        Test POST /api/actions with default pagination.

        Validates:
        - Returns 200 status
        - Default pagination is page=1, pageSize=10
        """
        payload = {
            "organization": None,
            "location": None,
            "verificationType": None,
            "dateRange": {
                "start": "2025-01-01",
                "end": "2025-12-31"
            }
        }

        response = client.post("/api/actions", json=payload)

        assert response.status_code == 200

        data = response.json()

        # Validate structure
        assert "data" in data
        assert "total" in data
        assert "page" in data
        assert "pageSize" in data

        # Validate pagination
        assert data["page"] == 1
        assert data["pageSize"] == 10
        assert isinstance(data["data"], list)
        assert len(data["data"]) <= 10

        if data["data"]:
            first_action = data["data"][0]
            assert "id" in first_action
            assert "verificationId" in first_action
            assert "status" in first_action
            assert "dueDate" in first_action

        print(f"\n✓ POST /api/actions (default pagination):")
        print(f"  Total: {data['total']} actions")
        print(f"  Returned: {len(data['data'])} items")

    def test_actions_endpoint_custom_pagination(self, client):
        """
        Test POST /api/actions with custom pagination parameters.

        Validates query parameters work correctly.
        """
        payload = {
            "organization": None,
            "location": None,
            "verificationType": None,
            "dateRange": {
                "start": "2025-01-01",
                "end": "2025-12-31"
            }
        }

        response = client.post("/api/actions?page=2&page_size=5", json=payload)

        assert response.status_code == 200

        data = response.json()

        assert data["page"] == 2
        assert data["pageSize"] == 5
        assert len(data["data"]) <= 5

        print(f"\n✓ POST /api/actions (page=2, page_size=5):")
        print(f"  Total: {data['total']} actions")
        print(f"  Returned: {len(data['data'])} items")

    def test_actions_endpoint_invalid_page(self, client):
        """
        Test POST /api/actions with invalid page parameter.

        Should return validation error for page < 1.
        """
        payload = {
            "organization": None,
            "location": None,
            "verificationType": None,
            "dateRange": {
                "start": "2025-01-01",
                "end": "2025-12-31"
            }
        }

        response = client.post("/api/actions?page=0", json=payload)

        # Should return 422 for validation error
        assert response.status_code == 422

        print("✓ POST /api/actions validates page >= 1")


class TestFilterOptionsEndpoint:
    """Tests for /api/filter-options endpoint."""

    def test_filter_options_endpoint(self, client):
        """
        Test GET /api/filter-options.

        Validates:
        - Returns 200 status
        - Returns organizations, locations, and verification types
        """
        response = client.get("/api/filter-options")

        assert response.status_code == 200

        data = response.json()

        # Validate structure
        assert "organizations" in data
        assert "locations" in data
        assert "verificationTypes" in data

        # Validate data
        assert isinstance(data["organizations"], list)
        assert isinstance(data["locations"], list)
        assert isinstance(data["verificationTypes"], list)

        assert len(data["organizations"]) > 0
        assert len(data["locations"]) > 0
        assert len(data["verificationTypes"]) > 0

        # Validate first item structure
        if data["organizations"]:
            first_org = data["organizations"][0]
            assert "value" in first_org
            assert "label" in first_org

        print(f"\n✓ GET /api/filter-options:")
        print(f"  Organizations: {len(data['organizations'])} options")
        print(f"  Locations: {len(data['locations'])} options")
        print(f"  Verification types: {len(data['verificationTypes'])} options")
