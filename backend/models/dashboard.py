"""
Pydantic models for Dashboard CRM API.
Matches TypeScript interfaces from frontend/src/types/dashboard.types.ts
"""
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import date, datetime


# Request Models
class DateRange(BaseModel):
    """Date range filter."""
    start: date
    end: date


class DashboardFilters(BaseModel):
    """Filters for dashboard queries."""
    organization: Optional[str] = None
    location: Optional[str] = None
    verificationType: Optional[str] = None
    dateRange: DateRange


# Response Models
class MetricCard(BaseModel):
    """Single metric card data."""
    total: int
    nonCompliant: int
    percentage: float


class MetricsData(BaseModel):
    """Main metrics data (3 cards)."""
    verifications: MetricCard
    controls: MetricCard
    questions: MetricCard


class ActionPriority(BaseModel):
    """Action priority category with count and color."""
    category: str
    count: int
    color: str


class Action(BaseModel):
    """Action item for the table."""
    id: str
    verificationId: str
    responsible: Optional[str] = None
    dueDate: date
    status: str
    type: str


class PaginatedActions(BaseModel):
    """Paginated list of actions."""
    data: List[Action]
    total: int
    page: int
    pageSize: int


class FilterOption(BaseModel):
    """Single filter option."""
    value: str
    label: str


class FilterOptions(BaseModel):
    """Available filter options."""
    organizations: List[FilterOption]
    locations: List[FilterOption]
    verificationTypes: List[FilterOption]
