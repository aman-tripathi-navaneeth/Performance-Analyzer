import React from 'react';
import PropTypes from 'prop-types';
import './StatCard.css';

/**
 * StatCard Component - Reusable card for displaying key metrics
 * Used on dashboard and other pages to highlight important statistics
 */
const StatCard = ({ 
  title, 
  value, 
  subtitle, 
  icon, 
  trend, 
  trendValue, 
  color = 'default',
  size = 'medium',
  loading = false,
  onClick,
  className = ''
}) => {
  // Determine card classes based on props
  const cardClasses = [
    'stat-card',
    `stat-card-${color}`,
    `stat-card-${size}`,
    onClick ? 'stat-card-clickable' : '',
    loading ? 'stat-card-loading' : '',
    className
  ].filter(Boolean).join(' ');

  // Format large numbers for better readability
  const formatValue = (val) => {
    if (loading) return '...';
    if (typeof val !== 'number') return val;
    
    if (val >= 1000000) {
      return (val / 1000000).toFixed(1) + 'M';
    } else if (val >= 1000) {
      return (val / 1000).toFixed(1) + 'K';
    }
    return val.toLocaleString();
  };

  // Determine trend icon and class
  const getTrendDisplay = () => {
    if (!trend || !trendValue) return null;
    
    const trendClass = trend === 'up' ? 'trend-up' : trend === 'down' ? 'trend-down' : 'trend-neutral';
    const trendIcon = trend === 'up' ? '↗️' : trend === 'down' ? '↘️' : '➡️';
    
    return (
      <div className={`stat-trend ${trendClass}`}>
        <span className="trend-icon" aria-hidden="true">{trendIcon}</span>
        <span className="trend-value">{trendValue}</span>
      </div>
    );
  };

  // Handle card click
  const handleClick = () => {
    if (onClick && !loading) {
      onClick();
    }
  };

  // Handle keyboard interaction
  const handleKeyDown = (e) => {
    if ((e.key === 'Enter' || e.key === ' ') && onClick && !loading) {
      e.preventDefault();
      onClick();
    }
  };

  return (
    <div 
      className={cardClasses}
      onClick={handleClick}
      onKeyDown={handleKeyDown}
      role={onClick ? 'button' : undefined}
      tabIndex={onClick ? 0 : undefined}
      aria-label={onClick ? `${title}: ${value}. Click for more details.` : undefined}
    >
      {/* Loading Overlay */}
      {loading && (
        <div className="stat-card-loading-overlay">
          <div className="loading-spinner"></div>
        </div>
      )}

      {/* Card Header */}
      <div className="stat-card-header">
        {icon && (
          <div className="stat-icon" aria-hidden="true">
            {typeof icon === 'string' ? <span>{icon}</span> : icon}
          </div>
        )}
        <h3 className="stat-title">{title}</h3>
      </div>

      {/* Card Body */}
      <div className="stat-card-body">
        <div className="stat-value-container">
          <span className="stat-value" aria-label={`Value: ${value}`}>
            {formatValue(value)}
          </span>
          {getTrendDisplay()}
        </div>
        
        {subtitle && (
          <p className="stat-subtitle">{subtitle}</p>
        )}
      </div>

      {/* Click indicator for interactive cards */}
      {onClick && !loading && (
        <div className="stat-card-click-indicator" aria-hidden="true">
          <span>→</span>
        </div>
      )}
    </div>
  );
};

// PropTypes for type checking and documentation
StatCard.propTypes = {
  /** Main title/label for the statistic */
  title: PropTypes.string.isRequired,
  
  /** The main value to display (number or string) */
  value: PropTypes.oneOfType([PropTypes.number, PropTypes.string]).isRequired,
  
  /** Optional subtitle or description */
  subtitle: PropTypes.string,
  
  /** Icon to display (emoji string or React component) */
  icon: PropTypes.oneOfType([PropTypes.string, PropTypes.node]),
  
  /** Trend direction: 'up', 'down', or 'neutral' */
  trend: PropTypes.oneOf(['up', 'down', 'neutral']),
  
  /** Trend value to display (e.g., '+5%', '-2.3%') */
  trendValue: PropTypes.string,
  
  /** Color theme for the card */
  color: PropTypes.oneOf(['default', 'primary', 'success', 'warning', 'error', 'info']),
  
  /** Size variant of the card */
  size: PropTypes.oneOf(['small', 'medium', 'large']),
  
  /** Loading state */
  loading: PropTypes.bool,
  
  /** Click handler function */
  onClick: PropTypes.func,
  
  /** Additional CSS classes */
  className: PropTypes.string
};

// Default props
StatCard.defaultProps = {
  color: 'default',
  size: 'medium',
  loading: false,
  className: ''
};

export default StatCard;