import {
  Box,
  Heading,
  Table,
  Thead,
  Tbody,
  Tr,
  Th,
  Td,
  Badge,
  HStack,
  Button,
  Text,
} from '@chakra-ui/react';
import { ChevronLeftIcon, ChevronRightIcon } from '@chakra-ui/icons';
import { useDashboard } from '../../context/DashboardContext';
import { format } from 'date-fns';
import { ptBR } from 'date-fns/locale';

const ActionsTable = () => {
  const { openActions, setPage } = useDashboard();

  if (!openActions) return null;

  const { data, total, page, pageSize } = openActions;
  const totalPages = Math.ceil(total / pageSize);

  const getStatusBadge = (status: 'Atrasado' | 'Em Andamento') => {
    if (status === 'Atrasado') {
      return (
        <Badge colorScheme="red" bg="vale.danger" color="white" px={3} py={1} borderRadius="md">
          Atrasado
        </Badge>
      );
    }
    return (
      <Badge colorScheme="blue" bg="vale.info" color="white" px={3} py={1} borderRadius="md">
        Em Andamento
      </Badge>
    );
  };

  const formatDate = (dateStr: string) => {
    try {
      return format(new Date(dateStr), 'dd/MM/yyyy', { locale: ptBR });
    } catch {
      return dateStr;
    }
  };

  return (
    <Box bg="white" borderRadius="lg" boxShadow="md" p={6}>
      <Heading as="h3" size="md" mb={6} color="vale.foreground">
        CRM - Lista de ações em aberto
      </Heading>

      <Box overflowX="auto">
        <Table variant="simple" size="sm">
          <Thead bg="vale.tableAccent">
            <Tr>
              <Th color="white" fontWeight="bold" textTransform="uppercase">
                ID Ação
              </Th>
              <Th color="white" fontWeight="bold" textTransform="uppercase">
                ID Verificação
              </Th>
              <Th color="white" fontWeight="bold" textTransform="uppercase">
                Responsável
              </Th>
              <Th color="white" fontWeight="bold" textTransform="uppercase">
                Data de Vencimento
              </Th>
              <Th color="white" fontWeight="bold" textTransform="uppercase">
                Status da Ação
              </Th>
              <Th color="white" fontWeight="bold" textTransform="uppercase">
                Tipo
              </Th>
            </Tr>
          </Thead>
          <Tbody>
            {data.map((action, index) => (
              <Tr
                key={action.id}
                bg={index % 2 === 0 ? 'gray.50' : 'white'}
                _hover={{ bg: 'gray.100' }}
                transition="background 0.2s"
              >
                <Td fontWeight="semibold" color="vale.primary">
                  {action.id}
                </Td>
                <Td fontWeight="semibold" color="vale.primary">
                  {action.verificationId}
                </Td>
                <Td>{action.responsible}</Td>
                <Td>{formatDate(action.dueDate)}</Td>
                <Td>{getStatusBadge(action.status)}</Td>
                <Td>{action.type}</Td>
              </Tr>
            ))}
          </Tbody>
        </Table>
      </Box>

      {/* Paginação */}
      <HStack justify="space-between" mt={6}>
        <Text fontSize="sm" color="gray.600">
          Mostrando {(page - 1) * pageSize + 1} a {Math.min(page * pageSize, total)} de {total} ações
        </Text>

        <HStack>
          <Button
            size="sm"
            leftIcon={<ChevronLeftIcon />}
            onClick={() => setPage(page - 1)}
            isDisabled={page === 1}
            variant="outline"
          >
            Anterior
          </Button>

          <Text fontSize="sm" fontWeight="medium" px={2}>
            Página {page} de {totalPages}
          </Text>

          <Button
            size="sm"
            rightIcon={<ChevronRightIcon />}
            onClick={() => setPage(page + 1)}
            isDisabled={page === totalPages}
            variant="outline"
          >
            Próxima
          </Button>
        </HStack>
      </HStack>
    </Box>
  );
};

export default ActionsTable;
