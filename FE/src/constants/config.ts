/**
 * Application Configuration Constants
 * Centralized configuration for easy management
 */

export const API_CONFIG = {
  BASE_URL: process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000',
  VERSION: process.env.NEXT_PUBLIC_API_VERSION || 'v1',
  TIMEOUT: 30000, // 30 seconds
} as const;

export const APP_CONFIG = {
  NAME: process.env.NEXT_PUBLIC_APP_NAME || 'Merchants Community Chatbot',
  MAX_MESSAGE_LENGTH: Number(process.env.NEXT_PUBLIC_MAX_MESSAGE_LENGTH) || 2000,
  MESSAGES_PER_PAGE: 50,
  CONVERSATIONS_PER_PAGE: 20,
} as const;

export const UI_CONFIG = {
  SIDEBAR_WIDTH: 320,
  ANIMATION_DURATION: 200,
  DEBOUNCE_DELAY: 300,
} as const;

export const MESSAGE_ROLES = {
  USER: 'user',
  ASSISTANT: 'assistant',
  SYSTEM: 'system',
} as const;

export const API_ENDPOINTS = {
  HEALTH: '/api/v1/health',
  CHAT: '/api/v1/chat',
  CONVERSATIONS: '/api/v1/conversations',
  CONVERSATION_DETAIL: (id: number) => `/api/v1/conversations/${id}`,
  CONVERSATION_DELETE: (id: number) => `/api/v1/conversations/${id}/delete`,
} as const;
