/**
 * ConversationItem Component
 * Displays a single conversation in the sidebar
 */

import React from 'react';
import { format, formatDistanceToNow } from 'date-fns';
import { FiMessageSquare, FiTrash2 } from 'react-icons/fi';
import type { Conversation } from '@/types';

interface ConversationItemProps {
  conversation: Conversation;
  isActive: boolean;
  onClick: () => void;
  onDelete: (e: React.MouseEvent) => void;
}

export const ConversationItem: React.FC<ConversationItemProps> = ({
  conversation,
  isActive,
  onClick,
  onDelete,
}) => {
  const timeAgo = formatDistanceToNow(new Date(conversation.updated_at), {
    addSuffix: true,
  });

  return (
    <div
      onClick={onClick}
      className={`group relative px-3 py-3 rounded-lg cursor-pointer transition-colors ${
        isActive
          ? 'bg-primary-50 border border-primary-200'
          : 'hover:bg-gray-50 border border-transparent'
      }`}
    >
      <div className="flex items-start gap-3">
        <div className={`flex-shrink-0 mt-1 ${isActive ? 'text-primary-500' : 'text-gray-400'}`}>
          <FiMessageSquare className="text-lg" />
        </div>
        
        <div className="flex-1 min-w-0">
          <h4
            className={`text-sm font-medium truncate ${
              isActive ? 'text-primary-700' : 'text-gray-900'
            }`}
          >
            {conversation.title}
          </h4>
          <p className="text-xs text-gray-500 mt-1">{timeAgo}</p>
        </div>

        <button
          onClick={onDelete}
          className="flex-shrink-0 opacity-0 group-hover:opacity-100 p-1 text-gray-400 hover:text-red-500 transition-opacity"
          title="Delete conversation"
        >
          <FiTrash2 className="text-sm" />
        </button>
      </div>
    </div>
  );
};
