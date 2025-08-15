import { useNavigate } from "react-router-dom";
import { useEffect } from "react";
import { getClassOverview } from "../api/apiService";
import useSimpleFetch from "../hooks/useSimpleFetch";
import cacheManager from "../utils/cacheManager";
import Header from "../components/common/Header";
import "./DashboardPage.css";

/**
 * DashboardPage Component - Simple dashboard showing only uploaded Excel sheet results
 * Displays uploaded student data in a clean, focused interface
 */
const DashboardPage = () => {
  const navigate = useNavigate();

  // Use simplified hook for data fetching
  const { data, loading, error, refresh } = useSimpleFetch(
    getClassOverview,
    []
  );

  // Listen for cache invalidation events
  useEffect(() => {
    const cleanup = cacheManager.addListener((reason) => {
      console.log(`Dashboard refreshing due to: ${reason}`);
      refresh();
    });

    return cleanup;
  }, [refresh]);

  // Navigate to upload page
  const navigateToUpload = () => {
    navigate("/upload");
  };

  // Loading state
  if (loading) {
    return (
      <div className="dashboard-page">
        <Header />
        <div className="dashboard-container">
          <div className="dashboard-header">
            <h1 className="dashboard-title">📊 Student Results Dashboard</h1>
            <div className="loading-message">Loading uploaded results...</div>
          </div>
        </div>
      </div>
    );
  }

  // No data state - show upload prompt
  if (!data || !data.statistics || data.statistics.total_students === 0) {
    return (
      <div className="dashboard-page">
        <Header />
        <div className="dashboard-container">
          <div className="no-data-container">
            <div className="no-data-icon">📤</div>
            <h2 className="no-data-title">No Student Data Found</h2>
            <p className="no-data-message">
              Upload an Excel sheet with student results to view the dashboard
            </p>
            <button className="btn btn-primary btn-large" onClick={navigateToUpload}>
              <span>📤</span>
              Upload Excel Sheet
            </button>
          </div>
        </div>
      </div>
    );
  }

  // Error state
  if (error) {
    return (
      <div className="dashboard-page">
        <Header />
        <div className="dashboard-container">
          <div className="error-container">
            <h2 className="error-title">Error Loading Results</h2>
            <p className="error-message">{error}</p>
            <div className="error-actions">
              <button className="btn btn-secondary" onClick={() => refresh()}>
                Try Again
              </button>
              <button className="btn btn-primary" onClick={navigateToUpload}>
                Upload New Data
              </button>
            </div>
          </div>
        </div>
      </div>
    );
  }

  // Main dashboard render - Simple view of uploaded Excel data
  return (
    <div className="dashboard-page">
      <Header />

      <div className="dashboard-container">
        {/* Simple Header */}
        <div className="dashboard-header">
          <div className="header-content">
            <h1 className="dashboard-title">📊 Student Results Dashboard</h1>
            <p className="dashboard-subtitle">
              Results from uploaded Excel sheet
            </p>
          </div>

          <div className="header-actions">
            <button className="btn btn-secondary" onClick={() => refresh()}>
              <span>🔄</span>
              Refresh
            </button>
            <button className="btn btn-primary" onClick={navigateToUpload}>
              <span>📤</span>
              Upload New Data
            </button>
          </div>
        </div>

        {/* Key Statistics - Simple Overview */}
        <div className="stats-overview">
          <div className="stat-card">
            <div className="stat-icon">👥</div>
            <div className="stat-content">
              <div className="stat-value">{data?.statistics?.total_students || 0}</div>
              <div className="stat-label">Total Students</div>
            </div>
          </div>

          <div className="stat-card">
            <div className="stat-icon">📚</div>
            <div className="stat-content">
              <div className="stat-value">{data?.statistics?.total_subjects || 0}</div>
              <div className="stat-label">Subjects</div>
            </div>
          </div>

          <div className="stat-card">
            <div className="stat-icon">📊</div>
            <div className="stat-content">
              <div className="stat-value">{data?.statistics?.overall_class_average || 0}%</div>
              <div className="stat-label">Class Average</div>
            </div>
          </div>

          <div className="stat-card">
            <div className="stat-icon">🏆</div>
            <div className="stat-content">
              <div className="stat-value">{data?.statistics?.overall_grade || "N/A"}</div>
              <div className="stat-label">Overall Grade</div>
            </div>
          </div>
        </div>

        {/* Student Results Table */}
        <div className="results-section">
          <div className="section-header">
            <h2 className="section-title">📋 Student Results</h2>
            <p className="section-subtitle">
              Individual student performance from uploaded data
            </p>
          </div>

          <div className="results-table-container">
            <table className="results-table">
              <thead>
                <tr>
                  <th>Roll Number</th>
                  <th>Student Name</th>
                  <th>Subject</th>
                  <th>Score</th>
                  <th>Grade</th>
                  <th>Status</th>
                </tr>
              </thead>
              <tbody>
                {data?.recent_assessments?.map((assessment, index) => (
                  <tr key={index} className="result-row">
                    <td className="roll-number">{assessment.student_roll || "N/A"}</td>
                    <td className="student-name">{assessment.student_name || "N/A"}</td>
                    <td className="subject-name">{assessment.subject_name}</td>
                    <td className="score">
                      <span className="score-value">{assessment.average_percentage}%</span>
                    </td>
                    <td className="grade">
                      <span className={`grade-badge grade-${assessment.grade?.toLowerCase()}`}>
                        {assessment.grade}
                      </span>
                    </td>
                    <td className="status">
                      <span className={`status-badge ${getStatusClass(assessment.average_percentage)}`}>
                        {getStatusText(assessment.average_percentage)}
                      </span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>

            {(!data?.recent_assessments || data.recent_assessments.length === 0) && (
              <div className="no-results">
                <div className="no-results-icon">📄</div>
                <p className="no-results-text">No student results found</p>
                <button className="btn btn-primary" onClick={navigateToUpload}>
                  Upload Excel Sheet
                </button>
              </div>
            )}
          </div>
        </div>

        {/* Subject Summary */}
        {data?.subjects_performance && data.subjects_performance.length > 0 && (
          <div className="subjects-summary">
            <div className="section-header">
              <h2 className="section-title">📚 Subject Summary</h2>
              <p className="section-subtitle">Performance overview by subject</p>
            </div>

            <div className="subjects-grid">
              {data.subjects_performance.map((subject, index) => (
                <div key={index} className="subject-summary-card">
                  <div className="subject-header">
                    <h3 className="subject-name">{subject.subject_name}</h3>
                    <span className={`grade-badge grade-${subject.grade?.toLowerCase()}`}>
                      {subject.grade}
                    </span>
                  </div>

                  <div className="subject-stats">
                    <div className="stat-row">
                      <span className="stat-label">Average Score:</span>
                      <span className="stat-value">{subject.average_percentage}%</span>
                    </div>
                    <div className="stat-row">
                      <span className="stat-label">Students:</span>
                      <span className="stat-value">{subject.unique_students}</span>
                    </div>
                    <div className="stat-row">
                      <span className="stat-label">Assessments:</span>
                      <span className="stat-value">{subject.assessment_count}</span>
                    </div>
                  </div>

                  <div className="progress-bar">
                    <div
                      className="progress-fill"
                      style={{ 
                        width: `${subject.average_percentage}%`,
                        backgroundColor: getGradeColor(subject.grade)
                      }}
                    ></div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Quick Actions */}
        <div className="quick-actions">
          <button className="action-btn" onClick={() => navigate("/students")}>
            <span className="action-icon">👥</span>
            <span className="action-text">View All Students</span>
          </button>
          
          <button className="action-btn" onClick={navigateToUpload}>
            <span className="action-icon">📤</span>
            <span className="action-text">Upload New Results</span>
          </button>
        </div>
      </div>
    </div>
  );
};

// Helper functions
const getGradeColor = (grade) => {
  const gradeColors = {
    "A+": "#10b981",
    A: "#10b981", 
    "B+": "#3b82f6",
    B: "#3b82f6",
    C: "#f59e0b",
    D: "#f59e0b",
    F: "#ef4444",
  };
  return gradeColors[grade] || "#6b7280";
};

const getStatusClass = (score) => {
  if (score >= 90) return "excellent";
  if (score >= 80) return "good";
  if (score >= 60) return "average";
  if (score >= 40) return "below-average";
  return "poor";
};

const getStatusText = (score) => {
  if (score >= 90) return "Excellent";
  if (score >= 80) return "Good";
  if (score >= 60) return "Average";
  if (score >= 40) return "Below Average";
  return "Needs Improvement";
};

export default DashboardPage;