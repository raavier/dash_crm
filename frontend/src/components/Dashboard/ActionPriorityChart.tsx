import { Box, Heading } from '@chakra-ui/react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Cell } from 'recharts';
import { useDashboard } from '../../context/DashboardContext';

const ActionPriorityChart = () => {
  const { actionPriorities } = useDashboard();

  if (!actionPriorities || actionPriorities.length === 0) return null;

  // Preparar dados para o gráfico
  const chartData = actionPriorities.map((item) => ({
    name: item.category,
    value: item.count,
    color: item.color,
  }));

  return (
    <Box bg="white" borderRadius="lg" boxShadow="md" p={6}>
      <Heading as="h3" size="md" mb={6} color="vale.foreground">
        CRM - Priorização de ações
      </Heading>

      <ResponsiveContainer width="100%" height={400}>
        <BarChart
          data={chartData}
          layout="vertical"
          margin={{ top: 5, right: 30, left: 20, bottom: 5 }}
        >
          <CartesianGrid strokeDasharray="3 3" stroke="#E2E8F0" />
          <XAxis type="number" stroke="#718096" />
          <YAxis
            dataKey="name"
            type="category"
            stroke="#718096"
            width={120}
          />
          <Tooltip
            contentStyle={{
              backgroundColor: '#FFFFFF',
              border: '1px solid #E2E8F0',
              borderRadius: '8px',
              padding: '12px',
            }}
            formatter={(value: number | undefined) => [`${value ?? 0} ações`, 'Total']}
          />
          <Bar dataKey="value" radius={[0, 8, 8, 0]}>
            {chartData.map((entry, index) => (
              <Cell key={`cell-${index}`} fill={entry.color} />
            ))}
          </Bar>
        </BarChart>
      </ResponsiveContainer>
    </Box>
  );
};

export default ActionPriorityChart;
