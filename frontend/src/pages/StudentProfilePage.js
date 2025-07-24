import React, { useState, useCallback } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { getStudentPerformance, getStudentInfo } from "../api/apiService";
import useSimpleFetch from "../hooks/useSimpleFetch";
import Header from "../components/common/Header";
import StatCard from "../components/common/StatCard";
import ClassPerformanceChart from "../components/dashboard/ClassPerformanceChart";
import SubjectComparisonChart from "../components/dashboard/SubjectComparisonChart";
import PerformanceRadarChart from "../components/student/PerformanceRadarChart";
import DetailedScoreTable from "../components/student/DetailedScoreTable";
import "./StudentProfilePage.css";

/**
 * StudentProfilePage Component - Detailed view of individual student performance
 * Displays student information, performance metrics, and subject-wise analysis
 */
const StudentProfilePage = () => {
  const { studentId } = useParams();
  const navigate = useNavigate();
  const [activeTab, setActiveTab] = useState("overview");

  // Create combined fetch function for both student info and performance data
  const fetchStudentData = useCallback(async () => {
    if (!studentId) {
      throw new Error("Student ID is required");
    }

    // Fetch both student info and performance data in parallel
    const [studentResponse, performanceResponse] = await Promise.all([
      getStudentInfo(studentId),
      getStudentPerformance(studentId),
    ]);

    // Check responses and throw errors if needed
    if (!studentResponse.success) {
      throw new Error(
        studentResponse.error || "Failed to fetch student information"
      );
    }

    if (!performanceResponse.success) {
      throw new Error(
        performanceResponse.error || "Failed to fetch performance data"
      );
    }

    // Return combined data
    return {
      studentData: studentResponse.data,
      performanceData: performanceResponse.data,
    };
  }, [studentId]);

  // Use custom hook for data fetching
  const {
    data: combinedData,
    loading,
    error,
    refresh,
  } = useSimpleFetch(fetchStudentData, [studentId]);

  // Extract data from combined response
  const studentData = combinedData?.studentData;
  const performanceData = combinedData?.performanceData;

  // Transform data for performance trend chart
  const getStudentPerformanceTrends = () => {
    if (!performanceData?.performance_trends) return [];

    return performanceData.performance_trends.map((item) => ({
      date: item.date,
      average: item.average_percentage,
      assessmentCount: item.assessment_count,
    }));
  };

  // Transform data for subject comparison chart
  const getStudentSubjectData = () => {
    if (!performanceData?.subject_performance) return [];

    return performanceData.subject_performance.map((subject) => ({
      subject: subject.subject_name,
      average: subject.average_percentage,
      assessmentCount: subject.assessment_count,
      grade: subject.grade,
    }));
  };

  // Transform data for radar chart
  const getRadarChartData = () => {
    if (!performanceData?.subject_performance) return [];

    return performanceData.subject_performance.map((subject) => ({
      subject: subject.subject_name,
      score: subject.average_percentage,
      classAverage: subject.class_average || 0,
      maxScore: 100,
    }));
  };

  // Transform data for detailed score table
  const getDetailedScoreData = () => {
    if (!performanceData?.assessment_history) return [];

    return performanceData.assessment_history.map((assessment) => ({
      subject: assessment.subject_name,
      assessmentName: assessment.assessment_name,
      date: assessment.date,
      score: assessment.score || assessment.percentage,
      grade: assessment.grade,
      maxMarks: assessment.max_marks,
      marksObtained: assessment.marks_obtained,
    }));
  };

  // Navigate back to students list
  const goBackToStudents = useCallback(() => {
    navigate("/students");
  }, [navigate]);

  // Handle refresh
  const handleRefresh = useCallback(() => {
    refresh();
  }, [refresh]);

  // Loading state
  if (loading) {
    return (
      <div className="student-profile-page">
        <Header />
        <div className="student-profile-container">
          <div className="profile-header">
            <div className="loading-skeleton profile-skeleton"></div>
            <div className="loading-skeleton info-skeleton"></div>
          </div>

          <div className="stats-grid">
            {[...Array(4)].map((_, index) => (
              <div key={index} className="loading-skeleton stat-skeleton"></div>
            ))}
          </div>

          <div className="profile-content">
            <div className="loading-skeleton chart-skeleton"></div>
            <div className="loading-skeleton chart-skeleton"></div>
          </div>
        </div>
      </div>
    );
  }

  // Error state
  if (error) {
    return (
      <div className="student-profile-page">
        <Header />
        <div className="student-profile-container">
          <div className="error-container">
            <div className="error-icon">⚠️</div>
            <h2 className="error-title">Unable to Load Student Profile</h2>
            <p className="error-message">{error}</p>
            <div className="error-actions">
              <button className="btn btn-primary" onClick={refresh}>
                Try Again
              </button>
              <button className="btn btn-secondary" onClick={goBackToStudents}>
                Back to Students
              </button>
            </div>
          </div>
        </div>
      </div>
    );
  }

  // Main render
  return (
    <div className="student-profile-page">
      <Header />

      <div className="student-profile-container">
        {/* Profile Header */}
        <div className="profile-header">
          <div className="profile-info">
            <div className="profile-avatar">
              <span className="avatar-text">
                {studentData?.full_name?.charAt(0)?.toUpperCase() || "S"}
              </span>
            </div>

            <div className="profile-details">
              <h1 className="student-name">
                {studentData?.full_name || "Unknown Student"}
              </h1>
              <p className="student-id">
                ID: {studentData?.student_roll_number || studentId}
              </p>
              <div className="profile-meta">
                <span className="meta-item">
                  <span className="meta-label">Overall Grade:</span>
                  <span
                    className={`grade-badge grade-${performanceData?.overall_grade?.toLowerCase()}`}
                  >
                    {performanceData?.overall_grade || "N/A"}
                  </span>
                </span>
                <span className="meta-item">
                  <span className="meta-label">Class Rank:</span>
                  <span className="rank-value">
                    #{performanceData?.class_rank || "N/A"}
                  </span>
                </span>
              </div>
            </div>
          </div>

          <div className="profile-actions">
            <button className="btn btn-secondary" onClick={goBackToStudents}>
              <span>←</span>
              Back to Students
            </button>
          </div>
        </div>

        {/* Performance Statistics */}
        <div className="stats-grid">
          <StatCard
            title="Overall Average"
            value={`${performanceData?.overall_average || 0}%`}
            subtitle={`Grade: ${performanceData?.overall_grade || "N/A"}`}
            icon="📊"
            color={getGradeColor(performanceData?.overall_grade)}
            trend={getPerformanceTrend(performanceData?.overall_average)}
          />

          <StatCard
            title="Subjects Enrolled"
            value={performanceData?.total_subjects || 0}
            subtitle="Active subjects"
            icon="📚"
            color="info"
          />

          <StatCard
            title="Assessments Taken"
            value={performanceData?.total_assessments || 0}
            subtitle="Completed assessments"
            icon="📝"
            color="primary"
          />

          <StatCard
            title="Class Rank"
            value={`#${performanceData?.class_rank || "N/A"}`}
            subtitle={`of ${performanceData?.total_students || "N/A"} students`}
            icon="🏆"
            color="success"
          />
        </div>

        {/* Tab Navigation */}
        <div className="tab-navigation">
          <button
            className={`tab-button ${activeTab === "overview" ? "active" : ""}`}
            onClick={() => setActiveTab("overview")}
          >
            📊 Overview
          </button>
          <button
            className={`tab-button ${activeTab === "analysis" ? "active" : ""}`}
            onClick={() => setActiveTab("analysis")}
          >
            🎯 Performance Analysis
          </button>
          <button
            className={`tab-button ${activeTab === "subjects" ? "active" : ""}`}
            onClick={() => setActiveTab("subjects")}
          >
            📚 Subject Details
          </button>
          <button
            className={`tab-button ${
              activeTab === "assessments" ? "active" : ""
            }`}
            onClick={() => setActiveTab("assessments")}
          >
            📋 Assessment Records
          </button>
        </div>

        {/* Tab Content */}
        <div className="tab-content">
          {activeTab === "overview" && (
            <div className="overview-tab">
              {/* Performance Trend Chart */}
              <div className="chart-card">
                <div className="chart-header">
                  <h2 className="chart-title">Performance Trends</h2>
                  <p className="chart-subtitle">
                    Student performance over time
                  </p>
                </div>
                <ClassPerformanceChart
                  data={getStudentPerformanceTrends()}
                  height={300}
                  color="#10b981"
                  showGrid={true}
                  showLegend={false}
                  loading={loading}
                  error={error}
                />
              </div>

              {/* Subject Performance Chart */}
              <div className="chart-card">
                <div className="chart-header">
                  <h2 className="chart-title">Subject Performance</h2>
                  <p className="chart-subtitle">
                    Performance across all subjects
                  </p>
                </div>
                <SubjectComparisonChart
                  data={getStudentSubjectData()}
                  height={300}
                  colorScheme="performance"
                  showGrid={true}
                  showLegend={false}
                  sortBy="average"
                  loading={loading}
                  error={error}
                />
              </div>
            </div>
          )}

          {activeTab === "analysis" && (
            <div className="analysis-tab">
              {/* Performance Radar Chart */}
              <div className="chart-card radar-chart-card">
                <div className="chart-header">
                  <h2 className="chart-title">
                    🎯 Strengths & Weaknesses Analysis
                  </h2>
                  <p className="chart-subtitle">
                    Multi-dimensional view of performance across all subjects
                  </p>
                </div>
                <PerformanceRadarChart
                  data={getRadarChartData()}
                  height={450}
                  showGrid={true}
                  showLegend={true}
                  colors={["#3b82f6", "#10b981", "#f59e0b"]}
                  loading={loading}
                  error={error}
                />
              </div>
            </div>
          )}

          {activeTab === "subjects" && (
            <div className="subjects-tab">
              <div className="subjects-grid">
                {performanceData?.subject_performance?.map((subject, index) => (
                  <div key={index} className="subject-detail-card">
                    <div className="subject-header">
                      <h3 className="subject-name">{subject.subject_name}</h3>
                      <span
                        className={`grade-badge grade-${subject.grade?.toLowerCase()}`}
                      >
                        {subject.grade}
                      </span>
                    </div>

                    <div className="subject-stats">
                      <div className="stat-row">
                        <span className="stat-label">Average:</span>
                        <span className="stat-value">
                          {subject.average_percentage}%
                        </span>
                      </div>
                      <div className="stat-row">
                        <span className="stat-label">Assessments:</span>
                        <span className="stat-value">
                          {subject.assessment_count}
                        </span>
                      </div>
                      <div className="stat-row">
                        <span className="stat-label">Best Score:</span>
                        <span className="stat-value">
                          {subject.best_score || "N/A"}%
                        </span>
                      </div>
                      <div className="stat-row">
                        <span className="stat-label">Class Rank:</span>
                        <span className="stat-value">
                          #{subject.class_rank || "N/A"}
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
          )}

          {activeTab === "assessments" && (
            <div className="assessments-tab">
              <div className="assessments-header">
                <h2 className="assessments-title">
                  📋 Complete Assessment History
                </h2>
                <p className="assessments-subtitle">
                  Detailed record of all assessments with sorting and filtering
                </p>
              </div>

              <DetailedScoreTable
                data={getDetailedScoreData()}
                loading={loading}
                error={error}
                pageSize={15}
                showPagination={true}
                className="student-score-table"
              />
            </div>
          )}
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

export default StudentProfilePage;
