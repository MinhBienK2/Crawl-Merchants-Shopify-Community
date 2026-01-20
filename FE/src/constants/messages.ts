/**
 * User-facing messages and labels
 */

export const UI_MESSAGES = {
  WELCOME: 'Welcome to Merchants Community Chatbot',
  WELCOME_SUBTITLE: 'Ask me anything about the Shopify Community data',
  NEW_CHAT: 'New Chat',
  TYPE_MESSAGE: 'Type your message...',
  SEND: 'Send',
  DELETE_CONFIRM: 'Are you sure you want to delete this conversation?',
  LOADING: 'Loading...',
  SENDING: 'Sending...',
  NO_CONVERSATIONS: 'No conversations yet',
  START_NEW_CONVERSATION: 'Start a new conversation to get started',
  ERROR_GENERIC: 'Something went wrong. Please try again.',
  ERROR_NETWORK: 'Network error. Please check your connection.',
  ERROR_SEND_MESSAGE: 'Failed to send message. Please try again.',
  ERROR_LOAD_CONVERSATIONS: 'Failed to load conversations.',
  ERROR_DELETE_CONVERSATION: 'Failed to delete conversation.',
  SUCCESS_DELETE: 'Conversation deleted successfully',
  EMPTY_MESSAGE: 'Please enter a message',
  MESSAGE_TOO_LONG: 'Message is too long',
} as const;

export const PLACEHOLDERS = {
  SEARCH: 'Search conversations...',
  MESSAGE_INPUT: 'Ask about Shopify Community data...',
} as const;
