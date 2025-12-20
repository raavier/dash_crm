import { Box, SimpleGrid, VStack } from '@chakra-ui/react';
import { useDashboard } from '../context/DashboardContext';
import FilterBar from '../components/Dashboard/FilterBar';
import MetricsCards from '../components/Dashboard/MetricsCards';
import ActionPriorityChart from '../components/Dashboard/ActionPriorityChart';
import ActionsTable from '../components/Dashboard/ActionsTable';
import LoadingSpinner from '../components/Common/LoadingSpinner';
import ErrorAlert from '../components/Common/ErrorAlert';

const DashboardPage = () => {
  const { isLoading, error, refreshData } = useDashboard();

  if (error) {
    return (
      <Box p={6}>
        <ErrorAlert
          title="Erro ao carregar dashboard"
          message={error}
          onRetry={refreshData}
        />
      </Box>
    );
  }

  return (
    <VStack spacing={6} align="stretch">
      {/* Filtros */}
      <FilterBar />

      {isLoading ? (
        <LoadingSpinner message="Carregando dados do dashboard..." />
      ) : (
        <>
          {/* Cards de métricas */}
          <MetricsCards />

          {/* Gráfico e Tabela lado a lado */}
          <SimpleGrid columns={{ base: 1, xl: 2 }} spacing={6}>
            <ActionPriorityChart />
            <Box>
              <ActionsTable />
            </Box>
          </SimpleGrid>
        </>
      )}
    </VStack>
  );
};

export default DashboardPage;
