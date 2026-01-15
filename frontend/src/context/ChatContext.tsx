import React, { createContext, useContext, useState, useEffect, type ReactNode } from 'react';
import type { ChatMessage } from '../services/chatService';

interface ChatContextType {
  messages: ChatMessage[];
  isOpen: boolean;
  isLoading: boolean;
  userId: string | null;
  openChat: () => void;
  closeChat: () => void;
  toggleChat: () => void;
  sendMessage: (message: string) => Promise<void>;
  setUserId: (userId: string) => void;
}

const ChatContext = createContext<ChatContextType | undefined>(undefined);

export const ChatProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [isOpen, setIsOpen] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [userId, setUserId] = useState<string | null>(null);

  // Tentar obter userId do localStorage na inicialização
  useEffect(() => {
    const savedUserId = localStorage.getItem('chat_user_id');
    if (savedUserId) {
      setUserId(savedUserId);
    }
  }, []);

  const openChat = () => {
    // Se não tem userId, pedir agora (só quando abrir o chat)
    if (!userId) {
      const email = prompt('Digite seu email para usar o chatbot:');
      if (email) {
        setUserId(email);
        localStorage.setItem('chat_user_id', email);
        setIsOpen(true);
      }
    } else {
      setIsOpen(true);
    }
  };

  const closeChat = () => setIsOpen(false);

  const toggleChat = () => {
    if (isOpen) {
      closeChat();
    } else {
      openChat();
    }
  };

  const sendMessage = async (message: string) => {
    if (!userId) {
      console.error('User ID not set');
      return;
    }

    // Adiciona mensagem do usuário
    const userMessage: ChatMessage = {
      role: 'user',
      content: message,
      timestamp: new Date()
    };
    setMessages(prev => [...prev, userMessage]);

    setIsLoading(true);
    try {
      // Import dinâmico para evitar problemas de carregamento
      const { chatService } = await import('../services/chatService');
      const response = await chatService.sendMessage(userId, message);

      // Adiciona resposta do bot
      const botMessage: ChatMessage = {
        role: 'assistant',
        content: response.response,
        timestamp: new Date()
      };
      setMessages(prev => [...prev, botMessage]);
    } catch (error: any) {
      console.error('Error sending message:', error);

      // Extrai mensagem de erro do backend (se disponível)
      let errorContent = 'Desculpe, ocorreu um erro ao processar sua mensagem. Tente novamente.';

      if (error.response?.data?.detail) {
        errorContent = error.response.data.detail;
      } else if (error.response?.status === 504) {
        errorContent = 'O chatbot está inicializando. Por favor, aguarde alguns instantes e tente novamente.';
      }

      // Mensagem de erro
      const errorMessage: ChatMessage = {
        role: 'assistant',
        content: errorContent,
        timestamp: new Date()
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <ChatContext.Provider value={{
      messages,
      isOpen,
      isLoading,
      userId,
      openChat,
      closeChat,
      toggleChat,
      sendMessage,
      setUserId
    }}>
      {children}
    </ChatContext.Provider>
  );
};

export const useChat = () => {
  const context = useContext(ChatContext);
  if (!context) {
    throw new Error('useChat must be used within ChatProvider');
  }
  return context;
};
