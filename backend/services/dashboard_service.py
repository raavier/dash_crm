"""
Dashboard service with business logic and SQL queries.
Implements all queries from docs/DATABASE_SCHEMA.md
"""
from typing import List, Dict, Any
from datetime import date
from database import db
from models.dashboard import (
    DashboardFilters,
    MetricsData,
    MetricCard,
    ActionPriority,
    Action,
    PaginatedActions,
    FilterOptions,
    FilterOption
)
from cache import cached
import logging

logger = logging.getLogger(__name__)


class DashboardService:
    """Business logic for dashboard queries."""

    def __init__(self):
        self.catalog = "hs_franquia"
        self.schema = "gold_connect_bot"

    def _build_where_clause(self, filters: DashboardFilters) -> tuple[str, Dict[str, Any]]:
        """
        Build WHERE clause and parameters from filters.

        Returns:
            Tuple of (where_clause_string, parameters_dict)
        """
        conditions = []
        params = {}

        # Date range (required)
        conditions.append("v.VERIFICATION_DATE BETWEEN :start_date AND :end_date")
        params['start_date'] = filters.dateRange.start.isoformat()
        params['end_date'] = filters.dateRange.end.isoformat()

        # Organization filter
        if filters.organization:
            conditions.append("org.uo_level_03 = :organization")
            params['organization'] = filters.organization

        # Location filter
        if filters.location:
            conditions.append("loc.H_01 = :location")
            params['location'] = filters.location

        # Verification type filter
        if filters.verificationType:
            conditions.append("v.TYPE = :verification_type")
            params['verification_type'] = filters.verificationType

        where_clause = " AND ".join(conditions)
        return where_clause, params

    @cached
    def get_metrics(self, filters: DashboardFilters) -> MetricsData:
        """
        Get main metrics: verifications, controls, and questions with non-compliance percentages.

        Uses materialized table crm_metrics_daily for better performance.

        Args:
            filters: Dashboard filters

        Returns:
            MetricsData with three metric cards
        """
        # Build WHERE clause for materialized table
        conditions = []
        params = {}

        # Date range (required) - query on pre-aggregated data
        conditions.append("data_referencia BETWEEN :start_date AND :end_date")
        params['start_date'] = filters.dateRange.start.isoformat()
        params['end_date'] = filters.dateRange.end.isoformat()

        # Organization filter
        if filters.organization:
            conditions.append("organizacao = :organization")
            params['organization'] = filters.organization

        # Location filter
        if filters.location:
            conditions.append("localizacao = :location")
            params['location'] = filters.location

        # Verification type filter
        if filters.verificationType:
            conditions.append("tipo_verificacao = :verification_type")
            params['verification_type'] = filters.verificationType

        where_clause = " AND ".join(conditions)

        # Query materialized table (simple SUM aggregations)
        query = f"""
        SELECT
          SUM(total_verificacoes) as total_verificacoes,
          SUM(verificacoes_nao_conformes) as verificacoes_nao_conformes,
          SUM(total_controles) as total_controles,
          SUM(controles_nao_conformes) as controles_nao_conformes,
          SUM(total_perguntas) as total_perguntas,
          SUM(perguntas_nao_conformes) as perguntas_nao_conformes
        FROM {self.catalog}.{self.schema}.crm_metrics_daily
        WHERE {where_clause}
        """

        # Execute single query on pre-aggregated data
        result = db.execute_query_single(query, params)

        # Calculate percentages
        def calc_percentage(non_compliant: int, total: int) -> float:
            if total == 0:
                return 0.0
            return round((non_compliant * 100.0) / total, 2)

        verif_total = result['total_verificacoes'] or 0
        verif_nc = result['verificacoes_nao_conformes'] or 0

        controls_total = result['total_controles'] or 0
        controls_nc = result['controles_nao_conformes'] or 0

        questions_total = result['total_perguntas'] or 0
        questions_nc = result['perguntas_nao_conformes'] or 0

        return MetricsData(
            verifications=MetricCard(
                total=verif_total,
                nonCompliant=verif_nc,
                percentage=calc_percentage(verif_nc, verif_total)
            ),
            controls=MetricCard(
                total=controls_total,
                nonCompliant=controls_nc,
                percentage=calc_percentage(controls_nc, controls_total)
            ),
            questions=MetricCard(
                total=questions_total,
                nonCompliant=questions_nc,
                percentage=calc_percentage(questions_nc, questions_total)
            )
        )

    @cached
    def get_action_priorities(self, filters: DashboardFilters) -> List[ActionPriority]:
        """
        Get action priority distribution (overdue, S=0 to S=4, later).

        Uses materialized table crm_action_priorities_daily for better performance.

        Args:
            filters: Dashboard filters

        Returns:
            List of ActionPriority objects
        """
        # Build WHERE clause for materialized table
        conditions = ["data_referencia = CURRENT_DATE()"]  # Latest snapshot
        params = {}

        # Organization filter
        if filters.organization:
            conditions.append("organizacao = :organization")
            params['organization'] = filters.organization

        # Location filter
        if filters.location:
            conditions.append("localizacao = :location")
            params['location'] = filters.location

        # Verification type filter
        if filters.verificationType:
            conditions.append("tipo_verificacao = :verification_type")
            params['verification_type'] = filters.verificationType

        where_clause = " AND ".join(conditions)

        # Query materialized table (simple SUM aggregation)
        query = f"""
        SELECT
          categoria_prioridade,
          SUM(total_acoes) as total_acoes
        FROM {self.catalog}.{self.schema}.crm_action_priorities_daily
        WHERE {where_clause}
        GROUP BY categoria_prioridade
        ORDER BY
          CASE categoria_prioridade
            WHEN 'Vencidas' THEN 0
            WHEN 'S=0' THEN 1
            WHEN 'S=1' THEN 2
            WHEN 'S=2' THEN 3
            WHEN 'S=3' THEN 4
            WHEN 'S=4' THEN 5
            WHEN 'Posterior a S=4' THEN 6
            ELSE 7
          END
        """

        results = db.execute_query(query, params)

        # Color mapping
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

        return [
            ActionPriority(
                category=row['categoria_prioridade'],
                count=row['total_acoes'],
                color=color_map.get(row['categoria_prioridade'], '#666666')
            )
            for row in results
        ]

    @cached
    def get_actions(self, filters: DashboardFilters, page: int = 1, page_size: int = 10) -> PaginatedActions:
        """
        Get paginated list of open actions.

        Uses materialized table crm_actions_open_snapshot for better performance.

        Args:
            filters: Dashboard filters
            page: Page number (1-indexed)
            page_size: Number of items per page

        Returns:
            PaginatedActions with data, total count, and pagination info
        """
        # Build WHERE clause for materialized table
        conditions = ["data_snapshot = CURRENT_DATE()"]  # Latest snapshot
        params = {}

        # Organization filter
        if filters.organization:
            conditions.append("organizacao = :organization")
            params['organization'] = filters.organization

        # Location filter
        if filters.location:
            conditions.append("localizacao = :location")
            params['location'] = filters.location

        # Verification type filter
        if filters.verificationType:
            conditions.append("tipo_verificacao = :verification_type")
            params['verification_type'] = filters.verificationType

        where_clause = " AND ".join(conditions)

        # Add pagination parameters
        params['limit'] = page_size
        params['offset'] = (page - 1) * page_size

        # Query materialized snapshot table with window function for count
        data_query = f"""
        SELECT
          id_acao,
          id_verificacao,
          responsavel,
          data_vencimento_acao,
          status_acao,
          tipo,
          COUNT(*) OVER() as total_count
        FROM {self.catalog}.{self.schema}.crm_actions_open_snapshot
        WHERE {where_clause}
        ORDER BY
          CASE WHEN status_acao = 'Atrasado' THEN 0 ELSE 1 END,
          data_vencimento_acao ASC
        LIMIT :limit OFFSET :offset
        """

        # Execute single query on pre-computed snapshot
        data_results = db.execute_query(data_query, params)

        # Extract total from first row (window function returns same count for all rows)
        total = data_results[0]['total_count'] if data_results else 0

        # Convert to Action models
        actions = [
            Action(
                id=row['id_acao'],
                verificationId=row['id_verificacao'],
                responsible=row['responsavel'],
                dueDate=row['data_vencimento_acao'],
                status=row['status_acao'],
                type=row['tipo']
            )
            for row in data_results
        ]

        return PaginatedActions(
            data=actions,
            total=total,
            page=page,
            pageSize=page_size
        )

    @cached
    def get_filter_options(self) -> FilterOptions:
        """
        Get available filter options (organizations, locations, verification types).

        Returns:
            FilterOptions with lists of available values
        """
        # Single combined query with UNION ALL
        combined_query = f"""
        SELECT 'organization' as filter_type, org.uo_level_03 as value
        FROM {self.catalog}.{self.schema}.vw_general_de_para_hier_org_unit org
        WHERE org.uo_level_03 IS NOT NULL
        GROUP BY org.uo_level_03

        UNION ALL

        SELECT 'location' as filter_type, loc.H_01 as value
        FROM {self.catalog}.{self.schema}.vw_crm_location loc
        WHERE loc.H_01 IS NOT NULL
        GROUP BY loc.H_01

        UNION ALL

        SELECT 'verification_type' as filter_type, v.TYPE as value
        FROM {self.catalog}.{self.schema}.vw_crm_verification v
        WHERE v.TYPE IS NOT NULL
        GROUP BY v.TYPE

        ORDER BY filter_type, value
        """

        # Execute single query
        results = db.execute_query(combined_query)

        # Separate results by filter type
        orgs = []
        locs = []
        types = []

        for row in results:
            filter_option = FilterOption(value=row['value'], label=row['value'])
            if row['filter_type'] == 'organization':
                orgs.append(filter_option)
            elif row['filter_type'] == 'location':
                locs.append(filter_option)
            elif row['filter_type'] == 'verification_type':
                types.append(filter_option)

        return FilterOptions(
            organizations=orgs,
            locations=locs,
            verificationTypes=types
        )


# Global service instance
dashboard_service = DashboardService()
