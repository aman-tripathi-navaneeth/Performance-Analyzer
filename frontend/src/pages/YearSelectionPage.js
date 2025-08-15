import React from "react";
import { useNavigate } from "react-router-dom";
import { getClassOverview } from "../api/apiService";
import useFetchSimple from "../hooks/useFetchSimple";
import Header from "../components/common/Header";
import StatCard from "../components/common/StatCard";

import "./YearSelectionPage.css";

/**
 * YearSelectionPage Component - Shows year-wise student distribution
 * Allows navigation to specific year performance analysis
 */
const YearSelectionPage = () => {
  const navigate = useNavigate();

  // Fetch overview data to get year distribution
  const { data, loading, error, refresh } = useFetchSimple(
    () => getClassOverview(),
    []
  );



  const overviewData = data?.data;

  // Use API data or empty objects if not available
  const yearDistribution = overviewData?.year_distribution || {};
  const yearSectionDistribution = overviewData?.year_section_distribution || {};



  // Navigate to year performance page
  const handleYearSelect = (yearNumber, yearLabel) => {
    navigate(`/students/year/${yearNumber}`);
  };

  // Get year icon based on year number
  const getYearIcon = (yearNumber) => {
    switch (yearNumber) {
      case 1:
        return "🌱";
      case 2:
        return "🌿";
      case 3:
        return "🌳";
      case 4:
        return "🎓";
      default:
        return "📚";
    }
  };

  // Get color based on student count
  const getCountColor = (count) => {
    if (count >= 50) return "high";
    if (count >= 20) return "medium";
    if (count > 0) return "low";
    return "none";
  };

  // Calculate total students
  const totalStudents = Object.values(yearDistribution).reduce(
    (sum, count) => sum + count,
    0
  );

  if (loading) {
    return (
      <div className="year-selection-page">
        <Header />
        <div className="container">
          <div className="loading">Loading year data...</div>
        </div>
      </div>
    );
  }

  // Don't return early on error - show fallback data instead

  return (
    <div className="year-selection-page">
      <Header />

      <div className="container">
        {/* Page Header */}
        <div className="page-header">
          <div className="header-content">
            <h1>📚 Students by Academic Year</h1>
            <p>
              Select an academic year to view section-wise performance analysis
            </p>

          </div>
        </div>

        {/* Overall Statistics */}
        <div className="stats-grid">
          <StatCard
            title="Total Students"
            value={totalStudents}
            subtitle="Across all years"
            icon="👥"
            color="primary"
          />
          <StatCard
            title="Active Years"
            value={
              Object.values(yearDistribution).filter((count) => count > 0)
                .length
            }
            subtitle="Years with students"
            icon="📅"
            color="info"
          />
          <StatCard
            title="Total Sections"
            value={Object.values(yearSectionDistribution).reduce(
              (sum, sections) => sum + Object.keys(sections).length,
              0
            )}
            subtitle="Active sections"
            icon="🏫"
            color="success"
          />
          <StatCard
            title="Average per Year"
            value={
              Math.round(
                totalStudents /
                  Object.values(yearDistribution).filter((count) => count > 0)
                    .length
              ) || 0
            }
            subtitle="Students per year"
            icon="📊"
            color="warning"
          />
        </div>

        {/* Year Selection Cards */}
        <div className="year-cards-grid">
          {[1, 2, 3, 4].map((yearNumber) => {
            const yearLabel = `${yearNumber}${
              yearNumber === 1
                ? "st"
                : yearNumber === 2
                ? "nd"
                : yearNumber === 3
                ? "rd"
                : "th"
            } Year`;
            const studentCount = yearDistribution[yearLabel] || 0;
            const sections = yearSectionDistribution[yearLabel] || {};
            const sectionCount = Object.keys(sections).length;

            const handleCardClick = (e) => {
              e.preventDefault();
              e.stopPropagation();

              if (studentCount > 0) {
                handleYearSelect(yearNumber, yearLabel);
              }
            };

            return (
              <div
                key={yearNumber}
                className={`year-card ${
                  studentCount === 0 ? "disabled" : "clickable"
                }`}
                onClick={handleCardClick}

                style={{
                  cursor: studentCount > 0 ? "pointer" : "not-allowed",
                  pointerEvents: "auto",
                  userSelect: "none",
                }}
              >
                <div className="year-icon">{getYearIcon(yearNumber)}</div>

                <div className="year-info">
                  <h3 className="year-title">{yearLabel}</h3>
                  <div className="year-stats">
                    <div
                      className={`student-count ${getCountColor(studentCount)}`}
                    >
                      <span className="count-number">{studentCount}</span>
                      <span className="count-label">students</span>
                    </div>
                    <div className="section-count">
                      <span className="section-number">{sectionCount}</span>
                      <span className="section-label">sections</span>
                    </div>
                  </div>

                  {/* Section Preview */}
                  {sectionCount > 0 && (
                    <div className="sections-preview">
                      {Object.entries(sections)
                        .slice(0, 3)
                        .map(([section, count]) => (
                          <span key={section} className="section-tag">
                            {section} ({count})
                          </span>
                        ))}
                      {sectionCount > 3 && (
                        <span className="section-tag more">
                          +{sectionCount - 3} more
                        </span>
                      )}
                    </div>
                  )}
                </div>

                <div className="year-arrow">{studentCount > 0 ? "→" : "—"}</div>
              </div>
            );
          })}
        </div>





        {/* Quick Actions */}
        <div className="quick-actions">
          <button
            className="btn btn-secondary"
            onClick={() => navigate("/teacher-dashboard")}
          >
            ← Back to Dashboard
          </button>
          <button
            className="btn btn-secondary"
            onClick={() => navigate("/upload")}
          >
            📤 Upload New Data
          </button>
        </div>

        {/* No Data Message */}
        {totalStudents === 0 && (
          <div className="no-data-message">
            <div className="no-data-icon">📚</div>
            <h3>No Student Data Available</h3>
            <p>Upload student performance data to see year-wise analysis</p>
            <button
              className="btn btn-primary"
              onClick={() => navigate("/upload")}
            >
              Upload Data
            </button>
          </div>
        )}
      </div>
    </div>
  );
};

export default YearSelectionPage;
