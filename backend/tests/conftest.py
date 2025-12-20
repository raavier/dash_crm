"""
Pytest configuration and fixtures for Dashboard CRM API tests.
"""
import pytest
from datetime import date
from models.dashboard import DashboardFilters, DateRange


@pytest.fixture
def filters_2025():
    """Fixture with filters for year 2025."""
    return DashboardFilters(
        organization=None,
        location=None,
        verificationType=None,
        dateRange=DateRange(
            start=date(2025, 1, 1),
            end=date(2025, 12, 31)
        )
    )


@pytest.fixture
def filters_2024():
    """Fixture with filters for year 2024."""
    return DashboardFilters(
        organization=None,
        location=None,
        verificationType=None,
        dateRange=DateRange(
            start=date(2024, 1, 1),
            end=date(2024, 12, 31)
        )
    )


@pytest.fixture
def expected_verifications_2025():
    """Expected total verifications for 2025."""
    return 316414
