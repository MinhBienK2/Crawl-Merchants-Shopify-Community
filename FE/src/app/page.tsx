'use client';

/**
 * Main Chat Page
 * Entry point for the chatbot application
 */

import React from 'react';
import { Sidebar } from '@/components/sidebar';
import { MessageList, ChatInput } from '@/components/chat';
import { useChat } from '@/hooks/useChat';

export default function HomePage() {
  const {
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
  } = useChat();

  return (
    <div className="flex h-screen bg-gray-50">
      {/* Sidebar */}
      <Sidebar
        conversations={conversations}
        activeConversationId={activeConversationId}
        onNewChat={startNewChat}
        onSelectConversation={setActiveConversationId}
        onDeleteConversation={deleteConversation}
        isLoading={isLoadingConversations}
      />

      {/* Main Chat Area */}
      <div className="flex-1 flex flex-col">
        {/* Error Banner */}
        {error && (
          <div className="bg-red-50 border-b border-red-200 px-4 py-3">
            <div className="flex items-center gap-2">
              <svg
                className="w-5 h-5 text-red-500"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
                />
              </svg>
              <p className="text-sm text-red-700">{error}</p>
            </div>
          </div>
        )}

        {/* Messages */}
        <MessageList 
          messages={messages} 
          isLoading={isLoadingMessages || isSending} 
        />

        {/* Input */}
        <ChatInput 
          onSendMessage={sendMessage} 
          disabled={isSending} 
        />
      </div>
    </div>
  );
}
