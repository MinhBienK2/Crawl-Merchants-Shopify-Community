/**
 * TypeScript Type Definitions
 */

export interface Message {
  id: number;
  conversation_id: number;
  role: 'user' | 'assistant' | 'system';
  content: string;
  created_at: string;
}

export interface Conversation {
  id: number;
  title: string;
  created_at: string;
  updated_at: string;
  messages?: Message[];
  message_count?: number;
}

export interface ChatRequest {
  message: string;
  conversation_id?: number;
}

export interface ChatResponse {
  conversation_id: number;
  message: Message;
  conversation?: Conversation;
}

export interface ConversationsResponse {
  conversations: Conversation[];
  total: number;
  skip: number;
  limit: number;
}

export interface ApiError {
  detail?: string;
  message?: string;
  error?: string;
}

export interface ApiResponse<T = any> {
  data?: T;
  error?: ApiError;
  status: number;
}

export interface LoadingState {
  isLoading: boolean;
  error?: string | null;
}
