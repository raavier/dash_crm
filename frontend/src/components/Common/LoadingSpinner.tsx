import { Flex, Spinner, Text, VStack } from '@chakra-ui/react';

interface LoadingSpinnerProps {
  message?: string;
}

const LoadingSpinner = ({ message = 'Carregando dados...' }: LoadingSpinnerProps) => {
  return (
    <Flex justify="center" align="center" minH="400px">
      <VStack spacing={4}>
        <Spinner
          thickness="4px"
          speed="0.65s"
          emptyColor="gray.200"
          color="vale.primary"
          size="xl"
        />
        <Text color="gray.600" fontSize="md">
          {message}
        </Text>
      </VStack>
    </Flex>
  );
};

export default LoadingSpinner;
