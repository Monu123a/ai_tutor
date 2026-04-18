import React, { useState } from 'react';
import { User, Bot, ChevronDown, ChevronRight } from 'lucide-react';

export function Message({ message, apiBase }) {
  const [showSources, setShowSources] = useState(false);
  const isUser = message.role === 'user';

  return (
    <div className={`message-wrapper ${isUser ? 'user' : 'assistant'} animate-fade-in`}>
      <div className={`avatar ${isUser ? 'user' : 'assistant'}`}>
        {isUser ? <User size={20} /> : <Bot size={20} />}
      </div>
      
      <div style={{ flex: 1, maxWidth: '100%' }}>
        <div className="message-content">
          <div style={{ whiteSpace: 'pre-wrap' }}>{message.content}</div>
          
          {message.image && (
            <div className="message-image animate-fade-in">
              <img 
                src={message.image.url || `${apiBase}/assets/${message.image.filename}`} 
                alt={message.image.title} 
                onError={(e) => { e.currentTarget.style.display = 'none'; }}
              />
              <div className="image-caption">
                {message.image.title} • {message.image.description}
              </div>
            </div>
          )}
          
          {message.sources && message.sources.length > 0 && (
            <div className="sources-container">
              <button 
                className="sources-toggle" 
                onClick={() => setShowSources(!showSources)}
              >
                {showSources ? <ChevronDown size={14} /> : <ChevronRight size={14} />}
                {showSources ? 'Hide Sources' : 'View Sources'}
              </button>
              
              {showSources && (
                <div className="sources-list animate-fade-in">
                  {message.sources.map((source, idx) => (
                    <div key={idx} className="source-item">
                      "{source.trim()}"
                    </div>
                  ))}
                </div>
              )}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
