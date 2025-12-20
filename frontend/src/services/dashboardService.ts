import type {
  DashboardFilters,
  MetricsData,
  ActionPriority,
  PaginatedActions,
  FilterOptions,
} from '../types/dashboard.types';

// Mock data baseado na imagem fornecida
const mockMetrics: MetricsData = {
  verifications: { total: 316414, nonCompliant: 63705, percentage: 20.13 },
  controls: { total: 772899, nonCompliant: 70015, percentage: 9.06 },
  questions: { total: 3627949, nonCompliant: 89363, percentage: 2.46 },
};

const mockActionPriorities: ActionPriority[] = [
  { category: 'Vencidas', count: 133, color: '#BB133E' },
  { category: 'S=0', count: 97, color: '#E37222' },
  { category: 'S=1', count: 111, color: '#ECB11F' },
  { category: 'S=2', count: 28, color: '#3D7EDB' },
  { category: 'S=3', count: 34, color: '#00B0CA' },
  { category: 'S=4', count: 18, color: '#69BE28' },
  { category: 'Posterior a S=4', count: 185, color: '#747678' },
];

const mockActions: PaginatedActions = {
  data: [
    {
      id: '2217716',
      verificationId: '2217715',
      responsible: 'Rodrigo Rios',
      dueDate: '2025-05-29',
      status: 'Atrasado',
      type: 'Comportamental',
    },
    {
      id: '2217109',
      verificationId: '2217108',
      responsible: 'Roberto Cardoso',
      dueDate: '2025-06-30',
      status: 'Atrasado',
      type: 'Planta ou Equipamento',
    },
    {
      id: '2206175',
      verificationId: '2200474',
      responsible: 'Sabrina Borges',
      dueDate: '2025-07-25',
      status: 'Atrasado',
      type: 'Sistema ou Processo',
    },
    {
      id: '2268906',
      verificationId: '2268905',
      responsible: 'Paulo Gomide',
      dueDate: '2025-07-30',
      status: 'Atrasado',
      type: 'Sistema ou Processo',
    },
    {
      id: '2268907',
      verificationId: '2268905',
      responsible: 'Paulo Gomide',
      dueDate: '2025-07-30',
      status: 'Atrasado',
      type: 'Sistema ou Processo',
    },
    {
      id: '2271421',
      verificationId: '2271420',
      responsible: 'Paulo Gomide',
      dueDate: '2025-07-31',
      status: 'Em Andamento',
      type: 'Sistema ou Processo',
    },
    {
      id: '2294520',
      verificationId: '2294519',
      responsible: 'Tiashantan Médaid',
      dueDate: '2025-08-20',
      status: 'Em Andamento',
      type: 'Planta ou Equipamento',
    },
  ],
  total: 100,
  page: 1,
  pageSize: 10,
};

const mockFilterOptions: FilterOptions = {
  organizations: ['Vale', 'Vale sem VBM', 'Todas'],
  locations: ['All', 'Tufilândia', 'Santa Inês', 'Vila Nova dos Martírios'],
  verificationTypes: ['All', 'Manager Verification', 'Operator Verification', 'Supervisor Verification'],
};

export const dashboardService = {
  async getMetrics(_filters: DashboardFilters): Promise<MetricsData> {
    // Simula delay de API
    await new Promise((resolve) => setTimeout(resolve, 500));
    return mockMetrics;
  },

  async getActionPriorities(_filters: DashboardFilters): Promise<ActionPriority[]> {
    await new Promise((resolve) => setTimeout(resolve, 500));
    return mockActionPriorities;
  },

  async getOpenActions(_filters: DashboardFilters, _page: number = 1): Promise<PaginatedActions> {
    await new Promise((resolve) => setTimeout(resolve, 500));
    return mockActions;
  },

  async getFilterOptions(): Promise<FilterOptions> {
    await new Promise((resolve) => setTimeout(resolve, 300));
    return mockFilterOptions;
  },
};
