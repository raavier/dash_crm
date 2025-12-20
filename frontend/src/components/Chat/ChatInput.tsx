import { useState, type KeyboardEvent } from 'react';
import { HStack, Input, IconButton } from '@chakra-ui/react';
import { FiSend } from 'react-icons/fi';
import { useChat } from '../../context/ChatContext';

const ChatInput = () => {
  const { sendMessage, isLoading } = useChat();
  const [input, setInput] = useState('');

  const handleSend = async () => {
    if (!input.trim() || isLoading) return;

    await sendMessage(input);
    setInput('');
  };

  const handleKeyPress = (e: KeyboardEvent<HTMLInputElement>) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  return (
    <HStack p={4} bg="white" borderTop="1px" borderColor="gray.200">
      <Input
        placeholder="Digite sua mensagem..."
        value={input}
        onChange={(e) => setInput(e.target.value)}
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
        isDisabled={!input.trim()}
      />
    </HStack>
  );
};

export default ChatInput;
