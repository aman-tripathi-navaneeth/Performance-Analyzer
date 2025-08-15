import React from 'react';
import './AcademicInsights.css';

/**
 * AcademicInsights Component - Displays comprehensive academic analysis for a student
 * Shows performance level, strengths, weaknesses, and recommendations
 */
const AcademicInsights = ({ insights, className = '' }) => {
  if (!insights) {
    return (
      <div className={`academic-insights ${className}`}>
        <div className="insights-header">
          <h3>📊 Academic Insights</h3>
        </div>
        <div className="no-insights">
          <p>No academic insights available. Upload performance data to get detailed analysis.</p>
        </div>
      </div>
    );
  }

  const getPerformanceLevelColor = (level) => {
    if (level?.includes('Excellent')) return 'excellent';
    if (level?.includes('Good')) return 'good';
    if (level?.includes('Average')) return 'average';
    if (level?.includes('Below Average')) return 'below-average';
    if (level?.includes('Struggling')) return 'struggling';
    return 'default';
  };

  const getConsistencyColor = (score) => {
    if (score >= 80) return 'excellent';
    if (score >= 60) return 'good';
    if (score >= 40) return 'average';
    return 'poor';
  };

  return (
    <div className={`academic-insights ${className}`}>
      {/* Header */}
      <div className="insights-header">
        <h3>🎓 Academic Insights</h3>
        <div className="performance-badge">
          <span className={`performance-level ${getPerformanceLevelColor(insights.performance_level)}`}>
            {insights.performance_level}
          </span>
        </div>
      </div>

      {/* Academic Summary */}
      <div className="academic-summary">
        <div className="summary-card">
          <div className="summary-icon">📋</div>
          <div className="summary-content">
            <h4>Academic Status</h4>
            <p>{insights.academic_status}</p>
          </div>
        </div>
      </div>

      {/* Performance Metrics */}
      <div className="performance-metrics">
        <div className="metric-card">
          <div className="metric-icon">🎯</div>
          <div className="metric-content">
            <span className="metric-label">Overall Grade</span>
            <span className={`metric-value grade-${insights.overall_grade?.toLowerCase()}`}>
              {insights.overall_grade}
            </span>
          </div>
        </div>

        <div className="metric-card">
          <div className="metric-icon">📊</div>
          <div className="metric-content">
            <span className="metric-label">Consistency</span>
            <span className={`metric-value consistency-${getConsistencyColor(insights.consistency_score)}`}>
              {insights.consistency} ({insights.consistency_score}%)
            </span>
          </div>
        </div>
      </div>

      {/* Strengths */}
      {insights.strengths && insights.strengths.length > 0 && (
        <div className="insights-section strengths-section">
          <h4 className="section-title">
            <span className="section-icon">💪</span>
            Strengths
          </h4>
          <div className="insights-list">
            {insights.strengths.map((strength, index) => (
              <div key={index} className="insight-item strength-item">
                <span className="item-icon">✅</span>
                <span className="item-text">{strength}</span>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Areas for Improvement */}
      {insights.areas_for_improvement && insights.areas_for_improvement.length > 0 && (
        <div className="insights-section improvement-section">
          <h4 className="section-title">
            <span className="section-icon">⚠️</span>
            Areas for Improvement
          </h4>
          <div className="insights-list">
            {insights.areas_for_improvement.map((area, index) => (
              <div key={index} className="insight-item improvement-item">
                <span className="item-icon">🔸</span>
                <span className="item-text">{area}</span>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Recommendations */}
      {insights.recommendations && insights.recommendations.length > 0 && (
        <div className="insights-section recommendations-section">
          <h4 className="section-title">
            <span className="section-icon">💡</span>
            Recommendations
          </h4>
          <div className="insights-list">
            {insights.recommendations.map((recommendation, index) => (
              <div key={index} className="insight-item recommendation-item">
                <span className="item-icon">💡</span>
                <span className="item-text">{recommendation}</span>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Subject Analysis */}
      {(insights.strongest_subject || insights.weakest_subject) && (
        <div className="insights-section subject-analysis-section">
          <h4 className="section-title">
            <span className="section-icon">📚</span>
            Subject Analysis
          </h4>
          <div className="subject-analysis">
            {insights.strongest_subject && (
              <div className="subject-highlight strongest">
                <span className="subject-label">Strongest Subject:</span>
                <span className="subject-name">{insights.strongest_subject}</span>
              </div>
            )}
            {insights.weakest_subject && (
              <div className="subject-highlight weakest">
                <span className="subject-label">Needs Attention:</span>
                <span className="subject-name">{insights.weakest_subject}</span>
              </div>
            )}
          </div>
        </div>
      )}

      {/* Trends */}
      {(insights.improving_subjects?.length > 0 || insights.declining_subjects?.length > 0) && (
        <div className="insights-section trends-section">
          <h4 className="section-title">
            <span className="section-icon">📈</span>
            Performance Trends
          </h4>
          <div className="trends-content">
            {insights.improving_subjects?.length > 0 && (
              <div className="trend-item improving">
                <span className="trend-icon">📈</span>
                <span className="trend-label">Improving:</span>
                <span className="trend-subjects">{insights.improving_subjects.join(', ')}</span>
              </div>
            )}
            {insights.declining_subjects?.length > 0 && (
              <div className="trend-item declining">
                <span className="trend-icon">📉</span>
                <span className="trend-label">Declining:</span>
                <span className="trend-subjects">{insights.declining_subjects.join(', ')}</span>
              </div>
            )}
          </div>
        </div>
      )}

      {/* Academic Summary Text */}
      {insights.academic_summary && (
        <div className="insights-section summary-text-section">
          <h4 className="section-title">
            <span className="section-icon">📖</span>
            Summary
          </h4>
          <div className="summary-text">
            <p>{insights.academic_summary}</p>
          </div>
        </div>
      )}
    </div>
  );
};

export default AcademicInsights;