"""
Dashboard API routes.
Exposes REST endpoints for the frontend.
"""
from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from models.dashboard import (
    DashboardFilters,
    MetricsData,
    ActionPriority,
    PaginatedActions,
    FilterOptions
)
from services.dashboard_service import dashboard_service
from cache import clear_all_cache, get_cache_stats, invalidate_cache_pattern
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api", tags=["dashboard"])


@router.post("/metrics", response_model=MetricsData)
async def get_metrics(filters: DashboardFilters):
    """
    Get main metrics: verifications, controls, and questions with non-compliance %.

    Args:
        filters: Dashboard filters (organization, location, verificationType, dateRange)

    Returns:
        MetricsData with three metric cards
    """
    try:
        logger.info(f"GET /api/metrics - Filters: {filters}")
        result = dashboard_service.get_metrics(filters)
        return result
    except Exception as e:
        logger.error(f"Error in get_metrics: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error fetching metrics: {str(e)}")


@router.post("/action-priorities", response_model=List[ActionPriority])
async def get_action_priorities(filters: DashboardFilters):
    """
    Get action priority distribution (overdue, S=0 to S=4, later).

    Args:
        filters: Dashboard filters

    Returns:
        List of ActionPriority objects with category, count, and color
    """
    try:
        logger.info(f"GET /api/action-priorities - Filters: {filters}")
        result = dashboard_service.get_action_priorities(filters)
        return result
    except Exception as e:
        logger.error(f"Error in get_action_priorities: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error fetching action priorities: {str(e)}")


@router.post("/actions", response_model=PaginatedActions)
async def get_actions(
    filters: DashboardFilters,
    page: int = Query(1, ge=1, description="Page number (1-indexed)"),
    page_size: int = Query(10, ge=1, le=100, description="Items per page")
):
    """
    Get paginated list of open actions.

    Args:
        filters: Dashboard filters
        page: Page number (default: 1)
        page_size: Items per page (default: 10, max: 100)

    Returns:
        PaginatedActions with data, total count, and pagination info
    """
    try:
        logger.info(f"GET /api/actions - Filters: {filters}, Page: {page}, PageSize: {page_size}")
        result = dashboard_service.get_actions(filters, page, page_size)
        return result
    except Exception as e:
        logger.error(f"Error in get_actions: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error fetching actions: {str(e)}")


@router.get("/filter-options", response_model=FilterOptions)
async def get_filter_options():
    """
    Get available filter options (organizations, locations, verification types).

    Returns:
        FilterOptions with lists of available values
    """
    try:
        logger.info("GET /api/filter-options")
        result = dashboard_service.get_filter_options()
        return result
    except Exception as e:
        logger.error(f"Error in get_filter_options: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error fetching filter options: {str(e)}")


@router.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "ok", "service": "Dashboard CRM API"}


# ============================================================================
# Cache Management Endpoints
# ============================================================================

@router.get("/cache/stats")
async def get_cache_statistics():
    """
    Get cache statistics.

    Returns:
        Cache stats: size, maxsize, TTL, etc.
    """
    try:
        logger.info("GET /api/cache/stats")
        stats = get_cache_stats()
        return {
            "status": "ok",
            "cache": stats
        }
    except Exception as e:
        logger.error(f"Error getting cache stats: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error fetching cache stats: {str(e)}")


@router.post("/cache/clear")
async def clear_cache():
    """
    Clear entire cache.

    ⚠️ WARNING: This will force all subsequent requests to hit the database.

    Returns:
        Success message
    """
    try:
        logger.warning("POST /api/cache/clear - Clearing entire cache")
        clear_all_cache()
        return {
            "status": "success",
            "message": "Cache cleared successfully",
            "warning": "Next requests will hit the database"
        }
    except Exception as e:
        logger.error(f"Error clearing cache: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error clearing cache: {str(e)}")


@router.post("/cache/invalidate")
async def invalidate_cache(
    pattern: Optional[str] = Query(None, description="Pattern to match cache keys (e.g., 'get_metrics')")
):
    """
    Invalidate cache keys matching a pattern.

    Args:
        pattern: String to match in cache keys (e.g., "get_metrics", "get_actions")

    Returns:
        Number of keys invalidated
    """
    try:
        if not pattern:
            raise HTTPException(status_code=400, detail="Pattern parameter is required")

        logger.info(f"POST /api/cache/invalidate - Pattern: {pattern}")
        deleted_count = invalidate_cache_pattern(pattern)

        return {
            "status": "success",
            "pattern": pattern,
            "keys_deleted": deleted_count,
            "message": f"Invalidated {deleted_count} cache keys matching pattern '{pattern}'"
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error invalidating cache: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error invalidating cache: {str(e)}")
