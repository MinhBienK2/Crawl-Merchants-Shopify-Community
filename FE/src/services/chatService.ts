/**
 * Chat Service - Business Logic for Chat Operations
 * Handles all chat-related API calls
 */

import { apiService } from './api';
import { API_ENDPOINTS } from '@/constants';
import type {
  ChatRequest,
  ChatResponse,
  Conversation,
  ConversationsResponse,
  ApiResponse,
} from '@/types';

class ChatService {
  /**
   * Send a chat message
   */
  async sendMessage(request: ChatRequest): Promise<ApiResponse<ChatResponse>> {
    return apiService.post<ChatResponse>(API_ENDPOINTS.CHAT, request);
  }

  /**
   * Get list of conversations
   */
  async getConversations(
    skip: number = 0,
    limit: number = 20
  ): Promise<ApiResponse<ConversationsResponse>> {
    return apiService.get<ConversationsResponse>(
      `${API_ENDPOINTS.CONVERSATIONS}?skip=${skip}&limit=${limit}`
    );
  }

  /**
   * Get conversation details with messages
   */
  async getConversationDetail(id: number): Promise<ApiResponse<Conversation>> {
    return apiService.get<Conversation>(API_ENDPOINTS.CONVERSATION_DETAIL(id));
  }

  /**
   * Delete a conversation
   */
  async deleteConversation(id: number): Promise<ApiResponse<{ message: string }>> {
    return apiService.delete<{ message: string }>(
      API_ENDPOINTS.CONVERSATION_DELETE(id)
    );
  }

  /**
   * Health check
   */
  async healthCheck(): Promise<ApiResponse<{ status: string }>> {
    return apiService.get<{ status: string }>(API_ENDPOINTS.HEALTH);
  }
}

export const chatService = new ChatService();
