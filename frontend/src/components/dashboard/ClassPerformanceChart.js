import React from 'react';
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  Legend
} from 'recharts';
import PropTypes from 'prop-types';
import './ChartComponents.css';

/**
 * ClassPerformanceChart Component - Line chart showing class performance trends over time
 * Uses recharts to visualize time-series data of class average performance
 */
const ClassPerformanceChart = ({ 
  data = [], 
  height = 300, 
  showGrid = true,
  showLegend = true,
  color = '#3b82f6',
  loading = false,
  error = null
}) => {
  // Loading state
  if (loading) {
    return (
      <div className="chart-container" style={{ height }}>
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
          <div className="empty-icon">📈</div>
          <p className="empty-message">No performance data available</p>
          <p className="empty-subtitle">Upload assessment data to see trends</p>
        </div>
      </div>
    );
  }

  // Custom tooltip component
  const CustomTooltip = ({ active, payload, label }) => {
    if (active && payload && payload.length) {
      const data = payload[0];
      return (
        <div className="chart-tooltip">
          <p className="tooltip-label">{`Date: ${label}`}</p>
          <p className="tooltip-value" style={{ color: data.color }}>
            {`Average: ${data.value}%`}
          </p>
          {data.payload.assessmentCount && (
            <p className="tooltip-info">
              {`Assessments: ${data.payload.assessmentCount}`}
            </p>
          )}
        </div>
      );
    }
    return null;
  };

  // Format X-axis labels for dates
  const formatXAxisLabel = (tickItem) => {
    const date = new Date(tickItem);
    return date.toLocaleDateString('en-US', { 
      month: 'short', 
      day: 'numeric' 
    });
  };

  // Format Y-axis labels for percentages
  const formatYAxisLabel = (value) => `${value}%`;

  // Calculate domain for Y-axis (with some padding)
  const values = data.map(item => item.average || 0);
  const minValue = Math.max(0, Math.min(...values) - 5);
  const maxValue = Math.min(100, Math.max(...values) + 5);

  return (
    <div className="chart-container" style={{ height }}>
      <ResponsiveContainer width="100%" height="100%">
        <LineChart
          data={data}
          margin={{
            top: 20,
            right: 30,
            left: 20,
            bottom: 20,
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
            dataKey="date"
            tickFormatter={formatXAxisLabel}
            stroke="#64748b"
            fontSize={12}
            tickLine={false}
            axisLine={{ stroke: '#e2e8f0' }}
          />
          
          <YAxis
            domain={[minValue, maxValue]}
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
          
          <Line
            type="monotone"
            dataKey="average"
            stroke={color}
            strokeWidth={3}
            dot={{ 
              fill: color, 
              strokeWidth: 2, 
              r: 4,
              stroke: '#ffffff'
            }}
            activeDot={{ 
              r: 6, 
              stroke: color,
              strokeWidth: 2,
              fill: '#ffffff'
            }}
            name="Class Average"
          />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
};

// PropTypes for type checking
ClassPerformanceChart.propTypes = {
  /** Array of time-series data points with date and average properties */
  data: PropTypes.arrayOf(
    PropTypes.shape({
      date: PropTypes.string.isRequired,
      average: PropTypes.number.isRequired,
      assessmentCount: PropTypes.number
    })
  ),
  
  /** Height of the chart in pixels */
  height: PropTypes.number,
  
  /** Whether to show grid lines */
  showGrid: PropTypes.bool,
  
  /** Whether to show legend */
  showLegend: PropTypes.bool,
  
  /** Color of the line */
  color: PropTypes.string,
  
  /** Loading state */
  loading: PropTypes.bool,
  
  /** Error message to display */
  error: PropTypes.string
};

export default React.memo(ClassPerformanceChart);