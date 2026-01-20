/**
 * Sidebar Component
 * Main sidebar with new chat button and conversation list
 */

import React from 'react';
import { FiPlus } from 'react-icons/fi';
import { ConversationList } from './ConversationList';
import type { Conversation } from '@/types';
import { UI_MESSAGES, APP_CONFIG } from '@/constants';

interface SidebarProps {
  conversations: Conversation[];
  activeConversationId: number | null;
  onNewChat: () => void;
  onSelectConversation: (id: number) => void;
  onDeleteConversation: (id: number) => void;
  isLoading?: boolean;
}

export const Sidebar: React.FC<SidebarProps> = ({
  conversations,
  activeConversationId,
  onNewChat,
  onSelectConversation,
  onDeleteConversation,
  isLoading,
}) => {
  return (
    <div className="w-80 bg-white border-r border-gray-200 flex flex-col h-screen">
      {/* Header */}
      <div className="p-4 border-b border-gray-200">
        <h1 className="text-xl font-bold text-gray-900 mb-4">{APP_CONFIG.NAME}</h1>
        
        <button
          onClick={onNewChat}
          className="w-full flex items-center justify-center gap-2 px-4 py-3 bg-primary-500 text-white rounded-lg hover:bg-primary-600 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:ring-offset-2 transition-colors"
        >
          <FiPlus className="text-xl" />
          <span className="font-medium">{UI_MESSAGES.NEW_CHAT}</span>
        </button>
      </div>

      {/* Conversations */}
      <div className="flex-1 overflow-y-auto p-4">
        <h2 className="text-xs font-semibold text-gray-500 uppercase tracking-wider mb-3">
          Conversations
        </h2>
        
        <ConversationList
          conversations={conversations}
          activeConversationId={activeConversationId}
          onSelectConversation={onSelectConversation}
          onDeleteConversation={onDeleteConversation}
          isLoading={isLoading}
        />
      </div>

      {/* Footer */}
      <div className="p-4 border-t border-gray-200">
        <p className="text-xs text-gray-500 text-center">
          Powered by Shopify Community Data
        </p>
      </div>
    </div>
  );
};
