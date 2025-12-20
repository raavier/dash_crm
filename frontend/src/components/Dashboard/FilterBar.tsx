import { Box, SimpleGrid, FormControl, FormLabel, Select, Input, Button, HStack, Text } from '@chakra-ui/react';
import { AddIcon, RepeatIcon } from '@chakra-ui/icons';
import { useDashboard } from '../../context/DashboardContext';
import { format } from 'date-fns';

const FilterBar = () => {
  const { filters, filterOptions, updateFilters, refreshData, lastUpdated } = useDashboard();

  const handleOrganizationChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    updateFilters({ organization: e.target.value });
  };

  const handleLocationChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    updateFilters({ location: e.target.value });
  };

  const handleVerificationTypeChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    updateFilters({ verificationType: e.target.value });
  };

  const handleStartDateChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    updateFilters({
      dateRange: {
        ...filters.dateRange,
        start: new Date(e.target.value),
      },
    });
  };

  const handleEndDateChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    updateFilters({
      dateRange: {
        ...filters.dateRange,
        end: new Date(e.target.value),
      },
    });
  };

  return (
    <Box bg="white" borderRadius="lg" boxShadow="sm" p={6} mb={6}>
      <SimpleGrid columns={{ base: 1, md: 2, lg: 4 }} spacing={4} mb={4}>
        {/* Organização */}
        <FormControl>
          <FormLabel fontSize="sm" fontWeight="semibold" color="gray.700">
            Organização
          </FormLabel>
          <Select
            value={filters.organization}
            onChange={handleOrganizationChange}
            size="md"
            borderColor="gray.300"
          >
            {filterOptions?.organizations.map((org) => (
              <option key={org} value={org}>
                {org}
              </option>
            ))}
          </Select>
        </FormControl>

        {/* Localização */}
        <FormControl>
          <FormLabel fontSize="sm" fontWeight="semibold" color="gray.700">
            Localização
          </FormLabel>
          <Select
            value={filters.location}
            onChange={handleLocationChange}
            size="md"
            borderColor="gray.300"
          >
            {filterOptions?.locations.map((loc) => (
              <option key={loc} value={loc}>
                {loc}
              </option>
            ))}
          </Select>
        </FormControl>

        {/* Tipo verificação */}
        <FormControl>
          <FormLabel fontSize="sm" fontWeight="semibold" color="gray.700">
            Tipo verificação
          </FormLabel>
          <Select
            value={filters.verificationType}
            onChange={handleVerificationTypeChange}
            size="md"
            borderColor="gray.300"
          >
            {filterOptions?.verificationTypes.map((type) => (
              <option key={type} value={type}>
                {type}
              </option>
            ))}
          </Select>
        </FormControl>

        {/* Data de verificação */}
        <FormControl>
          <FormLabel fontSize="sm" fontWeight="semibold" color="gray.700">
            Data de verificação
          </FormLabel>
          <HStack>
            <Input
              type="date"
              value={format(filters.dateRange.start, 'yyyy-MM-dd')}
              onChange={handleStartDateChange}
              size="md"
              borderColor="gray.300"
            />
            <Input
              type="date"
              value={format(filters.dateRange.end, 'yyyy-MM-dd')}
              onChange={handleEndDateChange}
              size="md"
              borderColor="gray.300"
            />
          </HStack>
        </FormControl>
      </SimpleGrid>

      {/* Botões e última atualização */}
      <HStack justify="space-between" flexWrap="wrap">
        <HStack spacing={3}>
          <Button
            leftIcon={<AddIcon />}
            size="sm"
            variant="outline"
            colorScheme="gray"
          >
            + Mais Filtros
          </Button>

          <Button
            leftIcon={<RepeatIcon />}
            size="sm"
            bg="vale.primary"
            color="white"
            _hover={{ bg: 'vale.primary', opacity: 0.9 }}
            onClick={refreshData}
          >
            Aplicar filtros
          </Button>
        </HStack>

        {lastUpdated && (
          <Text fontSize="xs" color="gray.500">
            Última atualização dos dados: {format(lastUpdated, 'dd/MM/yyyy HH:mm:ss')}
          </Text>
        )}
      </HStack>
    </Box>
  );
};

export default FilterBar;
