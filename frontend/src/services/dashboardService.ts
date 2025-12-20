import api from './api';
import type {
  DashboardFilters,
  MetricsData,
  ActionPriority,
  PaginatedActions,
  FilterOptions,
} from '../types/dashboard.types';

// Helper para transformar DashboardFilters → backend format
const transformFilters = (filters: DashboardFilters) => ({
  organization: filters.organization === 'Todas' || filters.organization === 'All'
    ? null
    : filters.organization,
  location: filters.location === 'All'
    ? null
    : filters.location,
  verificationType: filters.verificationType === 'All'
    ? null
    : filters.verificationType,
  dateRange: {
    start: filters.dateRange.start.toISOString().split('T')[0], // YYYY-MM-DD
    end: filters.dateRange.end.toISOString().split('T')[0],
  },
});

export const dashboardService = {
  async getMetrics(filters: DashboardFilters): Promise<MetricsData> {
    const response = await api.post('/api/metrics', transformFilters(filters));
    return response.data;
  },

  async getActionPriorities(filters: DashboardFilters): Promise<ActionPriority[]> {
    const response = await api.post('/api/action-priorities', transformFilters(filters));
    return response.data;
  },

  async getOpenActions(filters: DashboardFilters, page: number = 1): Promise<PaginatedActions> {
    const response = await api.post(`/api/actions?page=${page}&page_size=10`, transformFilters(filters));
    return response.data;
  },

  async getFilterOptions(): Promise<FilterOptions> {
    const response = await api.get('/api/filter-options');

    // Transform backend format to frontend format
    const data = response.data;
    return {
      organizations: ['Todas', ...data.organizations.map((o: any) => o.label)],
      locations: ['All', ...data.locations.map((l: any) => l.label)],
      verificationTypes: ['All', ...data.verificationTypes.map((t: any) => t.label)],
    };
  },
};
