import {
  Box,
  VStack,
  HStack,
  Text,
  CloseButton,
  Flex
} from '@chakra-ui/react';
import { useRef, useEffect } from 'react';
import { useChat } from '../../context/ChatContext';
import ChatMessage from './ChatMessage';
import ChatInput from './ChatInput';

const ChatWindow = () => {
  const { messages, isLoading, closeChat } = useChat();
  const messagesEndRef = useRef<HTMLDivElement>(null);

  // Auto-scroll to bottom (inspired by template's useMessages hook)
  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, isLoading]);

  return (
    <Box
      position="fixed"
      bottom="90px"
      right="20px"
      width="400px"
      height="600px"
      bg="white"
      borderRadius="lg"
      boxShadow="2xl"
      zIndex={1000}
      display="flex"
      flexDirection="column"
      overflow="hidden"
    >
      {/* Header */}
      <HStack
        bg="blue.500"
        color="white"
        p={4}
        justify="space-between"
      >
        <Text fontWeight="bold" fontSize="lg">Connect Bot</Text>
        <CloseButton size="sm" onClick={closeChat} />
      </HStack>

      {/* Messages */}
      <VStack
        flex={1}
        overflowY="auto"
        p={4}
        spacing={4}
        align="stretch"
        bg="gray.50"
      >
        {messages.length === 0 && (
          <Text color="gray.500" textAlign="center" mt={4}>
            Olá! Como posso ajudar?
          </Text>
        )}

        {messages.map((msg, idx) => (
          <ChatMessage key={idx} message={msg} />
        ))}

        {isLoading && (
          <Flex justify="flex-start">
            <Box
              bg="gray.200"
              px={4}
              py={2}
              borderRadius="lg"
              maxW="80%"
            >
              <Text color="gray.600" fontStyle="italic">
                Digitando...
              </Text>
            </Box>
          </Flex>
        )}

        <div ref={messagesEndRef} />
      </VStack>

      {/* Input */}
      <ChatInput />
    </Box>
  );
};

export default ChatWindow;
