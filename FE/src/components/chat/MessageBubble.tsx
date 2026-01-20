/**
 * MessageBubble Component
 * Displays a single chat message
 */

import React from 'react';
import { format } from 'date-fns';
import ReactMarkdown from 'react-markdown';
import { FiUser, FiCpu } from 'react-icons/fi';
import type { Message } from '@/types';

interface MessageBubbleProps {
  message: Message;
}

export const MessageBubble: React.FC<MessageBubbleProps> = ({ message }) => {
  const isUser = message.role === 'user';
  const formattedTime = format(new Date(message.created_at), 'HH:mm');

  return (
    <div className={`flex gap-3 ${isUser ? 'flex-row-reverse' : 'flex-row'} mb-4`}>
      {/* Avatar */}
      <div
        className={`flex-shrink-0 w-8 h-8 rounded-full flex items-center justify-center ${
          isUser ? 'bg-primary-500' : 'bg-gray-600'
        }`}
      >
        {isUser ? (
          <FiUser className="text-white text-sm" />
        ) : (
          <FiCpu className="text-white text-sm" />
        )}
      </div>

      {/* Message Content */}
      <div className={`flex flex-col ${isUser ? 'items-end' : 'items-start'} max-w-[70%]`}>
        <div
          className={`px-4 py-2 rounded-lg ${
            isUser
              ? 'bg-primary-500 text-white rounded-br-none'
              : 'bg-gray-100 text-gray-900 rounded-bl-none'
          }`}
        >
          {isUser ? (
            <p className="text-sm whitespace-pre-wrap break-words">{message.content}</p>
          ) : (
            <div className="prose prose-sm max-w-none prose-p:my-2 prose-ul:my-2 prose-ol:my-2">
              <ReactMarkdown>{message.content}</ReactMarkdown>
            </div>
          )}
        </div>
        <span className="text-xs text-gray-500 mt-1">{formattedTime}</span>
      </div>
    </div>
  );
};
