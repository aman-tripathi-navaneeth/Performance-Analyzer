import React from 'react';
import { useNavigate } from 'react-router-dom';
import Header from '../components/common/Header';
import './NotFoundPage.css';

/**
 * NotFoundPage Component - 404 error page for invalid routes
 * Provides helpful navigation options when users reach non-existent pages
 */
const NotFoundPage = () => {
  const navigate = useNavigate();

  const handleGoHome = () => {
    navigate('/');
  };

  const handleGoBack = () => {
    window.history.back();
  };

  return (
    <div className="not-found-page">
      <Header />
      
      <div className="not-found-container">
        <div className="not-found-content">
          {/* Error Illustration */}
          <div className="error-illustration">
            <div className="error-code">404</div>
            <div className="error-icon">🔍</div>
          </div>

          {/* Error Message */}
          <div className="error-message">
            <h1 className="error-title">Page Not Found</h1>
            <p className="error-description">
              Sorry, we couldn't find the page you're looking for. 
              The page might have been moved, deleted, or you entered the wrong URL.
            </p>
          </div>

          {/* Action Buttons */}
          <div className="error-actions">
            <button 
              className="btn btn-primary"
              onClick={handleGoHome}
            >
              <span>🏠</span>
              Go to Dashboard
            </button>
            
            <button 
              className="btn btn-secondary"
              onClick={handleGoBack}
            >
              <span>←</span>
              Go Back
            </button>
          </div>

          {/* Helpful Links */}
          <div className="helpful-links">
            <h3 className="links-title">You might be looking for:</h3>
            <div className="links-grid">
              <button 
                className="link-card"
                onClick={() => navigate('/')}
              >
                <span className="link-icon">📊</span>
                <span className="link-label">Dashboard</span>
                <span className="link-description">View class performance overview</span>
              </button>
              
              <button 
                className="link-card"
                onClick={() => navigate('/students')}
              >
                <span className="link-icon">👥</span>
                <span className="link-label">Students</span>
                <span className="link-description">Browse all students</span>
              </button>
              
              <button 
                className="link-card"
                onClick={() => navigate('/upload')}
              >
                <span className="link-icon">📤</span>
                <span className="link-label">Upload Data</span>
                <span className="link-description">Upload new assessment data</span>
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default NotFoundPage;