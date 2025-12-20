import api from './api';

export interface ChatMessage {
  role: 'user' | 'assistant';
  content: string;
  timestamp: Date;
}

export interface ChatResponse {
  response: string;
}

class ChatService {
  /**
   * Envia mensagem para o chatbot via backend proxy
   */
  async sendMessage(userId: string, query: string): Promise<ChatResponse> {
    const response = await api.post<ChatResponse>('/api/chat/message', {
      user_id: userId,
      query: query
    });

    return response.data;
  }
}

export const chatService = new ChatService();
