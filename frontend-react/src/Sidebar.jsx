import React, { useCallback, useState } from 'react';
import { UploadCloud, CheckCircle, AlertCircle, BookOpen } from 'lucide-react';

export function Sidebar({ onUpload, isUploading, uploadError, currentFileName, isTopicActive }) {
  const [isDragActive, setIsDragActive] = useState(false);

  const handleDrag = useCallback((e) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === 'dragenter' || e.type === 'dragover') {
      setIsDragActive(true);
    } else if (e.type === 'dragleave') {
      setIsDragActive(false);
    }
  }, []);

  const handleDrop = useCallback((e) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragActive(false);
    
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      const file = e.dataTransfer.files[0];
      if (file.type === 'application/pdf') {
        onUpload(file);
      }
    }
  }, [onUpload]);

  const handleChange = (e) => {
    e.preventDefault();
    if (e.target.files && e.target.files[0]) {
      onUpload(e.target.files[0]);
    }
  };

  return (
    <aside className="sidebar">
      <div className="sidebar-header">
        <BookOpen size={28} className="upload-icon" style={{ marginBottom: 0 }} />
        <h1>AI Tutor</h1>
      </div>

      <div 
        className={`upload-zone glass-panel ${isDragActive ? 'drag-active' : ''} ${isUploading ? 'animate-pulse' : ''}`}
        onDragEnter={handleDrag}
        onDragLeave={handleDrag}
        onDragOver={handleDrag}
        onDrop={handleDrop}
        onClick={() => document.getElementById('file-upload').click()}
      >
        <input 
          id="file-upload" 
          type="file" 
          accept=".pdf" 
          onChange={handleChange} 
          style={{ display: 'none' }} 
        />
        <UploadCloud size={48} className="upload-icon" />
        <p className="upload-text">
          {isUploading ? 'Processing PDF...' : (
            <>
              <strong>Click to upload</strong> or drag and drop<br/><br/>PDF Chapter files only
            </>
          )}
        </p>
      </div>

      {currentFileName && !isUploading && !uploadError && (
        <div className="file-status success animate-fade-in">
          <CheckCircle size={20} />
          <span>Ready: {currentFileName}</span>
        </div>
      )}

      {uploadError && (
        <div className="file-status error animate-fade-in">
          <AlertCircle size={20} />
          <span>{uploadError}</span>
        </div>
      )}
    </aside>
  );
}
