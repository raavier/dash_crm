import React, { createContext, useContext, useState, useCallback, useEffect, type ReactNode } from 'react';
import type {
  DashboardFilters,
  MetricsData,
  ActionPriority,
  PaginatedActions,
  FilterOptions,
} from '../types/dashboard.types';
import { dashboardService } from '../services/dashboardService';

interface DashboardContextType {
  filters: DashboardFilters;
  metrics: MetricsData | null;
  actionPriorities: ActionPriority[];
  openActions: PaginatedActions | null;
  filterOptions: FilterOptions | null;
  isLoading: boolean;
  error: string | null;
  lastUpdated: Date | null;
  updateFilters: (filters: Partial<DashboardFilters>) => void;
  refreshData: () => Promise<void>;
  setPage: (page: number) => void;
}

const DashboardContext = createContext<DashboardContextType | undefined>(undefined);

const getDefaultFilters = (): DashboardFilters => ({
  organization: 'Todas',
  location: 'All',
  verificationType: 'All',
  dateRange: {
    start: new Date('2024-01-01'), // Start from 2024 to include historical data
    end: new Date(new Date().getFullYear(), 11, 31), // End of current year
  },
});

export const DashboardProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
  const [filters, setFilters] = useState<DashboardFilters>(getDefaultFilters());
  const [metrics, setMetrics] = useState<MetricsData | null>(null);
  const [actionPriorities, setActionPriorities] = useState<ActionPriority[]>([]);
  const [openActions, setOpenActions] = useState<PaginatedActions | null>(null);
  const [filterOptions, setFilterOptions] = useState<FilterOptions | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [lastUpdated, setLastUpdated] = useState<Date | null>(null);
  const [currentPage, setCurrentPage] = useState(1);

  const fetchData = useCallback(async () => {
    setIsLoading(true);
    setError(null);

    try {
      const [metricsData, prioritiesData, actionsData, filtersData] = await Promise.all([
        dashboardService.getMetrics(filters),
        dashboardService.getActionPriorities(filters),
        dashboardService.getOpenActions(filters, currentPage),
        filterOptions ? Promise.resolve(filterOptions) : dashboardService.getFilterOptions(),
      ]);

      setMetrics(metricsData);
      setActionPriorities(prioritiesData);
      setOpenActions(actionsData);
      if (!filterOptions) {
        setFilterOptions(filtersData);
      }
      setLastUpdated(new Date());
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Erro ao carregar dados');
      console.error('Error fetching dashboard data:', err);
    } finally {
      setIsLoading(false);
    }
  }, [filters, currentPage, filterOptions]);

  const updateFilters = useCallback((newFilters: Partial<DashboardFilters>) => {
    setFilters((prev) => ({ ...prev, ...newFilters }));
    setCurrentPage(1); // Reset page when filters change
  }, []);

  const refreshData = useCallback(async () => {
    await fetchData();
  }, [fetchData]);

  const setPage = useCallback((page: number) => {
    setCurrentPage(page);
  }, []);

  // Initial data fetch
  useEffect(() => {
    fetchData();
  }, [fetchData]);

  const value: DashboardContextType = {
    filters,
    metrics,
    actionPriorities,
    openActions,
    filterOptions,
    isLoading,
    error,
    lastUpdated,
    updateFilters,
    refreshData,
    setPage,
  };

  return <DashboardContext.Provider value={value}>{children}</DashboardContext.Provider>;
};

export const useDashboard = (): DashboardContextType => {
  const context = useContext(DashboardContext);
  if (!context) {
    throw new Error('useDashboard must be used within a DashboardProvider');
  }
  return context;
};
