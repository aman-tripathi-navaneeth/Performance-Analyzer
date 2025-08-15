import React from 'react';
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  Legend,
  Cell
} from 'recharts';
import PropTypes from 'prop-types';
import './ChartComponents.css';

/**
 * SubjectComparisonChart Component - Bar chart comparing performance across subjects
 * Uses recharts to visualize average scores per subject for quick comparison
 */
const SubjectComparisonChart = ({ 
  data = [], 
  height = 300, 
  showGrid = true,
  showLegend = false,
  colorScheme = 'default',
  loading = false,
  error = null,
  sortBy = 'average' // 'average', 'name', or 'none'
}) => {
  // Color schemes for different subjects
  const colorSchemes = {
    default: ['#3b82f6', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6', '#06b6d4', '#84cc16', '#f97316'],
    performance: (value) => {
      if (value >= 90) return '#10b981'; // Green for excellent
      if (value >= 80) return '#3b82f6'; // Blue for good
      if (value >= 70) return '#f59e0b'; // Yellow for average
      if (value >= 60) return '#f97316'; // Orange for below average
      return '#ef4444'; // Red for poor
    },
    gradient: ['#6366f1', '#8b5cf6', '#d946ef', '#ec4899', '#f43f5e']
  };

  // Loading state
  if (loading) {
    return (
      <div className="chart-container" style={{ height }}>
        <div className="chart-loading">
          <div className="loading-spinner"></div>
          <p>Loading subject data...</p>
        </div>
      </div>
    );
  }

  // Error state
  if (error) {
    return (
      <div className="chart-container" style={{ height }}>
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
      <div className="chart-container" style={{ height }}>
        <div className="chart-empty">
          <div className="empty-icon">📊</div>
          <p className="empty-message">No subject data available</p>
          <p className="empty-subtitle">Upload assessment data to compare subjects</p>
        </div>
      </div>
    );
  }

  // Sort data based on sortBy prop
  const sortedData = [...data].sort((a, b) => {
    switch (sortBy) {
      case 'average':
        return (b.average || 0) - (a.average || 0);
      case 'name':
        return (a.subject || a.name || '').localeCompare(b.subject || b.name || '');
      default:
        return 0;
    }
  });

  // Custom tooltip component
  const CustomTooltip = ({ active, payload, label }) => {
    if (active && payload && payload.length) {
      const data = payload[0];
      return (
        <div className="chart-tooltip">
          <p className="tooltip-label">{`Subject: ${label}`}</p>
          <p className="tooltip-value" style={{ color: data.color }}>
            {`Average: ${data.value}%`}
          </p>
          {data.payload.studentCount && (
            <p className="tooltip-info">
              {`Students: ${data.payload.studentCount}`}
            </p>
          )}
          {data.payload.assessmentCount && (
            <p className="tooltip-info">
              {`Assessments: ${data.payload.assessmentCount}`}
            </p>
          )}
          {data.payload.grade && (
            <p className="tooltip-grade">
              {`Grade: ${data.payload.grade}`}
            </p>
          )}
        </div>
      );
    }
    return null;
  };

  // Format X-axis labels (truncate long subject names)
  const formatXAxisLabel = (tickItem) => {
    if (tickItem.length > 12) {
      return tickItem.substring(0, 12) + '...';
    }
    return tickItem;
  };

  // Format Y-axis labels for percentages
  const formatYAxisLabel = (value) => `${value}%`;

  // Get color for a bar
  const getBarColor = (entry, index) => {
    if (colorScheme === 'performance' && typeof colorSchemes.performance === 'function') {
      return colorSchemes.performance(entry.average || 0);
    }
    
    const colors = colorSchemes[colorScheme] || colorSchemes.default;
    return colors[index % colors.length];
  };

  // Calculate domain for Y-axis
  const values = sortedData.map(item => item.average || 0);
  const maxValue = Math.min(100, Math.max(...values) + 10);

  return (
    <div className="chart-container" style={{ height }}>
      <ResponsiveContainer width="100%" height="100%">
        <BarChart
          data={sortedData}
          margin={{
            top: 20,
            right: 30,
            left: 20,
            bottom: 60,
          }}
        >
          {showGrid && (
            <CartesianGrid 
              strokeDasharray="3 3" 
              stroke="#e2e8f0"
              opacity={0.5}
            />
          )}
          
          <XAxis
            dataKey="subject"
            tickFormatter={formatXAxisLabel}
            stroke="#64748b"
            fontSize={12}
            tickLine={false}
            axisLine={{ stroke: '#e2e8f0' }}
            angle={-45}
            textAnchor="end"
            height={60}
            interval={0}
          />
          
          <YAxis
            domain={[0, maxValue]}
            tickFormatter={formatYAxisLabel}
            stroke="#64748b"
            fontSize={12}
            tickLine={false}
            axisLine={{ stroke: '#e2e8f0' }}
            width={40}
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
          
          <Bar
            dataKey="average"
            name="Average Score"
            radius={[4, 4, 0, 0]}
            stroke="#ffffff"
            strokeWidth={1}
          >
            {sortedData.map((entry, index) => (
              <Cell 
                key={`cell-${index}`} 
                fill={getBarColor(entry, index)}
              />
            ))}
          </Bar>
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
};

// PropTypes for type checking
SubjectComparisonChart.propTypes = {
  /** Array of subject data with subject name and average score */
  data: PropTypes.arrayOf(
    PropTypes.shape({
      subject: PropTypes.string.isRequired,
      average: PropTypes.number.isRequired,
      studentCount: PropTypes.number,
      assessmentCount: PropTypes.number,
      grade: PropTypes.string
    })
  ),
  
  /** Height of the chart in pixels */
  height: PropTypes.number,
  
  /** Whether to show grid lines */
  showGrid: PropTypes.bool,
  
  /** Whether to show legend */
  showLegend: PropTypes.bool,
  
  /** Color scheme: 'default', 'performance', or 'gradient' */
  colorScheme: PropTypes.oneOf(['default', 'performance', 'gradient']),
  
  /** Loading state */
  loading: PropTypes.bool,
  
  /** Error message to display */
  error: PropTypes.string,
  
  /** How to sort the data: 'average', 'name', or 'none' */
  sortBy: PropTypes.oneOf(['average', 'name', 'none'])
};

export default React.memo(SubjectComparisonChart);