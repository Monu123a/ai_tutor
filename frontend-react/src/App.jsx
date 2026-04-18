import React, { useState } from 'react';
import axios from 'axios';
import { Sidebar } from './Sidebar';
import { ChatBox } from './ChatBox';
import { InputArea } from './InputArea';
import './App.css';

const API_BASE = import.meta.env.VITE_API_URL || 'http://localhost:8000';

function App() {
  const [topicId, setTopicId] = useState(null);
  const [messages, setMessages] = useState([]);
  const [isUploading, setIsUploading] = useState(false);
  const [isTyping, setIsTyping] = useState(false);
  const [uploadError, setUploadError] = useState(null);
  const [currentFileName, setCurrentFileName] = useState(null);

  const handleUpload = async (file) => {
    if (!file) return;
    setIsUploading(true);
    setUploadError(null);
    setCurrentFileName(file.name);

    const formData = new FormData();
    formData.append('file', file);

    try {
      const res = await axios.post(`${API_BASE}/upload`, formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      });
      setTopicId(res.data.topicId);
      setMessages([{
        role: 'assistant',
        content: `I've successfully processed "${file.name}". What would you like to know about it?`
      }]);
    } catch (err) {
      console.error(err);
      setUploadError(err.response?.data?.detail || 'Failed to upload PDF. Ensure the backend is running.');
      setCurrentFileName(null);
    } finally {
      setIsUploading(false);
    }
  };

  const handleSendMessage = async (text) => {
    if (!text.trim() || !topicId) return;

    const userMsg = { role: 'user', content: text };
    setMessages((prev) => [...prev, userMsg]);
    setIsTyping(true);

    try {
      const res = await axios.post(`${API_BASE}/chat`, {
        topicId,
        question: text
      });
      
      const assistantMsg = {
        role: 'assistant',
        content: res.data.answer,
        sources: res.data.sources,
        image: res.data.image
      };
      
      setMessages((prev) => [...prev, assistantMsg]);
    } catch (err) {
      console.error(err);
      const errorMsg = {
        role: 'assistant',
        content: `Error: ${err.response?.data?.detail || err.message}`
      };
      setMessages((prev) => [...prev, errorMsg]);
    } finally {
      setIsTyping(false);
    }
  };

  return (
    <div className="app-container">
      <Sidebar 
        onUpload={handleUpload} 
        isUploading={isUploading} 
        uploadError={uploadError}
        currentFileName={currentFileName}
        isTopicActive={!!topicId}
      />
      <main className="main-content">
        <ChatBox 
          messages={messages} 
          isTyping={isTyping} 
          apiBase={API_BASE}
        />
        <InputArea 
          onSend={handleSendMessage} 
          disabled={!topicId || isUploading || isTyping} 
        />
      </main>
    </div>
  );
}

export default App;
