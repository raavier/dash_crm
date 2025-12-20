import { Box, Flex, Heading, Tabs, TabList, Tab, Button, HStack, Text } from '@chakra-ui/react';

const Header = () => {
  return (
    <Box bg="vale.primary" color="white" px={6} py={4} boxShadow="md">
      <Flex justify="space-between" align="center" maxW="1920px" mx="auto">
        {/* Logo e Título */}
        <HStack spacing={4}>
          <Text fontSize="2xl" fontWeight="bold" letterSpacing="wider">
            VALE
          </Text>
          <Heading as="h1" size="md" fontWeight="bold">
            Gerenciamento de Riscos Críticos
          </Heading>
        </HStack>

        {/* Botões de idioma e versão */}
        <HStack spacing={4}>
          <Button
            size="sm"
            variant="solid"
            bg="yellow.400"
            color="vale.primary"
            fontWeight="bold"
            _hover={{ bg: 'yellow.500' }}
          >
            PT
          </Button>
          <Button
            size="sm"
            variant="outline"
            color="white"
            borderColor="white"
            _hover={{ bg: 'whiteAlpha.200' }}
          >
            EN
          </Button>
          <Text fontSize="xs" opacity={0.8}>
            REV 3.0
          </Text>
        </HStack>
      </Flex>

      {/* Tabs */}
      <Tabs variant="unstyled" mt={4} maxW="1920px" mx="auto">
        <TabList>
          <Tab
            color="white"
            fontWeight="medium"
            _selected={{
              color: 'white',
              borderBottom: '3px solid',
              borderColor: 'white',
            }}
            _hover={{ opacity: 0.8 }}
          >
            FMDS
          </Tab>
          <Tab
            color="white"
            fontWeight="medium"
            _selected={{
              color: 'white',
              borderBottom: '3px solid',
              borderColor: 'white',
            }}
            _hover={{ opacity: 0.8 }}
          >
            Detalhamento
          </Tab>
          <Tab
            color="white"
            fontWeight="medium"
            _selected={{
              color: 'white',
              borderBottom: '3px solid',
              borderColor: 'white',
            }}
            _hover={{ opacity: 0.8 }}
          >
            Ações
          </Tab>
        </TabList>
      </Tabs>
    </Box>
  );
};

export default Header;
