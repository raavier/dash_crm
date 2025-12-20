export interface MetricCard {
  total: number;
  nonCompliant: number;
  percentage: number;
}

export interface MetricsData {
  verifications: MetricCard;
  controls: MetricCard;
  questions: MetricCard;
}

export interface ActionPriority {
  category: 'S=0' | 'S=1' | 'S=2' | 'S=3' | 'S=4' | 'Posterior a S=4' | 'Vencidas';
  count: number;
  color: string;
}

export interface Action {
  id: string;
  verificationId: string;
  responsible: string;
  dueDate: string;
  status: 'Atrasado' | 'Em Andamento';
  type: string;
}

export interface PaginatedActions {
  data: Action[];
  total: number;
  page: number;
  pageSize: number;
}

export interface DashboardFilters {
  organization?: string;
  location?: string;
  verificationType?: string;
  dateRange: {
    start: Date;
    end: Date;
  };
}

export interface FilterOptions {
  organizations: string[];
  locations: string[];
  verificationTypes: string[];
}

export interface DashboardData {
  metrics: MetricsData;
  actionPriorities: ActionPriority[];
  openActions: PaginatedActions;
}
