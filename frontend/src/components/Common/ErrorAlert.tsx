import { Alert, AlertIcon, AlertTitle, AlertDescription, Box, Button } from '@chakra-ui/react';
import { RepeatIcon } from '@chakra-ui/icons';

interface ErrorAlertProps {
  title?: string;
  message: string;
  onRetry?: () => void;
}

const ErrorAlert = ({ title = 'Erro', message, onRetry }: ErrorAlertProps) => {
  return (
    <Alert
      status="error"
      variant="subtle"
      flexDirection="column"
      alignItems="center"
      justifyContent="center"
      textAlign="center"
      minH="200px"
      borderRadius="lg"
    >
      <AlertIcon boxSize="40px" mr={0} />
      <AlertTitle mt={4} mb={1} fontSize="lg">
        {title}
      </AlertTitle>
      <AlertDescription maxWidth="sm" mb={4}>
        {message}
      </AlertDescription>
      {onRetry && (
        <Box>
          <Button
            leftIcon={<RepeatIcon />}
            colorScheme="red"
            variant="outline"
            size="sm"
            onClick={onRetry}
          >
            Tentar novamente
          </Button>
        </Box>
      )}
    </Alert>
  );
};

export default ErrorAlert;
