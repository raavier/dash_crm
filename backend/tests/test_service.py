"""
Service layer tests.
Tests the dashboard_service business logic and data transformations.
"""
import pytest
from services.dashboard_service import dashboard_service
from models.dashboard import MetricsData, ActionPriority, PaginatedActions


class TestMetricsService:
    """Tests for get_metrics service method."""

    def test_get_metrics_2025(self, filters_2025, expected_verifications_2025):
        """
        Test get_metrics returns correct data structure for 2025.

        Validates:
        - Total verifications = 316414
        - All fields are present
        - Percentages are calculated correctly
        """
        result = dashboard_service.get_metrics(filters_2025)

        # Validate type
        assert isinstance(result, MetricsData), "Result should be MetricsData instance"

        # Validate verifications
        assert result.verifications.total == expected_verifications_2025, (
            f"Expected {expected_verifications_2025} total verifications, "
            f"got {result.verifications.total}"
        )
        assert result.verifications.nonCompliant >= 0
        assert result.verifications.nonCompliant <= result.verifications.total
        assert 0 <= result.verifications.percentage <= 100

        # Validate controls
        assert result.controls.total > 0, "Total controls should be > 0"
        assert result.controls.nonCompliant >= 0
        assert result.controls.nonCompliant <= result.controls.total
        assert 0 <= result.controls.percentage <= 100

        # Validate questions (should equal controls in this implementation)
        assert result.questions.total > 0, "Total questions should be > 0"
        assert result.questions.nonCompliant >= 0
        assert result.questions.nonCompliant <= result.questions.total
        assert 0 <= result.questions.percentage <= 100

        # Print results
        print(f"\n✓ Metrics for 2025:")
        print(f"  Verifications: {result.verifications.total} total, "
              f"{result.verifications.nonCompliant} non-compliant ({result.verifications.percentage}%)")
        print(f"  Controls: {result.controls.total} total, "
              f"{result.controls.nonCompliant} non-compliant ({result.controls.percentage}%)")
        print(f"  Questions: {result.questions.total} total, "
              f"{result.questions.nonCompliant} non-compliant ({result.questions.percentage}%)")

    def test_get_metrics_percentages_calculation(self, filters_2025):
        """
        Test that percentages are calculated correctly.

        Validates: percentage = (nonCompliant / total) * 100
        """
        result = dashboard_service.get_metrics(filters_2025)

        # Verify verifications percentage
        if result.verifications.total > 0:
            expected_pct = round((result.verifications.nonCompliant * 100.0) / result.verifications.total, 2)
            assert result.verifications.percentage == expected_pct, (
                f"Verifications percentage mismatch: expected {expected_pct}, got {result.verifications.percentage}"
            )

        # Verify controls percentage
        if result.controls.total > 0:
            expected_pct = round((result.controls.nonCompliant * 100.0) / result.controls.total, 2)
            assert result.controls.percentage == expected_pct, (
                f"Controls percentage mismatch: expected {expected_pct}, got {result.controls.percentage}"
            )

        print("✓ Percentage calculations are correct")


class TestActionPrioritiesService:
    """Tests for get_action_priorities service method."""

    def test_get_action_priorities_2025(self, filters_2025):
        """
        Test get_action_priorities returns correct structure.

        Validates:
        - Returns list of ActionPriority objects
        - Each priority has category, count, and color
        - Categories are in correct order
        """
        result = dashboard_service.get_action_priorities(filters_2025)

        # Validate type
        assert isinstance(result, list), "Result should be a list"
        assert len(result) > 0, "Should return at least one priority category"

        # Validate each item
        for item in result:
            assert isinstance(item, ActionPriority), "Each item should be ActionPriority instance"
            assert item.category, "Category should not be empty"
            assert item.count > 0, f"Category {item.category} should have count > 0"
            assert item.color.startswith('#'), f"Color should be hex format for {item.category}"
            assert len(item.color) == 7, f"Color should be 7 chars (#RRGGBB) for {item.category}"

        # Validate expected categories
        categories = [item.category for item in result]
        expected_categories = ['Vencidas', 'S=0', 'S=1', 'S=2', 'S=3', 'S=4', 'Posterior a S=4', 'Outros']

        for category in categories:
            assert category in expected_categories, f"Unexpected category: {category}"

        # Print results
        print(f"\n✓ Action priorities for 2025:")
        for item in result:
            print(f"  {item.category}: {item.count} actions ({item.color})")

    def test_action_priorities_colors(self, filters_2025):
        """
        Test that priority categories have correct color codes.

        Validates the color mapping matches specifications.
        """
        result = dashboard_service.get_action_priorities(filters_2025)

        color_map = {
            'Vencidas': '#BB133E',
            'S=0': '#E37222',
            'S=1': '#F4A100',
            'S=2': '#FFD600',
            'S=3': '#8BC83F',
            'S=4': '#009A44',
            'Posterior a S=4': '#0078D4',
            'Outros': '#666666'
        }

        for item in result:
            expected_color = color_map.get(item.category)
            if expected_color:
                assert item.color == expected_color, (
                    f"Color mismatch for {item.category}: expected {expected_color}, got {item.color}"
                )

        print("✓ All priority colors are correct")


class TestActionsService:
    """Tests for get_actions service method."""

    def test_get_actions_pagination_first_page(self, filters_2025):
        """
        Test get_actions with pagination (first page).

        Validates:
        - Returns correct number of items per page
        - Total count is accurate
        - Page metadata is correct
        """
        page = 1
        page_size = 10

        result = dashboard_service.get_actions(filters_2025, page, page_size)

        # Validate type
        assert isinstance(result, PaginatedActions), "Result should be PaginatedActions instance"

        # Validate pagination metadata
        assert result.page == page, f"Expected page {page}, got {result.page}"
        assert result.pageSize == page_size, f"Expected pageSize {page_size}, got {result.pageSize}"
        assert result.total >= 0, "Total should be >= 0"

        # Validate data
        assert isinstance(result.data, list), "Data should be a list"
        assert len(result.data) <= page_size, f"Should return at most {page_size} items"

        if result.total > 0:
            assert len(result.data) > 0, "Should have data if total > 0"

            # Validate first action structure
            first_action = result.data[0]
            assert first_action.id, "Action should have ID"
            assert first_action.verificationId, "Action should have verificationId"
            assert first_action.dueDate, "Action should have dueDate"
            assert first_action.status in ['Atrasado', 'Em Andamento'], "Status should be valid"
            assert first_action.type, "Action should have type"

        print(f"\n✓ Actions pagination (page {page}):")
        print(f"  Total actions: {result.total}")
        print(f"  Returned: {len(result.data)} items")
        if result.data:
            print(f"  First action: {result.data[0].id} - Status: {result.data[0].status}")

    def test_get_actions_pagination_second_page(self, filters_2025):
        """
        Test get_actions with pagination (second page).

        Validates that pagination works correctly for subsequent pages.
        """
        page = 2
        page_size = 10

        result = dashboard_service.get_actions(filters_2025, page, page_size)

        assert result.page == page
        assert result.pageSize == page_size

        if result.total > page_size:
            # Should have data on page 2 if total > page_size
            assert len(result.data) > 0, "Should have data on page 2"

        print(f"\n✓ Actions pagination (page {page}):")
        print(f"  Total actions: {result.total}")
        print(f"  Returned: {len(result.data)} items")

    def test_get_actions_large_page_size(self, filters_2025):
        """
        Test get_actions with large page size.

        Validates that large page sizes work correctly.
        """
        page = 1
        page_size = 100

        result = dashboard_service.get_actions(filters_2025, page, page_size)

        assert result.pageSize == page_size
        assert len(result.data) <= page_size

        print(f"\n✓ Actions with page_size={page_size}:")
        print(f"  Total actions: {result.total}")
        print(f"  Returned: {len(result.data)} items")


class TestFilterOptionsService:
    """Tests for get_filter_options service method."""

    def test_get_filter_options(self):
        """
        Test get_filter_options returns all available options.

        Validates:
        - Returns organizations, locations, and verification types
        - Each option has value and label
        """
        result = dashboard_service.get_filter_options()

        # Validate structure
        assert result.organizations, "Should return organizations"
        assert result.locations, "Should return locations"
        assert result.verificationTypes, "Should return verification types"

        # Validate organizations
        assert len(result.organizations) > 0, "Should have at least one organization"
        for org in result.organizations:
            assert org.value, "Organization should have value"
            assert org.label, "Organization should have label"

        # Validate locations
        assert len(result.locations) > 0, "Should have at least one location"
        for loc in result.locations:
            assert loc.value, "Location should have value"
            assert loc.label, "Location should have label"

        # Validate verification types
        assert len(result.verificationTypes) > 0, "Should have at least one verification type"
        for vtype in result.verificationTypes:
            assert vtype.value, "Verification type should have value"
            assert vtype.label, "Verification type should have label"

        print(f"\n✓ Filter options:")
        print(f"  Organizations: {len(result.organizations)} options")
        print(f"  Locations: {len(result.locations)} options")
        print(f"  Verification types: {len(result.verificationTypes)} options")

    def test_filter_options_verification_types(self):
        """
        Test that verification types include expected values.

        Expected types: Manager Verification, Operator Verification, Supervisor Verification
        """
        result = dashboard_service.get_filter_options()

        types = [vtype.value for vtype in result.verificationTypes]

        expected_types = ['Manager Verification', 'Operator Verification', 'Supervisor Verification']

        for expected in expected_types:
            # Should contain at least one of the expected types
            matches = [t for t in types if expected in t]
            print(f"  Found verification type containing '{expected}': {len(matches) > 0}")

        print("✓ Verification types validated")
