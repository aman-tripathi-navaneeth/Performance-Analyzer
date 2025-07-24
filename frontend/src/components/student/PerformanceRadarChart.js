import React from 'react';
import {
  RadarChart,
  PolarGrid,
  PolarAngleAxis,
  PolarRadiusAxis,
  Radar,
  ResponsiveContainer,
  Legend,
  Tooltip
} from 'recharts';
import PropTypes from 'prop-types';
import './StudentComponents.css';

/**
 * PerformanceRadarChart Component - Radar chart showing student's performance across subjects
 * Uses recharts to visualize multi-dimensional performance data in a single view
 */
const PerformanceRadarChart = ({
  data = [],
  height = 400,
  showGrid = true,
  showLegend = true,
  colors = ['#3b82f6', '#10b981', '#f59e0b'],
  loading = false,
  error = null,
  className = ''
}) => {
  // Loading state
  if (loading) {
    return (
      <div className={`radar-chart-container ${className}`} style={{ height }}>
        <div className="chart-loading">
          <div className="loading-spinner"></div>
          <p>Loading performance data...</p>
        </div>
      </div>
    );
  }

  // Error state
  if (error) {
    return (
      <div className={`radar-chart-container ${className}`} style={{ height }}>
        <div className="chart-error">
          <div className="error-icon">⚠️</div>
          <p className="error-message">{error}</p>
        </div>
      </div>
    );
  }

  // Empty data state
  if (!data || data.length === 0) {
    return (
      <div className={`radar-chart-container ${className}`} style={{ height }}>
        <div className="chart-empty">
          <div className="empty-icon">🎯</div>
          <p className="empty-message">No subject performance data available</p>
          <p className="empty-subtitle">Subject scores will appear here once assessments are completed</p>
        </div>
      </div>
    );
  }

  // Custom tooltip component
  const CustomTooltip = ({ active, payload, label }) => {
    if (active && payload && payload.length) {
      return (
        <div className="radar-tooltip">
          <p className="tooltip-label">{`Subject: ${label}`}</p>
          {payload.map((entry, index) => (
            <p key={index} className="tooltip-value" style={{ color: entry.color }}>
              {`${entry.name}: ${entry.value}%`}
            </p>
          ))}
        </div>
      );
    }
    return null;
  };

  // Format the data to ensure proper structure
  const formattedData = data.map(item => ({
    subject: item.subject || item.subjectName || 'Unknown',
    score: item.score || item.average || item.percentage || 0,
    classAverage: item.classAverage || 0,
    maxScore: item.maxScore || 100,
    ...item
  }));

  // Calculate performance metrics
  const averageScore = formattedData.length > 0 
    ? formattedData.reduce((sum, item) => sum + item.score, 0) / formattedData.length 
    : 0;

  const strongestSubject = formattedData.reduce((max, item) => 
    item.score > max.score ? item : max, formattedData[0] || { subject: 'N/A', score: 0 });

  const weakestSubject = formattedData.reduce((min, item) => 
    item.score < min.score ? item : min, formattedData[0] || { subject: 'N/A', score: 0 });

  return (
    <div className={`radar-chart-container ${className}`}>
      <div className="radar-chart-wrapper" style={{ height }}>
        <ResponsiveContainer width="100%" height="100%">
          <RadarChart data={formattedData} margin={{ top: 20, right: 30, bottom: 20, left: 30 }}>
            {showGrid && (
              <PolarGrid 
                stroke="#e2e8f0" 
                strokeWidth={1}
                opacity={0.7}
              />
            )}
            
            <PolarAngleAxis 
              dataKey="subject" 
              tick={{ 
                fontSize: 12, 
                fill: '#64748b',
                fontWeight: 500
              }}
              className="radar-angle-axis"
            />
            
            <PolarRadiusAxis
              angle={90}
              domain={[0, 100]}
              tick={{ 
                fontSize: 10, 
                fill: '#94a3b8',
                fontWeight: 400
              }}
              tickFormatter={(value) => `${value}%`}
              className="radar-radius-axis"
            />
            
            <Tooltip content={<CustomTooltip />} />
            
            {showLegend && (
              <Legend 
                wrapperStyle={{ 
                  paddingTop: '20px',
                  fontSize: '12px',
                  color: '#64748b'
                }}
              />
            )}
            
            {/* Student Performance */}
            <Radar
              name="Student Score"
              dataKey="score"
              stroke={colors[0]}
              fill={colors[0]}
              fillOpacity={0.2}
              strokeWidth={3}
              dot={{ 
                fill: colors[0], 
                strokeWidth: 2, 
                r: 4,
                stroke: '#ffffff'
              }}
            />
            
            {/* Class Average (if available) */}
            {formattedData.some(item => item.classAverage > 0) && (
              <Radar
                name="Class Average"
                dataKey="classAverage"
                stroke={colors[1]}
                fill={colors[1]}
                fillOpacity={0.1}
                strokeWidth={2}
                strokeDasharray="5 5"
                dot={{ 
                  fill: colors[1], 
                  strokeWidth: 1, 
                  r: 3,
                  stroke: '#ffffff'
                }}
              />
            )}
          </RadarChart>
        </ResponsiveContainer>
      </div>

      {/* Performance Summary */}
      <div className="radar-summary">
        <div className="summary-stats">
          <div className="summary-item">
            <span className="summary-label">Overall Average:</span>
            <span className="summary-value">{Math.round(averageScore)}%</span>
          </div>
          <div className="summary-item">
            <span className="summary-label">Strongest Subject:</span>
            <span className="summary-value strong">{strongestSubject.subject} ({strongestSubject.score}%)</span>
          </div>
          <div className="summary-item">
            <span className="summary-label">Area for Improvement:</span>
            <span className="summary-value weak">{weakestSubject.subject} ({weakestSubject.score}%)</span>
          </div>
        </div>

        {/* Performance Insights */}
        <div className="performance-insights">
          <h4 className="insights-title">Performance Insights</h4>
          <div className="insights-list">
            {getPerformanceInsights(formattedData, averageScore).map((insight, index) => (
              <div key={index} className={`insight-item ${insight.type}`}>
                <span className="insight-icon">{insight.icon}</span>
                <span className="insight-text">{insight.text}</span>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};

// Helper function to generate performance insights
const getPerformanceInsights = (data, averageScore) => {
  const insights = [];
  
  // Overall performance insight
  if (averageScore >= 85) {
    insights.push({
      type: 'excellent',
      icon: '🌟',
      text: 'Excellent overall performance across all subjects'
    });
  } else if (averageScore >= 75) {
    insights.push({
      type: 'good',
      icon: '👍',
      text: 'Good performance with room for improvement'
    });
  } else if (averageScore >= 60) {
    insights.push({
      type: 'average',
      icon: '📈',
      text: 'Average performance - focus on consistent improvement'
    });
  } else {
    insights.push({
      type: 'needs-improvement',
      icon: '📚',
      text: 'Needs focused attention and additional support'
    });
  }

  // Subject-specific insights
  const strongSubjects = data.filter(item => item.score >= 80);
  const weakSubjects = data.filter(item => item.score < 60);

  if (strongSubjects.length > 0) {
    insights.push({
      type: 'strength',
      icon: '💪',
      text: `Strong performance in ${strongSubjects.length} subject${strongSubjects.length > 1 ? 's' : ''}`
    });
  }

  if (weakSubjects.length > 0) {
    insights.push({
      type: 'improvement',
      icon: '🎯',
      text: `Focus needed in ${weakSubjects.length} subject${weakSubjects.length > 1 ? 's' : ''}`
    });
  }

  // Consistency insight
  const scores = data.map(item => item.score);
  const maxScore = Math.max(...scores);
  const minScore = Math.min(...scores);
  const scoreRange = maxScore - minScore;

  if (scoreRange <= 10) {
    insights.push({
      type: 'consistent',
      icon: '⚖️',
      text: 'Consistent performance across all subjects'
    });
  } else if (scoreRange > 30) {
    insights.push({
      type: 'inconsistent',
      icon: '📊',
      text: 'Performance varies significantly between subjects'
    });
  }

  return insights.slice(0, 4); // Limit to 4 insights
};

// PropTypes for type checking
PerformanceRadarChart.propTypes = {
  /** Array of subject performance data */
  data: PropTypes.arrayOf(
    PropTypes.shape({
      subject: PropTypes.string,
      subjectName: PropTypes.string,
      score: PropTypes.number,
      average: PropTypes.number,
      percentage: PropTypes.number,
      classAverage: PropTypes.number,
      maxScore: PropTypes.number
    })
  ),
  
  /** Height of the chart in pixels */
  height: PropTypes.number,
  
  /** Whether to show grid lines */
  showGrid: PropTypes.bool,
  
  /** Whether to show legend */
  showLegend: PropTypes.bool,
  
  /** Array of colors for different data series */
  colors: PropTypes.arrayOf(PropTypes.string),
  
  /** Loading state */
  loading: PropTypes.bool,
  
  /** Error message to display */
  error: PropTypes.string,
  
  /** Additional CSS classes */
  className: PropTypes.string
};

export default React.memo(PerformanceRadarChart);