import React, { useEffect, useRef } from 'react';
import { Message } from './Message';
import { Bot } from 'lucide-react';

export function ChatBox({ messages, isTyping, apiBase }) {
  const bottomRef = useRef(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, isTyping]);

  return (
    <div className="chat-container">
      {messages.length === 0 ? (
        <div className="empty-state animate-fade-in">
          <Bot size={64} />
          <h2>Welcome to your AI Tutor</h2>
          <p>Upload a chapter PDF to begin your interactive learning session.</p>
        </div>
      ) : (
        messages.map((msg, idx) => (
          <Message key={idx} message={msg} apiBase={apiBase} />
        ))
      )}
      
      {isTyping && (
        <div className="message-wrapper assistant animate-fade-in">
          <div className="avatar assistant">
            <Bot size={20} />
          </div>
          <div className="message-content">
            <div className="typing-indicator">
              <span className="typing-dot"></span>
              <span className="typing-dot"></span>
              <span className="typing-dot"></span>
            </div>
          </div>
        </div>
      )}
      
      <div ref={bottomRef} />
    </div>
  );
}
