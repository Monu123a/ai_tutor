import React, { useState } from 'react';
import { Send } from 'lucide-react';

export function InputArea({ onSend, disabled }) {
  const [text, setText] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    if (text.trim() && !disabled) {
      onSend(text);
      setText('');
    }
  };

  return (
    <div className="input-area">
      <form onSubmit={handleSubmit} className="input-wrapper">
        <input 
          type="text" 
          value={text}
          onChange={(e) => setText(e.target.value)}
          placeholder={disabled ? "Upload a PDF to ask a question..." : "Ask a question about the chapter..."}
          className="input-box"
          disabled={disabled}
        />
        <button 
          type="submit" 
          className="send-button"
          disabled={disabled || !text.trim()}
        >
          <Send size={18} />
        </button>
      </form>
    </div>
  );
}
