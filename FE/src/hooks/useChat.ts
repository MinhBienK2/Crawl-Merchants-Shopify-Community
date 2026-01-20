/**
 * useChat Hook
 * Custom hook for managing chat state and operations
 */

import { useState, useEffect, useCallback } from 'react';
import { chatService } from '@/services';
import type { Conversation, Message } from '@/types';
import { UI_MESSAGES } from '@/constants';

export const useChat = () => {
  const [conversations, setConversations] = useState<Conversation[]>([]);
  const [activeConversationId, setActiveConversationId] = useState<number | null>(null);
  const [messages, setMessages] = useState<Message[]>([]);
  const [isLoadingConversations, setIsLoadingConversations] = useState(false);
  const [isLoadingMessages, setIsLoadingMessages] = useState(false);
  const [isSending, setIsSending] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // Load conversations on mount
  useEffect(() => {
    loadConversations();
  }, []);

  // Load messages when active conversation changes
  useEffect(() => {
    if (activeConversationId) {
      loadMessages(activeConversationId);
    } else {
      setMessages([]);
    }
  }, [activeConversationId]);

  const loadConversations = async () => {
    setIsLoadingConversations(true);
    setError(null);

    const response = await chatService.getConversations(0, 50);

    if (response.error) {
      setError(response.error.message || UI_MESSAGES.ERROR_LOAD_CONVERSATIONS);
    } else if (response.data) {
      setConversations(response.data.conversations);
    }

    setIsLoadingConversations(false);
  };

  const loadMessages = async (conversationId: number) => {
    setIsLoadingMessages(true);
    setError(null);

    const response = await chatService.getConversationDetail(conversationId);

    if (response.error) {
      setError(response.error.message || UI_MESSAGES.ERROR_GENERIC);
      setMessages([]);
    } else if (response.data?.messages) {
      setMessages(response.data.messages);
    }

    setIsLoadingMessages(false);
  };

  const sendMessage = async (content: string) => {
    if (isSending) return;

    setIsSending(true);
    setError(null);

    // Optimistically add user message
    const tempUserMessage: Message = {
      id: Date.now(),
      conversation_id: activeConversationId || 0,
      role: 'user',
      content,
      created_at: new Date().toISOString(),
    };
    setMessages((prev) => [...prev, tempUserMessage]);

    const response = await chatService.sendMessage({
      message: content,
      conversation_id: activeConversationId || undefined,
    });

    if (response.error) {
      setError(response.error.message || UI_MESSAGES.ERROR_SEND_MESSAGE);
      // Remove optimistic message on error
      setMessages((prev) => prev.filter((m) => m.id !== tempUserMessage.id));
    } else if (response.data) {
      const { conversation_id, message: assistantMessage, conversation } = response.data;

      // Update messages
      setMessages((prev) => {
        const filtered = prev.filter((m) => m.id !== tempUserMessage.id);
        return [...filtered, tempUserMessage, assistantMessage];
      });

      // Update or add conversation
      if (conversation) {
        setConversations((prev) => {
          const exists = prev.find((c) => c.id === conversation.id);
          if (exists) {
            return prev.map((c) => (c.id === conversation.id ? conversation : c));
          }
          return [conversation, ...prev];
        });
      }

      // Set active conversation if new
      if (!activeConversationId) {
        setActiveConversationId(conversation_id);
      }
    }

    setIsSending(false);
  };

  const deleteConversation = async (id: number) => {
    const response = await chatService.deleteConversation(id);

    if (response.error) {
      setError(response.error.message || UI_MESSAGES.ERROR_DELETE_CONVERSATION);
    } else {
      setConversations((prev) => prev.filter((c) => c.id !== id));
      if (activeConversationId === id) {
        setActiveConversationId(null);
        setMessages([]);
      }
    }
  };

  const startNewChat = () => {
    setActiveConversationId(null);
    setMessages([]);
    setError(null);
  };

  return {
    conversations,
    activeConversationId,
    messages,
    isLoadingConversations,
    isLoadingMessages,
    isSending,
    error,
    sendMessage,
    deleteConversation,
    startNewChat,
    setActiveConversationId,
  };
};
