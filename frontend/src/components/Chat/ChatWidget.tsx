import { IconButton, Box, VStack, HStack, Text, CloseButton, Input } from '@chakra-ui/react';
import { FiMessageCircle, FiX, FiSend } from 'react-icons/fi';
import { useChat } from '../../context/ChatContext';
import { useState } from 'react';

const ChatWidget = () => {
  const { isOpen, toggleChat, messages, isLoading, sendMessage } = useChat();
  const [inputValue, setInputValue] = useState('');

  const handleSend = async () => {
    if (!inputValue.trim() || isLoading) return;
    await sendMessage(inputValue);
    setInputValue('');
  };

  const handleKeyPress = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  return (
    <>
      {/* Floating button */}
      <IconButton
        aria-label={isOpen ? "Fechar chat" : "Abrir chat"}
        icon={isOpen ? <FiX /> : <FiMessageCircle />}
        position="fixed"
        bottom="20px"
        right="20px"
        size="lg"
        colorScheme="blue"
        borderRadius="full"
        boxShadow="2xl"
        onClick={toggleChat}
        zIndex={1001}
        _hover={{ transform: 'scale(1.1)' }}
        transition="all 0.2s"
      />

      {/* Chat window inline */}
      {isOpen && (
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
          <HStack bg="blue.500" color="white" p={4} justify="space-between">
            <Text fontWeight="bold" fontSize="lg">Connect Bot</Text>
            <CloseButton size="sm" onClick={toggleChat} />
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
              <Box
                key={idx}
                alignSelf={msg.role === 'user' ? 'flex-end' : 'flex-start'}
                maxW="80%"
              >
                <Box
                  bg={msg.role === 'user' ? 'blue.500' : 'white'}
                  color={msg.role === 'user' ? 'white' : 'gray.800'}
                  px={4}
                  py={3}
                  borderRadius="lg"
                  boxShadow="sm"
                >
                  <Text whiteSpace="pre-wrap">{msg.content}</Text>
                </Box>
              </Box>
            ))}

            {isLoading && (
              <Box alignSelf="flex-start" maxW="80%">
                <Box bg="gray.200" px={4} py={2} borderRadius="lg">
                  <Text color="gray.600" fontStyle="italic">Digitando...</Text>
                </Box>
              </Box>
            )}
          </VStack>

          {/* Input */}
          <HStack p={4} bg="white" borderTop="1px" borderColor="gray.200">
            <Input
              placeholder="Digite sua mensagem..."
              value={inputValue}
              onChange={(e) => setInputValue(e.target.value)}
              onKeyPress={handleKeyPress}
              disabled={isLoading}
              variant="filled"
            />
            <IconButton
              aria-label="Enviar mensagem"
              icon={<FiSend />}
              colorScheme="blue"
              onClick={handleSend}
              isLoading={isLoading}
              isDisabled={!inputValue.trim()}
            />
          </HStack>
        </Box>
      )}
    </>
  );
};

export default ChatWidget;
