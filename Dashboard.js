import React from 'react';
import { Link } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

const Dashboard = () => {
  const { user } = useAuth();

  return (
    <div>
      <div className="card">
        <h1 style={{ marginBottom: '16px', color: '#333' }}>
          Welcome back, {user?.name}!
        </h1>
        <p style={{ color: '#666', fontSize: '18px', marginBottom: '32px' }}>
          AI-powered Kidney Anomaly Detection System
        </p>
        
        <div style={{ 
          display: 'grid', 
          gridTemplateColumns: 'repeat(auto-fit, minmax(250px, 1fr))', 
          gap: '24px',
          marginBottom: '32px'
        }}>
          <div style={{ 
            padding: '24px', 
            backgroundColor: '#f8f9ff', 
            borderRadius: '12px',
            border: '2px solid #e8ecff'
          }}>
            <h3 style={{ color: '#667eea', marginBottom: '8px' }}>Upload CT Scan</h3>
            <p style={{ color: '#666', marginBottom: '16px' }}>
              Upload a kidney CT scan image for AI analysis
            </p>
            <Link to="/upload" className="btn btn-primary">
              Upload Now
            </Link>
          </div>
          
          <div style={{ 
            padding: '24px', 
            backgroundColor: '#fff5f5', 
            borderRadius: '12px',
            border: '2px solid #fed7d7'
          }}>
            <h3 style={{ color: '#e53e3e', marginBottom: '8px' }}>View Results</h3>
            <p style={{ color: '#666', marginBottom: '16px' }}>
              Check your previous analysis results
            </p>
            <Link to="/results" className="btn btn-secondary">
              View Results
            </Link>
          </div>
        </div>
      </div>
      
      <div className="card">
        <h2 style={{ marginBottom: '24px', color: '#333' }}>How It Works</h2>
        
        <div style={{ 
          display: 'grid', 
          gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', 
          gap: '24px'
        }}>
          <div style={{ textAlign: 'center' }}>
            <div style={{ 
              width: '60px', 
              height: '60px', 
              backgroundColor: '#667eea', 
              borderRadius: '50%', 
              display: 'flex', 
              alignItems: 'center', 
              justifyContent: 'center',
              margin: '0 auto 16px',
              color: 'white',
              fontSize: '24px',
              fontWeight: 'bold'
            }}>
              1
            </div>
            <h4 style={{ marginBottom: '8px', color: '#333' }}>Upload Image</h4>
            <p style={{ color: '#666', fontSize: '14px' }}>
              Upload your kidney CT scan image in JPG, PNG, or JPEG format
            </p>
          </div>
          
          <div style={{ textAlign: 'center' }}>
            <div style={{ 
              width: '60px', 
              height: '60px', 
              backgroundColor: '#667eea', 
              borderRadius: '50%', 
              display: 'flex', 
              alignItems: 'center', 
              justifyContent: 'center',
              margin: '0 auto 16px',
              color: 'white',
              fontSize: '24px',
              fontWeight: 'bold'
            }}>
              2
            </div>
            <h4 style={{ marginBottom: '8px', color: '#333' }}>AI Analysis</h4>
            <p style={{ color: '#666', fontSize: '14px' }}>
              Our MobileNetV2 model analyzes the image for anomalies
            </p>
          </div>
          
          <div style={{ textAlign: 'center' }}>
            <div style={{ 
              width: '60px', 
              height: '60px', 
              backgroundColor: '#667eea', 
              borderRadius: '50%', 
              display: 'flex', 
              alignItems: 'center', 
              justifyContent: 'center',
              margin: '0 auto 16px',
              color: 'white',
              fontSize: '24px',
              fontWeight: 'bold'
            }}>
              3
            </div>
            <h4 style={{ marginBottom: '8px', color: '#333' }}>Get Results</h4>
            <p style={{ color: '#666', fontSize: '14px' }}>
              Receive detailed analysis with confidence scores
            </p>
          </div>
        </div>
      </div>
      
      <div className="card">
        <h2 style={{ marginBottom: '24px', color: '#333' }}>Detection Classes</h2>
        
        <div style={{ 
          display: 'grid', 
          gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', 
          gap: '16px'
        }}>
          <div style={{ 
            padding: '16px', 
            backgroundColor: '#d4edda', 
            borderRadius: '8px',
            border: '1px solid #c3e6cb'
          }}>
            <h4 style={{ color: '#155724', marginBottom: '4px' }}>Normal</h4>
            <p style={{ color: '#155724', fontSize: '14px', margin: 0 }}>
              Healthy kidney tissue with no abnormalities
            </p>
          </div>
          
          <div style={{ 
            padding: '16px', 
            backgroundColor: '#fff3cd', 
            borderRadius: '8px',
            border: '1px solid #ffeaa7'
          }}>
            <h4 style={{ color: '#856404', marginBottom: '4px' }}>Cyst</h4>
            <p style={{ color: '#856404', fontSize: '14px', margin: 0 }}>
              Fluid-filled sacs in the kidney tissue
            </p>
          </div>
          
          <div style={{ 
            padding: '16px', 
            backgroundColor: '#f8d7da', 
            borderRadius: '8px',
            border: '1px solid #f5c6cb'
          }}>
            <h4 style={{ color: '#721c24', marginBottom: '4px' }}>Stone</h4>
            <p style={{ color: '#721c24', fontSize: '14px', margin: 0 }}>
              Hard mineral deposits in the kidney
            </p>
          </div>
          
          <div style={{ 
            padding: '16px', 
            backgroundColor: '#d1ecf1', 
            borderRadius: '8px',
            border: '1px solid #bee5eb'
          }}>
            <h4 style={{ color: '#0c5460', marginBottom: '4px' }}>Tumor</h4>
            <p style={{ color: '#0c5460', fontSize: '14px', margin: 0 }}>
              Abnormal growth of cells in the kidney
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
