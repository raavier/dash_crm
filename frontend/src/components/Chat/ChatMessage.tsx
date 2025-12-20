import { Box, Text, Flex } from '@chakra-ui/react';
import type { ChatMessage as ChatMessageType } from '../../services/chatService';

interface ChatMessageProps {
  message: ChatMessageType;
}

const ChatMessage = ({ message }: ChatMessageProps) => {
  const isUser = message.role === 'user';

  return (
    <Flex justify={isUser ? 'flex-end' : 'flex-start'}>
      <Box
        bg={isUser ? 'blue.500' : 'white'}
        color={isUser ? 'white' : 'gray.800'}
        px={4}
        py={3}
        borderRadius="lg"
        maxW="80%"
        boxShadow="sm"
      >
        <Text whiteSpace="pre-wrap">{message.content}</Text>
        <Text
          fontSize="xs"
          color={isUser ? 'blue.100' : 'gray.500'}
          mt={1}
        >
          {message.timestamp.toLocaleTimeString('pt-BR', {
            hour: '2-digit',
            minute: '2-digit'
          })}
        </Text>
      </Box>
    </Flex>
  );
};

export default ChatMessage;
