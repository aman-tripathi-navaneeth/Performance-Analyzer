import { useNavigate } from "react-router-dom";
import { getClassOverview } from "../api/apiService";
import useSimpleFetch from "../hooks/useSimpleFetch";
import Header from "../components/common/Header";
import StatCard from "../components/common/StatCard";
import ClassPerformanceChart from "../components/dashboard/ClassPerformanceChart";
import SubjectComparisonChart from "../components/dashboard/SubjectComparisonChart";
import "./DashboardPage.css";

/**
 * DashboardPage Component - Main dashboard showing class overview and analytics
 * Displays key metrics, performance charts, and quick access to important data
 */
const DashboardPage = () => {
  const navigate = useNavigate();

  // Use simplified hook for data fetching
  const { data, loading, error, refresh } = useSimpleFetch(
    getClassOverview,
    []
  );

  // Handle refresh
  const handleRefresh = () => {
    refresh();
  };

  // Navigate to students with filter
  const navigateToStudents = (filter = "") => {
    const url = filter ? `/students?filter=${filter}` : "/students";
    navigate(url);
  };

  // Navigate to upload page
  const navigateToUpload = () => {
    navigate("/upload");
  };

  // Transform data for ClassPerformanceChart
  const getPerformanceTimeSeriesData = () => {
    if (!data?.performance_trends) return [];

    return data.performance_trends.map((item) => ({
      date: item.date,
      average: item.average_percentage,
      assessmentCount: item.assessment_count,
    }));
  };

  // Transform data for SubjectComparisonChart
  const getSubjectComparisonData = () => {
    if (!data?.subjects_performance) return [];

    return data.subjects_performance.map((subject) => ({
      subject: subject.subject_name,
      average: subject.average_percentage,
      studentCount: subject.unique_students,
      assessmentCount: subject.assessment_count,
      grade: subject.grade,
    }));
  };

  // Loading state
  if (loading) {
    return (
      <div className="dashboard-page">
        <Header />
        <div className="dashboard-container">
          <div className="dashboard-header">
            <div className="loading-skeleton title-skeleton"></div>
            <div className="loading-skeleton subtitle-skeleton"></div>
          </div>

          <div className="stats-grid">
            {[...Array(4)].map((_, index) => (
              <div key={index} className="loading-skeleton stat-skeleton"></div>
            ))}
          </div>

          <div className="dashboard-content">
            <div className="loading-skeleton chart-skeleton"></div>
            <div className="loading-skeleton chart-skeleton"></div>
          </div>
        </div>
      </div>
    );
  }

  // Error state
  if (error && !data) {
    return (
      <div className="dashboard-page">
        <Header />
        <div className="dashboard-container">
          <div className="error-container">
            <h2 className="error-title">Unable to Load Dashboard</h2>
            <p className="error-message">{error}</p>
            <div className="error-actions">
              <button className="btn btn-primary" onClick={handleRefresh}>
                Try Again
              </button>
              <button className="btn btn-primary" onClick={navigateToUpload}>
                Upload Data
              </button>
            </div>
          </div>
        </div>
      </div>
    );
  }

  // Main dashboard render
  return (
    <div className="dashboard-page">
      {/* Header Component */}
      <Header />

      <div className="dashboard-container">
        {/* Dashboard Header */}
        <div className="dashboard-header">
          <div className="header-content">
            <h1 className="dashboard-title">Class Performance Dashboard</h1>
            <p className="dashboard-subtitle">
              Overview of student performance across all subjects and
              assessments
            </p>
          </div>

          <div className="header-actions">
            <button
              className={`btn btn-secondary ${loading ? "loading" : ""}`}
              onClick={handleRefresh}
              disabled={loading}
            >
              {loading ? (
                <>
                  <span className="loading-spinner-small"></span>
                  Refreshing...
                </>
              ) : (
                <>
                  <span>🔄</span>
                  Refresh
                </>
              )}
            </button>

            <button className="btn btn-primary" onClick={navigateToUpload}>
              <span>📤</span>
              Upload Data
            </button>
          </div>
        </div>

        {/* Key Statistics Grid */}
        <div className="stats-grid">
          <StatCard
            title="Total Students"
            value={data?.statistics?.total_students || 0}
            subtitle="Enrolled students"
            icon="👥"
            color="primary"
            onClick={() => navigateToStudents()}
          />

          <StatCard
            title="Total Subjects"
            value={data?.statistics?.total_subjects || 0}
            subtitle="Active subjects"
            icon="📚"
            color="info"
          />

          <StatCard
            title="Class Average"
            value={`${data?.statistics?.overall_class_average || 0}%`}
            subtitle={`Grade: ${data?.statistics?.overall_grade || "N/A"}`}
            icon="📊"
            color={getGradeColor(data?.statistics?.overall_grade)}
            trend={getPerformanceTrend(data?.statistics?.overall_class_average)}
            trendValue="+2.3%"
          />

          <StatCard
            title="Total Assessments"
            value={data?.statistics?.total_assessments || 0}
            subtitle="Completed assessments"
            icon="📝"
            color="success"
          />
        </div>

        {/* Performance Search Section */}
        <div className="performance-search-section">
          <div className="search-header">
            <h2 className="search-title">🔍 Performance Analysis</h2>
            <p className="search-subtitle">
              Search for overall class or individual student performance
            </p>
          </div>

          <div className="search-options">
            <div className="search-option-card">
              <div className="option-icon">🏫</div>
              <div className="option-content">
                <h3 className="option-title">Overall Class Performance</h3>
                <p className="option-description">
                  View performance across all years and sections
                </p>
                <div className="option-filters">
                  <select
                    className="filter-select"
                    onChange={(e) =>
                      navigateToStudents(`year=${e.target.value}`)
                    }
                  >
                    <option value="">All Years</option>
                    <option value="1">1st Year</option>
                    <option value="2">2nd Year</option>
                    <option value="3">3rd Year</option>
                    <option value="4">4th Year</option>
                  </select>
                  <select
                    className="filter-select"
                    onChange={(e) =>
                      navigateToStudents(`section=${e.target.value}`)
                    }
                  >
                    <option value="">All Sections</option>
                    <option value="CSEA">CSE A</option>
                    <option value="CSEB">CSE B</option>
                    <option value="CSM">CSM</option>
                    <option value="ECE">ECE</option>
                    <option value="COS">COS</option>
                  </select>
                </div>
                <button
                  className="btn btn-primary option-btn"
                  onClick={() => navigateToStudents()}
                >
                  View Class Performance
                </button>
              </div>
            </div>

            <div className="search-option-card">
              <div className="option-icon">👤</div>
              <div className="option-content">
                <h3 className="option-title">Individual Student Performance</h3>
                <p className="option-description">
                  Search for specific student performance data
                </p>
                <div className="student-search">
                  <input
                    type="text"
                    className="search-input"
                    placeholder="Enter student name or roll number..."
                    onKeyPress={(e) => {
                      if (e.key === "Enter" && e.target.value.trim()) {
                        navigateToStudents(
                          `search=${encodeURIComponent(e.target.value.trim())}`
                        );
                      }
                    }}
                  />
                  <button
                    className="btn btn-secondary search-btn"
                    onClick={(e) => {
                      const input = e.target.previousElementSibling;
                      if (input.value.trim()) {
                        navigateToStudents(
                          `search=${encodeURIComponent(input.value.trim())}`
                        );
                      }
                    }}
                  >
                    Search Student
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Main Charts Section - Critical Information at Top */}
        <div className="charts-section">
          {/* Performance Trend Chart */}
          <div className="chart-card chart-primary">
            <div className="chart-header">
              <h2 className="chart-title">Performance Trends</h2>
              <p className="chart-subtitle">Class performance over time</p>
            </div>
            <ClassPerformanceChart
              data={getPerformanceTimeSeriesData()}
              height={280}
              loading={loading}
              error={error}
              color="#3b82f6"
              showGrid={true}
              showLegend={false}
            />
          </div>

          {/* Year Distribution Chart */}
          <div className="chart-card">
            <div className="chart-header">
              <h2 className="chart-title">Year Distribution</h2>
              <p className="chart-subtitle">Students by academic year</p>
            </div>
            <div className="year-distribution-summary">
              {Object.entries(
                data?.year_distribution || {
                  "1st Year": 0,
                  "2nd Year": 0,
                  "3rd Year": 0,
                  "4th Year": 0,
                }
              ).map(([year, count]) => (
                <div key={year} className="year-summary-item">
                  <span
                    className={`year-badge year-${year
                      .replace(/\s+/g, "")
                      .toLowerCase()}`}
                  >
                    {year}
                  </span>
                  <div className="year-info">
                    <span className="year-count">{count}</span>
                    <span className="year-percentage">
                      {data?.statistics?.total_students
                        ? Math.round(
                            (count / data.statistics.total_students) * 100
                          )
                        : 0}
                      %
                    </span>
                  </div>
                  <button
                    className="year-view-btn"
                    onClick={() =>
                      navigateToStudents(`year=${year.split(" ")[0]}`)
                    }
                    title={`View ${year} students`}
                  >
                    View
                  </button>
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* Subject Performance Chart */}
        <div className="chart-card chart-wide">
          <div className="chart-header">
            <h2 className="chart-title">Subject Performance Comparison</h2>
            <p className="chart-subtitle">
              Average performance across all subjects
            </p>
          </div>
          <SubjectComparisonChart
            data={getSubjectComparisonData()}
            height={320}
            loading={loading}
            error={error}
            colorScheme="performance"
            showGrid={true}
            showLegend={false}
            sortBy="average"
          />
        </div>

        {/* Dashboard Content Grid */}
        <div className="dashboard-content">
          {/* Top Performers Section - High Priority */}
          <div className="dashboard-section priority-section">
            <div className="section-header">
              <h2 className="section-title">🏆 Top Performers</h2>
              <p className="section-subtitle">Highest achieving students</p>
            </div>

            <div className="performers-list">
              {data?.top_performers?.slice(0, 5).map((student) => (
                <div
                  key={student.student_roll_number}
                  className="performer-item"
                  onClick={() =>
                    navigate(`/student/${student.student_roll_number}`)
                  }
                >
                  <div className="performer-rank">#{student.rank}</div>
                  <div className="performer-info">
                    <h4 className="performer-name">{student.full_name}</h4>
                    <p className="performer-id">
                      {student.student_roll_number}
                    </p>
                  </div>
                  <div className="performer-stats">
                    <span className="performer-average">
                      {student.average_percentage}%
                    </span>
                    <span
                      className={`grade-badge grade-${student.grade?.toLowerCase()}`}
                    >
                      {student.grade}
                    </span>
                  </div>
                </div>
              ))}
            </div>

            <div className="section-footer">
              <button
                className="btn btn-outline"
                onClick={() => navigateToStudents()}
              >
                View All Students
              </button>
            </div>
          </div>

          {/* Recent Assessments Section */}
          <div className="dashboard-section">
            <div className="section-header">
              <h2 className="section-title">📝 Recent Assessments</h2>
              <p className="section-subtitle">Latest assessment results</p>
            </div>

            <div className="recent-assessments">
              {data?.recent_assessments
                ?.slice(0, 5)
                .map((assessment, index) => (
                  <div key={index} className="assessment-item">
                    <div className="assessment-info">
                      <h4 className="assessment-name">
                        {assessment.assessment_name}
                      </h4>
                      <p className="assessment-details">
                        {assessment.subject_name} • {assessment.submissions}{" "}
                        submissions
                      </p>
                    </div>

                    <div className="assessment-stats">
                      <div className="assessment-average">
                        <span className="average-value">
                          {assessment.average_percentage}%
                        </span>
                        <span
                          className={`grade-badge grade-${assessment.grade?.toLowerCase()}`}
                        >
                          {assessment.grade}
                        </span>
                      </div>
                    </div>
                  </div>
                ))}
            </div>
          </div>

          {/* Subject Performance Details */}
          <div className="dashboard-section">
            <div className="section-header">
              <h2 className="section-title">📚 Subject Performance</h2>
              <p className="section-subtitle">
                Detailed performance by subject
              </p>
            </div>

            <div className="subjects-grid">
              {data?.subjects_performance?.slice(0, 6).map((subject, index) => (
                <div key={index} className="subject-card">
                  <div className="subject-header">
                    <h3 className="subject-name">{subject.subject_name}</h3>
                    <span
                      className={`grade-badge grade-${subject.grade?.toLowerCase()}`}
                    >
                      {subject.grade}
                    </span>
                  </div>

                  <div className="subject-stats">
                    <div className="stat-item">
                      <span className="stat-label">Average</span>
                      <span className="stat-value">
                        {subject.average_percentage}%
                      </span>
                    </div>
                    <div className="stat-item">
                      <span className="stat-label">Students</span>
                      <span className="stat-value">
                        {subject.unique_students}
                      </span>
                    </div>
                  </div>

                  <div className="progress-bar">
                    <div
                      className="progress-fill"
                      style={{ width: `${subject.average_percentage}%` }}
                    ></div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* Quick Actions */}
        <div className="quick-actions">
          <h3 className="quick-actions-title">Quick Actions</h3>
          <div className="actions-grid">
            <button
              className="action-card"
              onClick={() => navigateToStudents("struggling")}
            >
              <span className="action-icon">📊</span>
              <span className="action-label">View Struggling Students</span>
            </button>

            <button
              className="action-card"
              onClick={() => navigateToStudents("top")}
            >
              <span className="action-icon">🏆</span>
              <span className="action-label">View Top Performers</span>
            </button>

            <button className="action-card" onClick={navigateToUpload}>
              <span className="action-icon">📤</span>
              <span className="action-label">Upload New Data</span>
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

// Helper functions
const getGradeColor = (grade) => {
  const gradeColors = {
    "A+": "success",
    A: "success",
    "B+": "info",
    B: "info",
    C: "warning",
    D: "warning",
    F: "error",
  };
  return gradeColors[grade] || "default";
};

const getPerformanceTrend = (average) => {
  if (average >= 80) return "up";
  if (average >= 60) return "neutral";
  return "down";
};

export default DashboardPage;
