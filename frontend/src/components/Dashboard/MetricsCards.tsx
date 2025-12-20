import { SimpleGrid, Box, Text, Stat, StatLabel, StatNumber, StatHelpText, Icon, Tooltip } from '@chakra-ui/react';
import { InfoIcon } from '@chakra-ui/icons';
import { useDashboard } from '../../context/DashboardContext';

const MetricsCards = () => {
  const { metrics } = useDashboard();

  if (!metrics) return null;

  const getPercentageColor = (percentage: number): string => {
    if (percentage < 5) return 'vale.success'; // Verde - dados positivos
    if (percentage <= 10) return 'vale.secondary'; // Amarelo - atenção
    return 'vale.danger'; // Vermelho - dados negativos
  };

  const cards = [
    {
      title: 'Total verificações',
      data: metrics.verifications,
      tooltip: 'Total de verificações realizadas e porcentagem de não conformes',
    },
    {
      title: 'Total controles',
      data: metrics.controls,
      tooltip: 'Total de controles avaliados e porcentagem de não conformes',
    },
    {
      title: 'Total perguntas',
      data: metrics.questions,
      tooltip: 'Total de perguntas respondidas e porcentagem de não conformes',
    },
  ];

  return (
    <SimpleGrid columns={{ base: 1, md: 2, lg: 3 }} spacing={6}>
      {cards.map((card, index) => (
        <Box
          key={index}
          bg="white"
          borderRadius="lg"
          boxShadow="md"
          p={6}
          borderTop="4px solid"
          borderTopColor="vale.tableAccent"
          _hover={{ boxShadow: 'lg', transform: 'translateY(-2px)' }}
          transition="all 0.2s"
        >
          <Stat>
            <StatLabel
              display="flex"
              alignItems="center"
              gap={2}
              fontSize="sm"
              fontWeight="semibold"
              color="gray.600"
              mb={2}
            >
              {card.title}
              <Tooltip label={card.tooltip} placement="top">
                <Icon as={InfoIcon} boxSize={3} cursor="help" />
              </Tooltip>
            </StatLabel>

            <StatNumber fontSize="4xl" fontWeight="bold" color="vale.foreground">
              {card.data.total.toLocaleString('pt-BR')}
            </StatNumber>

            <StatHelpText fontSize="md" mt={2}>
              <Text as="span" fontWeight="semibold">
                Verificações não conformes
              </Text>
            </StatHelpText>

            <StatNumber fontSize="3xl" fontWeight="bold" color="gray.700">
              {card.data.nonCompliant.toLocaleString('pt-BR')}
            </StatNumber>

            <StatHelpText fontSize="md" mt={2}>
              <Text as="span" fontWeight="semibold">
                % Verificações não conformes
              </Text>
            </StatHelpText>

            <StatNumber
              fontSize="4xl"
              fontWeight="bold"
              color={getPercentageColor(card.data.percentage)}
            >
              {card.data.percentage.toFixed(2)} %
            </StatNumber>
          </Stat>
        </Box>
      ))}
    </SimpleGrid>
  );
};

export default MetricsCards;
