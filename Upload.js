import React, { useState, useCallback } from 'react';
import { useDropzone } from 'react-dropzone';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import { toast } from 'react-toastify';

const Upload = () => {
  const [uploadedFile, setUploadedFile] = useState(null);
  const [preview, setPreview] = useState(null);
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const onDrop = useCallback((acceptedFiles) => {
    const file = acceptedFiles[0];
    if (file) {
      setUploadedFile(file);
      
      // Create preview
      const reader = new FileReader();
      reader.onload = () => {
        setPreview(reader.result);
      };
      reader.readAsDataURL(file);
    }
  }, []);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'image/*': ['.jpeg', '.jpg', '.png']
    },
    multiple: false,
    maxSize: 16 * 1024 * 1024 // 16MB
  });

  const handleUpload = async () => {
    if (!uploadedFile) {
      toast.error('Please select a file first');
      return;
    }

    setLoading(true);
    
    const formData = new FormData();
    formData.append('image', uploadedFile);

    try {
      const response = await axios.post('/api/predict', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });

      // Store result in localStorage for the results page
      const result = {
        ...response.data,
        timestamp: new Date().toISOString(),
        filename: uploadedFile.name
      };
      
      const existingResults = JSON.parse(localStorage.getItem('analysisResults') || '[]');
      existingResults.unshift(result);
      localStorage.setItem('analysisResults', JSON.stringify(existingResults));

      toast.success('Analysis completed successfully!');
      navigate('/results');
      
    } catch (error) {
      console.error('Upload error:', error);
      toast.error(error.response?.data?.error || 'Upload failed. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const removeFile = () => {
    setUploadedFile(null);
    setPreview(null);
  };

  return (
    <div>
      <div className="card">
        <h1 style={{ marginBottom: '16px', color: '#333' }}>
          Upload CT Scan Image
        </h1>
        <p style={{ color: '#666', marginBottom: '32px' }}>
          Upload a kidney CT scan image for AI-powered anomaly detection
        </p>

        <div style={{ 
          display: 'grid', 
          gridTemplateColumns: '1fr 1fr', 
          gap: '32px',
          alignItems: 'start'
        }}>
          <div>
            <div
              {...getRootProps()}
              className={`dropzone ${isDragActive ? 'drag-active' : ''}`}
            >
              <input {...getInputProps()} />
              {isDragActive ? (
                <div>
                  <p style={{ fontSize: '18px', color: '#667eea', marginBottom: '8px' }}>
                    Drop the image here...
                  </p>
                  <p style={{ color: '#666' }}>Release to upload</p>
                </div>
              ) : (
                <div>
                  <div style={{ 
                    fontSize: '48px', 
                    color: '#667eea', 
                    marginBottom: '16px' 
                  }}>
                    📁
                  </div>
                  <p style={{ fontSize: '18px', color: '#667eea', marginBottom: '8px' }}>
                    Drag & drop an image here
                  </p>
                  <p style={{ color: '#666', marginBottom: '16px' }}>
                    or click to select a file
                  </p>
                  <p style={{ fontSize: '14px', color: '#999' }}>
                    Supports: JPG, PNG, JPEG (Max: 16MB)
                  </p>
                </div>
              )}
            </div>

            {uploadedFile && (
              <div style={{ marginTop: '16px' }}>
                <div style={{ 
                  display: 'flex', 
                  justifyContent: 'space-between', 
                  alignItems: 'center',
                  padding: '12px',
                  backgroundColor: '#f8f9fa',
                  borderRadius: '8px'
                }}>
                  <div>
                    <p style={{ margin: '0 0 4px 0', fontWeight: '500' }}>
                      {uploadedFile.name}
                    </p>
                    <p style={{ margin: 0, fontSize: '14px', color: '#666' }}>
                      {(uploadedFile.size / 1024 / 1024).toFixed(2)} MB
                    </p>
                  </div>
                  <button
                    onClick={removeFile}
                    className="btn btn-secondary"
                    style={{ padding: '8px 16px', fontSize: '14px' }}
                  >
                    Remove
                  </button>
                </div>
              </div>
            )}
          </div>

          <div>
            {preview ? (
              <div>
                <h3 style={{ marginBottom: '16px', color: '#333' }}>Image Preview</h3>
                <div style={{ 
                  border: '2px solid #e9ecef', 
                  borderRadius: '12px', 
                  overflow: 'hidden',
                  marginBottom: '24px'
                }}>
                  <img
                    src={preview}
                    alt="Preview"
                    style={{ 
                      width: '100%', 
                      height: 'auto', 
                      display: 'block' 
                    }}
                  />
                </div>
                
                <button
                  onClick={handleUpload}
                  className="btn btn-primary"
                  style={{ width: '100%' }}
                  disabled={loading}
                >
                  {loading ? (
                    <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                      <div className="spinner" style={{ width: '20px', height: '20px', marginRight: '8px' }}></div>
                      Analyzing...
                    </div>
                  ) : (
                    'Analyze Image'
                  )}
                </button>
              </div>
            ) : (
              <div style={{ 
                padding: '40px', 
                textAlign: 'center', 
                backgroundColor: '#f8f9fa',
                borderRadius: '12px',
                border: '2px dashed #dee2e6'
              }}>
                <div style={{ fontSize: '48px', color: '#dee2e6', marginBottom: '16px' }}>
                  🖼️
                </div>
                <p style={{ color: '#666' }}>
                  Image preview will appear here after selection
                </p>
              </div>
            )}
          </div>
        </div>
      </div>

      <div className="card">
        <h2 style={{ marginBottom: '24px', color: '#333' }}>Upload Guidelines</h2>
        
        <div style={{ 
          display: 'grid', 
          gridTemplateColumns: 'repeat(auto-fit, minmax(250px, 1fr))', 
          gap: '24px'
        }}>
          <div>
            <h4 style={{ color: '#667eea', marginBottom: '8px' }}>✅ Supported Formats</h4>
            <ul style={{ color: '#666', margin: 0, paddingLeft: '20px' }}>
              <li>JPEG (.jpg, .jpeg)</li>
              <li>PNG (.png)</li>
              <li>Maximum file size: 16MB</li>
            </ul>
          </div>
          
          <div>
            <h4 style={{ color: '#667eea', marginBottom: '8px' }}>📋 Image Requirements</h4>
            <ul style={{ color: '#666', margin: 0, paddingLeft: '20px' }}>
              <li>Clear, high-quality CT scan images</li>
              <li>Kidney region should be clearly visible</li>
              <li>Avoid blurry or low-resolution images</li>
            </ul>
          </div>
          
          <div>
            <h4 style={{ color: '#667eea', marginBottom: '8px' }}>🔒 Privacy & Security</h4>
            <ul style={{ color: '#666', margin: 0, paddingLeft: '20px' }}>
              <li>Images are processed securely</li>
              <li>No data is stored permanently</li>
              <li>Results are for educational purposes only</li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Upload;
