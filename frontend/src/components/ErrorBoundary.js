import React from 'react';
import './ErrorBoundary.css';

/**
 * ErrorBoundary Component - Catches JavaScript errors in component tree
 * Provides fallback UI when errors occur to prevent app crashes
 */
class ErrorBoundary extends React.Component {
  constructor(props) {
    super(props);
    this.state = { 
      hasError: false, 
      error: null, 
      errorInfo: null 
    };
  }

  static getDerivedStateFromError(error) {
    // Update state so the next render will show the fallback UI
    return { hasError: true };
  }

  componentDidCatch(error, errorInfo) {
    // Log error details for debugging
    console.error('ErrorBoundary caught an error:', error, errorInfo);
    
    this.setState({
      error: error,
      errorInfo: errorInfo
    });

    // You can also log the error to an error reporting service here
    // logErrorToService(error, errorInfo);
  }

  handleReload = () => {
    // Reset error state and reload the page
    this.setState({ hasError: false, error: null, errorInfo: null });
    window.location.reload();
  };

  handleGoHome = () => {
    // Reset error state and navigate to home
    this.setState({ hasError: false, error: null, errorInfo: null });
    window.location.href = '/';
  };

  render() {
    if (this.state.hasError) {
      return (
        <div className="error-boundary">
          <div className="error-boundary-container">
            <div className="error-icon">⚠️</div>
            <h1 className="error-title">Oops! Something went wrong</h1>
            <p className="error-message">
              We're sorry, but something unexpected happened. The error has been logged 
              and we'll work to fix it as soon as possible.
            </p>
            
            <div className="error-actions">
              <button 
                onClick={this.handleReload}
                className="btn btn-primary"
              >
                Reload Page
              </button>
              <button 
                onClick={this.handleGoHome}
                className="btn btn-secondary"
              >
                Go to Dashboard
              </button>
            </div>

            {/* Show error details in development */}
            {process.env.NODE_ENV === 'development' && (
              <details className="error-details">
                <summary>Error Details (Development Only)</summary>
                <div className="error-stack">
                  <h3>Error:</h3>
                  <pre>{this.state.error && this.state.error.toString()}</pre>
                  
                  <h3>Component Stack:</h3>
                  <pre>{this.state.errorInfo.componentStack}</pre>
                </div>
              </details>
            )}
          </div>
        </div>
      );
    }

    return this.props.children;
  }
}

export default ErrorBoundary;