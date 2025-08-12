import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { Chart as ChartJS, ArcElement, Tooltip, Legend, CategoryScale, LinearScale, BarElement } from 'chart.js';
import { Doughnut, Bar } from 'react-chartjs-2';

ChartJS.register(ArcElement, Tooltip, Legend, CategoryScale, LinearScale, BarElement);

const Results = () => {
  const [results, setResults] = useState([]);
  const [selectedResult, setSelectedResult] = useState(null);

  useEffect(() => {
    const storedResults = JSON.parse(localStorage.getItem('analysisResults') || '[]');
    setResults(storedResults);
    if (storedResults.length > 0) {
      setSelectedResult(storedResults[0]);
    }
  }, []);

  const getPredictionColor = (prediction) => {
    switch (prediction) {
      case 'Normal':
        return '#28a745';
      case 'Cyst':
        return '#ffc107';
      case 'Stone':
        return '#dc3545';
      case 'Tumor':
        return '#17a2b8';
      default:
        return '#6c757d';
    }
  };

  const formatDate = (timestamp) => {
    return new Date(timestamp).toLocaleString();
  };

  const getDoughnutData = (result) => {
    const labels = Object.keys(result.all_probabilities);
    const data = Object.values(result.all_probabilities);
    const colors = labels.map(label => getPredictionColor(label));

    return {
      labels,
      datasets: [
        {
          data,
          backgroundColor: colors,
          borderColor: colors.map(color => color + '80'),
          borderWidth: 2,
        },
      ],
    };
  };

  const getBarData = (result) => {
    const labels = Object.keys(result.all_probabilities);
    const data = Object.values(result.all_probabilities);
    const colors = labels.map(label => getPredictionColor(label));

    return {
      labels,
      datasets: [
        {
          label: 'Confidence Score',
          data,
          backgroundColor: colors,
          borderColor: colors,
          borderWidth: 1,
        },
      ],
    };
  };

  const barOptions = {
    responsive: true,
    plugins: {
      legend: {
        display: false,
      },
    },
    scales: {
      y: {
        beginAtZero: true,
        max: 1,
        ticks: {
          callback: function(value) {
            return (value * 100).toFixed(0) + '%';
          }
        }
      },
    },
  };

  const doughnutOptions = {
    responsive: true,
    plugins: {
      legend: {
        position: 'bottom',
      },
      tooltip: {
        callbacks: {
          label: function(context) {
            return context.label + ': ' + (context.parsed * 100).toFixed(1) + '%';
          }
        }
      }
    },
  };

  return (
    <div>
      <div className="card">
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '24px' }}>
          <h1 style={{ color: '#333', margin: 0 }}>Analysis Results</h1>
          <Link to="/upload" className="btn btn-primary">
            Upload New Image
          </Link>
        </div>

        {results.length === 0 ? (
          <div style={{ textAlign: 'center', padding: '40px' }}>
            <div style={{ fontSize: '48px', color: '#dee2e6', marginBottom: '16px' }}>
              📊
            </div>
            <h3 style={{ color: '#666', marginBottom: '16px' }}>No Results Yet</h3>
            <p style={{ color: '#999', marginBottom: '24px' }}>
              Upload a CT scan image to see analysis results here
            </p>
            <Link to="/upload" className="btn btn-primary">
              Upload Your First Image
            </Link>
          </div>
        ) : (
          <div style={{ display: 'grid', gridTemplateColumns: '300px 1fr', gap: '32px' }}>
            {/* Results List */}
            <div>
              <h3 style={{ marginBottom: '16px', color: '#333' }}>Previous Analyses</h3>
              <div style={{ maxHeight: '500px', overflowY: 'auto' }}>
                {results.map((result, index) => (
                  <div
                    key={index}
                    onClick={() => setSelectedResult(result)}
                    style={{
                      padding: '16px',
                      border: `2px solid ${selectedResult === result ? '#667eea' : '#e9ecef'}`,
                      borderRadius: '8px',
                      marginBottom: '12px',
                      cursor: 'pointer',
                      backgroundColor: selectedResult === result ? '#f8f9ff' : 'white',
                      transition: 'all 0.3s ease'
                    }}
                  >
                    <div style={{ 
                      display: 'flex', 
                      justifyContent: 'space-between', 
                      alignItems: 'center',
                      marginBottom: '8px'
                    }}>
                      <span style={{ 
                        fontWeight: '500', 
                        color: getPredictionColor(result.prediction)
                      }}>
                        {result.prediction}
                      </span>
                      <span style={{ 
                        fontSize: '14px', 
                        color: '#666',
                        backgroundColor: '#f8f9fa',
                        padding: '2px 8px',
                        borderRadius: '4px'
                      }}>
                        {(result.confidence * 100).toFixed(1)}%
                      </span>
                    </div>
                    <p style={{ 
                      fontSize: '12px', 
                      color: '#999', 
                      margin: '0 0 4px 0',
                      overflow: 'hidden',
                      textOverflow: 'ellipsis',
                      whiteSpace: 'nowrap'
                    }}>
                      {result.filename}
                    </p>
                    <p style={{ fontSize: '12px', color: '#999', margin: 0 }}>
                      {formatDate(result.timestamp)}
                    </p>
                  </div>
                ))}
              </div>
            </div>

            {/* Selected Result Details */}
            {selectedResult && (
              <div>
                <h3 style={{ marginBottom: '24px', color: '#333' }}>Analysis Details</h3>
                
                <div className="result-card">
                  <h2 style={{ marginBottom: '8px' }}>
                    {selectedResult.prediction}
                  </h2>
                  <p style={{ fontSize: '18px', marginBottom: '24px', opacity: 0.9 }}>
                    Confidence: {(selectedResult.confidence * 100).toFixed(1)}%
                  </p>
                  
                  <div style={{ 
                    display: 'grid', 
                    gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', 
                    gap: '16px',
                    marginBottom: '24px'
                  }}>
                    {Object.entries(selectedResult.all_probabilities).map(([label, probability]) => (
                      <div key={label}>
                        <div style={{ 
                          display: 'flex', 
                          justifyContent: 'space-between',
                          marginBottom: '4px'
                        }}>
                          <span>{label}</span>
                          <span>{(probability * 100).toFixed(1)}%</span>
                        </div>
                        <div className="confidence-bar">
                          <div 
                            className="confidence-fill"
                            style={{ 
                              width: `${probability * 100}%`,
                              backgroundColor: getPredictionColor(label)
                            }}
                          ></div>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>

                <div style={{ 
                  display: 'grid', 
                  gridTemplateColumns: '1fr 1fr', 
                  gap: '24px',
                  marginTop: '24px'
                }}>
                  <div className="card">
                    <h4 style={{ marginBottom: '16px', color: '#333' }}>Confidence Distribution</h4>
                    <div style={{ height: '300px' }}>
                      <Doughnut data={getDoughnutData(selectedResult)} options={doughnutOptions} />
                    </div>
                  </div>
                  
                  <div className="card">
                    <h4 style={{ marginBottom: '16px', color: '#333' }}>Confidence Comparison</h4>
                    <div style={{ height: '300px' }}>
                      <Bar data={getBarData(selectedResult)} options={barOptions} />
                    </div>
                  </div>
                </div>

                <div className="card">
                  <h4 style={{ marginBottom: '16px', color: '#333' }}>Analysis Information</h4>
                  <div style={{ 
                    display: 'grid', 
                    gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', 
                    gap: '16px'
                  }}>
                    <div>
                      <p style={{ margin: '0 0 4px 0', color: '#666', fontSize: '14px' }}>
                        File Name
                      </p>
                      <p style={{ margin: 0, fontWeight: '500' }}>
                        {selectedResult.filename}
                      </p>
                    </div>
                    <div>
                      <p style={{ margin: '0 0 4px 0', color: '#666', fontSize: '14px' }}>
                        Analysis Date
                      </p>
                      <p style={{ margin: 0, fontWeight: '500' }}>
                        {formatDate(selectedResult.timestamp)}
                      </p>
                    </div>
                    <div>
                      <p style={{ margin: '0 0 4px 0', color: '#666', fontSize: '14px' }}>
                        Model Used
                      </p>
                      <p style={{ margin: 0, fontWeight: '500' }}>
                        MobileNetV2
                      </p>
                    </div>
                  </div>
                </div>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
};

export default Results;
