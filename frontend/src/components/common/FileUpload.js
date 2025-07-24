import React, { useState, useRef } from 'react';
import PropTypes from 'prop-types';
import './FileUpload.css';

/**
 * FileUpload Component - Reusable file upload component with drag & drop support
 * Handles file selection and validation with callback to parent component
 */
const FileUpload = ({
  onFileSelect,
  acceptedTypes = '.xlsx,.xls,.csv',
  maxSize = 10 * 1024 * 1024, // 10MB default
  multiple = false,
  disabled = false,
  className = ''
}) => {
  // Component state
  const [selectedFile, setSelectedFile] = useState(null);
  const [dragActive, setDragActive] = useState(false);
  const [error, setError] = useState('');
  
  // File input reference
  const fileInputRef = useRef(null);

  // Validate file
  const validateFile = (file) => {
    // Check file size
    if (file.size > maxSize) {
      return `File size must be less than ${formatFileSize(maxSize)}`;
    }

    // Check file type
    const fileExtension = '.' + file.name.split('.').pop().toLowerCase();
    const acceptedExtensions = acceptedTypes.split(',').map(type => type.trim().toLowerCase());
    
    if (!acceptedExtensions.includes(fileExtension)) {
      return `File type not supported. Accepted types: ${acceptedTypes}`;
    }

    return null;
  };

  // Handle file selection
  const handleFileSelect = (files) => {
    const file = files[0]; // Take first file even if multiple is true
    
    if (!file) return;

    // Validate file
    const validationError = validateFile(file);
    if (validationError) {
      setError(validationError);
      setSelectedFile(null);
      return;
    }

    // Clear any previous errors
    setError('');
    setSelectedFile(file);
    
    // Call parent callback
    if (onFileSelect) {
      onFileSelect(file);
    }
  };

  // Handle file input change
  const handleInputChange = (e) => {
    handleFileSelect(e.target.files);
  };

  // Handle drag events
  const handleDrag = (e) => {
    e.preventDefault();
    e.stopPropagation();
  };

  const handleDragIn = (e) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.dataTransfer.items && e.dataTransfer.items.length > 0) {
      setDragActive(true);
    }
  };

  const handleDragOut = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);
  };

  const handleDrop = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);
    
    if (e.dataTransfer.files && e.dataTransfer.files.length > 0) {
      handleFileSelect(e.dataTransfer.files);
    }
  };

  // Open file dialog
  const openFileDialog = () => {
    if (!disabled && fileInputRef.current) {
      fileInputRef.current.click();
    }
  };

  // Remove selected file
  const removeFile = () => {
    setSelectedFile(null);
    setError('');
    if (fileInputRef.current) {
      fileInputRef.current.value = '';
    }
    if (onFileSelect) {
      onFileSelect(null);
    }
  };

  // Format file size for display
  const formatFileSize = (bytes) => {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
  };

  // Get file icon based on extension
  const getFileIcon = (fileName) => {
    const extension = fileName.split('.').pop().toLowerCase();
    switch (extension) {
      case 'xlsx':
      case 'xls':
        return '📊';
      case 'csv':
        return '📋';
      default:
        return '📄';
    }
  };

  return (
    <div className={`file-upload-container ${className}`}>
      {/* Hidden file input */}
      <input
        ref={fileInputRef}
        type="file"
        accept={acceptedTypes}
        multiple={multiple}
        onChange={handleInputChange}
        className="file-input-hidden"
        disabled={disabled}
      />

      {/* Drop zone */}
      <div
        className={`file-drop-zone ${dragActive ? 'drag-active' : ''} ${disabled ? 'disabled' : ''} ${selectedFile ? 'has-file' : ''}`}
        onDragEnter={handleDragIn}
        onDragLeave={handleDragOut}
        onDragOver={handleDrag}
        onDrop={handleDrop}
        onClick={openFileDialog}
      >
        {!selectedFile ? (
          <div className="drop-zone-content">
            <div className="upload-icon">📤</div>
            <div className="upload-text">
              <p className="upload-primary">
                {dragActive ? 'Drop file here' : 'Click to upload or drag and drop'}
              </p>
              <p className="upload-secondary">
                Supported formats: {acceptedTypes.replace(/\./g, '').toUpperCase()}
              </p>
              <p className="upload-size">
                Maximum file size: {formatFileSize(maxSize)}
              </p>
            </div>
          </div>
        ) : (
          <div className="selected-file">
            <div className="file-info">
              <div className="file-icon">
                {getFileIcon(selectedFile.name)}
              </div>
              <div className="file-details">
                <p className="file-name">{selectedFile.name}</p>
                <p className="file-size">{formatFileSize(selectedFile.size)}</p>
              </div>
            </div>
            <button
              type="button"
              className="remove-file-btn"
              onClick={(e) => {
                e.stopPropagation();
                removeFile();
              }}
              disabled={disabled}
            >
              ✕
            </button>
          </div>
        )}
      </div>

      {/* Error message */}
      {error && (
        <div className="file-upload-error">
          <span className="error-icon">⚠️</span>
          <span className="error-text">{error}</span>
        </div>
      )}

      {/* Upload button */}
      {selectedFile && !error && (
        <div className="upload-actions">
          <button
            type="button"
            className="btn btn-outline"
            onClick={removeFile}
            disabled={disabled}
          >
            Remove File
          </button>
          <button
            type="button"
            className="btn btn-primary upload-btn"
            onClick={openFileDialog}
            disabled={disabled}
          >
            <span>📁</span>
            Choose Different File
          </button>
        </div>
      )}

      {/* File requirements */}
      <div className="file-requirements">
        <h4 className="requirements-title">File Requirements:</h4>
        <ul className="requirements-list">
          <li>Excel files (.xlsx, .xls) or CSV files (.csv)</li>
          <li>Maximum file size: {formatFileSize(maxSize)}</li>
          <li>File should contain student data with proper column headers</li>
          <li>Ensure data is properly formatted before uploading</li>
        </ul>
      </div>
    </div>
  );
};

// PropTypes for type checking
FileUpload.propTypes = {
  /** Callback function called when file is selected */
  onFileSelect: PropTypes.func.isRequired,
  
  /** Accepted file types (comma-separated) */
  acceptedTypes: PropTypes.string,
  
  /** Maximum file size in bytes */
  maxSize: PropTypes.number,
  
  /** Allow multiple file selection */
  multiple: PropTypes.bool,
  
  /** Disable the component */
  disabled: PropTypes.bool,
  
  /** Additional CSS classes */
  className: PropTypes.string
};

export default FileUpload;