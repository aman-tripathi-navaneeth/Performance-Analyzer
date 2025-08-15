import React, { useState } from 'react';
import './BacklogChecker.css';

const BacklogChecker = () => {
  const [rollNumber, setRollNumber] = useState('');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  const checkBacklogs = async () => {
    if (!rollNumber.trim()) {
      setError('Please enter a roll number');
      return;
    }

    setLoading(true);
    setError(null);
    setResult(null);

    try {
      const response = await fetch(`${process.env.REACT_APP_API_URL || 'http://localhost:5000'}/api/v1/sis/check-backlogs`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          roll_number: rollNumber.trim(),
          password: rollNumber.trim() // Using roll number as password
        })
      });

      const data = await response.json();

      if (data.success) {
        setResult(data.data);
      } else {
        setError(data.error || 'Failed to check backlogs');
      }
    } catch (err) {
      console.error('Error checking backlogs:', err);
      setError('Network error. Please check your connection and try again.');
    } finally {
      setLoading(false);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter') {
      checkBacklogs();
    }
  };

  const getStatusColor = (status) => {
    switch (status) {
      case 'clear': return '#10b981';
      case 'backlogs_present': return '#ef4444';
      default: return '#6b7280';
    }
  };

  const getStatusIcon = (status) => {
    switch (status) {
      case 'clear': return '✅';
      case 'backlogs_present': return '⚠️';
      default: return '❓';
    }
  };

  const getStatusText = (status) => {
    switch (status) {
      case 'clear': return 'No Backlogs';
      case 'backlogs_present': return 'Backlogs Present';
      default: return 'Unknown';
    }
  };

  return (
    <div className="backlog-checker">
      <div className="checker-header">
        <h2>🎓 Student Backlog Checker</h2>
        <p>Enter a roll number to check backlog status from college SIS portal</p>
      </div>

      <div className="checker-input">
        <div className="input-group">
          <input
            type="text"
            placeholder="Enter roll number (e.g., 226K1A0546)"
            value={rollNumber}
            onChange={(e) => setRollNumber(e.target.value)}
            onKeyPress={handleKeyPress}
            className="roll-input"
            disabled={loading}
          />
          <button 
            onClick={checkBacklogs}
            disabled={loading || !rollNumber.trim()}
            className="check-button"
          >
            {loading ? (
              <>
                <span className="spinner"></span>
                Checking...
              </>
            ) : (
              'Check Backlogs'
            )}
          </button>
        </div>
      </div>

      {error && (
        <div className="error-message">
          <span className="error-icon">❌</span>
          <span>{error}</span>
        </div>
      )}

      {result && (
        <div className="result-container">
          <div className="result-header">
            <div className="status-indicator">
              <span className="status-icon">{getStatusIcon(result.overall_status)}</span>
              <div className="status-info">
                <h3>Roll Number: {result.roll_number}</h3>
                <p 
                  className="status-text"
                  style={{ color: getStatusColor(result.overall_status) }}
                >
                  {getStatusText(result.overall_status)}
                </p>
              </div>
            </div>
          </div>

          <div className="result-stats">
            <div className="stat-card">
              <div className="stat-value">{result.total_subjects}</div>
              <div className="stat-label">Total Subjects</div>
            </div>
            <div className="stat-card">
              <div className="stat-value">{result.passed_subjects}</div>
              <div className="stat-label">Passed</div>
            </div>
            <div className="stat-card">
              <div className="stat-value" style={{ color: result.backlog_count > 0 ? '#ef4444' : '#10b981' }}>
                {result.backlog_count}
              </div>
              <div className="stat-label">Backlogs</div>
            </div>
          </div>

          {result.backlogs && result.backlogs.length > 0 && (
            <div className="backlogs-section">
              <h4>📋 Backlog Details</h4>
              <div className="backlogs-list">
                {result.backlogs.map((backlog, index) => (
                  <div key={index} className="backlog-item">
                    <div className="backlog-header">
                      <span className="subject-name">{backlog.subject_name}</span>
                      <span className="subject-code">{backlog.subject_code}</span>
                    </div>
                    <div className="backlog-details">
                      <span className="semester">{backlog.semester}</span>
                      <span className="marks">Marks: {backlog.marks}</span>
                      <span className="grade">Grade: {backlog.grade}</span>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}

          {result.overall_status === 'clear' && (
            <div className="success-message">
              <span className="success-icon">🎉</span>
              <span>Congratulations! No backlogs found. Keep up the good work!</span>
            </div>
          )}
        </div>
      )}

      <div className="checker-info">
        <h4>ℹ️ How it works:</h4>
        <ul>
          <li>Connects to college SIS portal (sis.idealtech.edu.in)</li>
          <li>Uses roll number as both username and password</li>
          <li>Fetches and analyzes academic results</li>
          <li>Identifies subjects with failing grades</li>
          <li>Currently in demo mode for testing</li>
        </ul>
      </div>
    </div>
  );
};

export default BacklogChecker;