/**
 * ChatInput Component
 * Input field for sending chat messages
 */

import React, { useState, KeyboardEvent, ChangeEvent } from 'react';
import { FiSend } from 'react-icons/fi';
import { APP_CONFIG, UI_MESSAGES, PLACEHOLDERS } from '@/constants';

interface ChatInputProps {
  onSendMessage: (message: string) => void;
  disabled?: boolean;
}

export const ChatInput: React.FC<ChatInputProps> = ({ onSendMessage, disabled }) => {
  const [message, setMessage] = useState('');
  const [error, setError] = useState<string | null>(null);

  const handleSend = () => {
    const trimmedMessage = message.trim();

    if (!trimmedMessage) {
      setError(UI_MESSAGES.EMPTY_MESSAGE);
      return;
    }

    if (trimmedMessage.length > APP_CONFIG.MAX_MESSAGE_LENGTH) {
      setError(UI_MESSAGES.MESSAGE_TOO_LONG);
      return;
    }

    setError(null);
    onSendMessage(trimmedMessage);
    setMessage('');
  };

  const handleKeyPress = (e: KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  const handleChange = (e: ChangeEvent<HTMLTextAreaElement>) => {
    setMessage(e.target.value);
    if (error) setError(null);
  };

  return (
    <div className="border-t border-gray-200 bg-white p-4">
      {error && (
        <div className="mb-2 text-sm text-red-500">
          {error}
        </div>
      )}
      
      <div className="flex gap-2 items-end">
        <div className="flex-1 relative">
          <textarea
            value={message}
            onChange={handleChange}
            onKeyPress={handleKeyPress}
            placeholder={PLACEHOLDERS.MESSAGE_INPUT}
            disabled={disabled}
            rows={1}
            className="w-full px-4 py-3 pr-12 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent resize-none disabled:bg-gray-100 disabled:cursor-not-allowed"
            style={{
              minHeight: '48px',
              maxHeight: '120px',
            }}
          />
          <span className="absolute bottom-2 right-2 text-xs text-gray-400">
            {message.length}/{APP_CONFIG.MAX_MESSAGE_LENGTH}
          </span>
        </div>
        
        <button
          onClick={handleSend}
          disabled={disabled || !message.trim()}
          className="px-4 py-3 bg-primary-500 text-white rounded-lg hover:bg-primary-600 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:ring-offset-2 disabled:bg-gray-300 disabled:cursor-not-allowed transition-colors"
        >
          <FiSend className="text-xl" />
        </button>
      </div>
      
      <p className="text-xs text-gray-500 mt-2">
        Press Enter to send, Shift + Enter for new line
      </p>
    </div>
  );
};
