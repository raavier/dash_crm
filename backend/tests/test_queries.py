"""
Direct database query tests.
Tests SQL queries against Databricks to validate data accuracy.
"""
import pytest
from datetime import date
from database import db
from config import settings


class TestVerificationsQuery:
    """Tests for verifications count queries."""

    def test_total_verifications_2025(self, filters_2025, expected_verifications_2025):
        """
        Test that total verifications in 2025 equals 316414.

        This is a baseline test to ensure the query is correctly counting
        all verifications in the specified date range.
        """
        query = f"""
        SELECT COUNT(DISTINCT v.ID) as total_verificacoes
        FROM {settings.catalog}.{settings.schema_gold}.vw_crm_verification v
        WHERE v.VERIFICATION_DATE BETWEEN :start_date AND :end_date
        """

        params = {
            'start_date': filters_2025.dateRange.start.isoformat(),
            'end_date': filters_2025.dateRange.end.isoformat()
        }

        result = db.execute_query_single(query, params)

        assert result is not None, "Query returned no results"
        assert 'total_verificacoes' in result, "Missing 'total_verificacoes' in result"

        total = result['total_verificacoes']

        # Check if the total matches expected value
        assert total == expected_verifications_2025, (
            f"Expected {expected_verifications_2025} verifications in 2025, "
            f"but got {total}"
        )

        print(f"✓ Total verifications in 2025: {total}")

    def test_verifications_with_non_compliance_2025(self, filters_2025):
        """
        Test verifications with non-compliance count for 2025.

        Validates that the query correctly identifies verifications
        that have at least one non-compliant question.
        """
        query = f"""
        SELECT
          COUNT(DISTINCT v.ID) as total_verificacoes,
          COUNT(DISTINCT CASE WHEN q.CRITICAL_CONTROL_NON_COMPLIANCE = 1 THEN v.ID END) as verificacoes_nao_conformes
        FROM {settings.catalog}.{settings.schema_gold}.vw_crm_verification v
        LEFT JOIN {settings.catalog}.{settings.schema_gold}.vw_crm_verification_question q
          ON v.ID = q.VERIFICATION_ID
        WHERE v.VERIFICATION_DATE BETWEEN :start_date AND :end_date
        """

        params = {
            'start_date': filters_2025.dateRange.start.isoformat(),
            'end_date': filters_2025.dateRange.end.isoformat()
        }

        result = db.execute_query_single(query, params)

        assert result is not None, "Query returned no results"

        total = result['total_verificacoes']
        non_compliant = result['verificacoes_nao_conformes']

        # Basic validation
        assert total > 0, "Total verifications should be greater than 0"
        assert non_compliant >= 0, "Non-compliant verifications should be >= 0"
        assert non_compliant <= total, "Non-compliant count cannot exceed total"

        # Calculate percentage
        percentage = round((non_compliant * 100.0) / total, 2) if total > 0 else 0

        print(f"✓ Total verifications: {total}")
        print(f"✓ Non-compliant verifications: {non_compliant}")
        print(f"✓ Non-compliance percentage: {percentage}%")


class TestControlsQuery:
    """Tests for controls count queries."""

    def test_total_controls_2025(self, filters_2025):
        """
        Test total controls (questions) count for 2025.

        Each verification has multiple questions/controls.
        This test validates the total count of control checks.
        """
        query = f"""
        SELECT
          COUNT(DISTINCT q.DB_KEY) as total_controles,
          SUM(CASE WHEN q.CRITICAL_CONTROL_NON_COMPLIANCE = 1 THEN 1 ELSE 0 END) as controles_nao_conformes
        FROM {settings.catalog}.{settings.schema_gold}.vw_crm_verification_question q
        JOIN {settings.catalog}.{settings.schema_gold}.vw_crm_verification v
          ON q.VERIFICATION_ID = v.ID
        WHERE v.VERIFICATION_DATE BETWEEN :start_date AND :end_date
        """

        params = {
            'start_date': filters_2025.dateRange.start.isoformat(),
            'end_date': filters_2025.dateRange.end.isoformat()
        }

        result = db.execute_query_single(query, params)

        assert result is not None, "Query returned no results"

        total = result['total_controles']
        non_compliant = result['controles_nao_conformes']

        # Validation
        assert total > 0, "Total controls should be greater than 0"
        assert non_compliant >= 0, "Non-compliant controls should be >= 0"
        assert non_compliant <= total, "Non-compliant count cannot exceed total"

        # Calculate percentage
        percentage = round((non_compliant * 100.0) / total, 2) if total > 0 else 0

        print(f"✓ Total controls: {total}")
        print(f"✓ Non-compliant controls: {non_compliant}")
        print(f"✓ Non-compliance percentage: {percentage}%")


class TestActionsQuery:
    """Tests for actions queries."""

    def test_open_actions_count(self, filters_2025):
        """
        Test count of open actions (not completed) for 2025.

        Open actions are those where COMPLETED_DATE IS NULL.
        """
        query = f"""
        SELECT COUNT(*) as total_acoes_abertas
        FROM {settings.catalog}.{settings.schema_gold}.vw_crm_action a
        JOIN {settings.catalog}.{settings.schema_gold}.vw_crm_verification v
          ON a.VERIFICATION_ID = v.ID
        WHERE a.COMPLETED_DATE IS NULL
          AND v.VERIFICATION_DATE BETWEEN :start_date AND :end_date
        """

        params = {
            'start_date': filters_2025.dateRange.start.isoformat(),
            'end_date': filters_2025.dateRange.end.isoformat()
        }

        result = db.execute_query_single(query, params)

        assert result is not None, "Query returned no results"

        total_open = result['total_acoes_abertas']

        assert total_open >= 0, "Total open actions should be >= 0"

        print(f"✓ Total open actions: {total_open}")

    def test_action_priorities_distribution(self, filters_2025):
        """
        Test action priorities distribution (Vencidas, S=0 to S=4, etc.).

        Validates the categorization of actions by priority.
        """
        query = f"""
        SELECT
          CASE
            WHEN a.END_DATE < CURRENT_DATE AND a.COMPLETED_DATE IS NULL THEN 'Vencidas'
            WHEN a.PRIORITY = 0 THEN 'S=0'
            WHEN a.PRIORITY = 1 THEN 'S=1'
            WHEN a.PRIORITY = 2 THEN 'S=2'
            WHEN a.PRIORITY = 3 THEN 'S=3'
            WHEN a.PRIORITY = 4 THEN 'S=4'
            WHEN a.PRIORITY > 4 THEN 'Posterior a S=4'
            ELSE 'Outros'
          END as categoria_prioridade,
          COUNT(*) as total_acoes
        FROM {settings.catalog}.{settings.schema_gold}.vw_crm_action a
        JOIN {settings.catalog}.{settings.schema_gold}.vw_crm_verification v
          ON a.VERIFICATION_ID = v.ID
        WHERE a.COMPLETED_DATE IS NULL
          AND v.VERIFICATION_DATE BETWEEN :start_date AND :end_date
        GROUP BY
          CASE
            WHEN a.END_DATE < CURRENT_DATE AND a.COMPLETED_DATE IS NULL THEN 'Vencidas'
            WHEN a.PRIORITY = 0 THEN 'S=0'
            WHEN a.PRIORITY = 1 THEN 'S=1'
            WHEN a.PRIORITY = 2 THEN 'S=2'
            WHEN a.PRIORITY = 3 THEN 'S=3'
            WHEN a.PRIORITY = 4 THEN 'S=4'
            WHEN a.PRIORITY > 4 THEN 'Posterior a S=4'
            ELSE 'Outros'
          END
        """

        params = {
            'start_date': filters_2025.dateRange.start.isoformat(),
            'end_date': filters_2025.dateRange.end.isoformat()
        }

        results = db.execute_query(query, params)

        assert results is not None, "Query returned no results"
        assert len(results) > 0, "No priority categories found"

        # Validate structure
        for row in results:
            assert 'categoria_prioridade' in row
            assert 'total_acoes' in row
            assert row['total_acoes'] > 0, f"Category {row['categoria_prioridade']} has 0 actions"

        print(f"✓ Action priority distribution:")
        for row in results:
            print(f"  - {row['categoria_prioridade']}: {row['total_acoes']} actions")

    def test_actions_with_responsible(self, filters_2025):
        """
        Test that actions can be joined with user information.

        Validates the relationship between actions and responsible users.
        """
        query = f"""
        SELECT
          a.ID as id_acao,
          a.VERIFICATION_ID as id_verificacao,
          u.FULL_NAME as responsavel,
          a.END_DATE as data_vencimento_acao,
          CASE
            WHEN a.END_DATE < CURRENT_DATE THEN 'Atrasado'
            ELSE 'Em Andamento'
          END as status_acao,
          a.TYPE as tipo
        FROM {settings.catalog}.{settings.schema_gold}.vw_crm_action a
        JOIN {settings.catalog}.{settings.schema_gold}.vw_crm_verification v
          ON a.VERIFICATION_ID = v.ID
        LEFT JOIN {settings.catalog}.{settings.schema_gold}.vw_crm_user u
          ON a.RESPONSIBLE_PERSON_ID = u.USER_ID
        WHERE a.COMPLETED_DATE IS NULL
          AND v.VERIFICATION_DATE BETWEEN :start_date AND :end_date
        LIMIT 10
        """

        params = {
            'start_date': filters_2025.dateRange.start.isoformat(),
            'end_date': filters_2025.dateRange.end.isoformat()
        }

        results = db.execute_query(query, params)

        assert results is not None, "Query returned no results"
        assert len(results) > 0, "No actions found with responsible users"

        # Validate structure
        for row in results:
            assert 'id_acao' in row
            assert 'id_verificacao' in row
            assert 'status_acao' in row
            assert row['status_acao'] in ['Atrasado', 'Em Andamento']

        print(f"✓ Sample of {len(results)} actions with responsible users")
        print(f"  First action ID: {results[0]['id_acao']}")
        print(f"  Responsible: {results[0]['responsavel'] or 'N/A'}")
