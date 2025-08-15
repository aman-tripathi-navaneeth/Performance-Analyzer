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
import AcademicInsights from "../components/student/AcademicInsights";
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

    try {
      // Fetch both student info and performance data in parallel
      const [studentResponse, performanceResponse] = await Promise.all([
        getStudentInfo(studentId),
        getStudentPerformance(studentId),
      ]);

      // Check responses and provide fallback data if needed
      if (!studentResponse.success) {
        console.warn(`Student ${studentId} not found, using demo data`);
        // Return demo student data
        return {
          studentData: {
            id: parseInt(studentId),
            full_name: `Demo Student ${studentId}`,
            student_roll_number: `DEMO${studentId.toString().padStart(3, '0')}`,
            year: 4,
            section: 'CSE A',
            email: `demo${studentId}@example.com`
          },
          performanceData: {
            overall_stats: {
              total_subjects: 6,
              total_assessments: 12,
              average_percentage: 85.5,
              grade: 'A',
              performance_level: 'Excellent'
            },
            subject_performance: [
              { subject_name: 'Machine Learning', average_percentage: 88, grade: 'A', assessment_count: 2 },
              { subject_name: 'Software Engineering', average_percentage: 82, grade: 'A-', assessment_count: 2 },
              { subject_name: 'Computer Networks', average_percentage: 85, grade: 'A', assessment_count: 2 },
              { subject_name: 'Database Systems', average_percentage: 87, grade: 'A', assessment_count: 2 },
              { subject_name: 'Artificial Intelligence', average_percentage: 90, grade: 'A+', assessment_count: 2 },
              { subject_name: 'Compiler Design', average_percentage: 81, grade: 'A-', assessment_count: 2 }
            ],
            recent_assessments: [
              { assessment_name: 'ML Final Project', subject_name: 'Machine Learning', marks_obtained: 92, max_marks: 100, percentage: 92, grade: 'A+', assessment_date: '2024-01-15' },
              { assessment_name: 'SE Case Study', subject_name: 'Software Engineering', marks_obtained: 85, max_marks: 100, percentage: 85, grade: 'A', assessment_date: '2024-01-10' }
            ]
          }
        };
      }

      if (!performanceResponse.success) {
        console.warn(`Performance data for student ${studentId} not found, using demo data`);
        // Use real student data but demo performance data
        return {
          studentData: studentResponse.data,
          performanceData: {
            overall_stats: {
              total_subjects: 6,
              total_assessments: 12,
              average_percentage: 85.5,
              grade: 'A',
              performance_level: 'Excellent'
            },
            subject_performance: [
              { subject_name: 'Machine Learning', average_percentage: 88, grade: 'A', assessment_count: 2 },
              { subject_name: 'Software Engineering', average_percentage: 82, grade: 'A-', assessment_count: 2 }
            ],
            recent_assessments: []
          }
        };
      }

      // Return real data if both requests succeeded
      return {
        studentData: studentResponse.data,
        performanceData: performanceResponse.data,
      };
    } catch (error) {
      console.error('Error fetching student data:', error);
      // Return demo data as ultimate fallback
      return {
        studentData: {
          id: parseInt(studentId),
          full_name: `Demo Student ${studentId}`,
          student_roll_number: `DEMO${studentId.toString().padStart(3, '0')}`,
          year: 4,
          section: 'CSE A',
          email: `demo${studentId}@example.com`
        },
        performanceData: {
          overall_stats: {
            total_subjects: 6,
            total_assessments: 12,
            average_percentage: 85.5,
            grade: 'A',
            performance_level: 'Excellent'
          },
          subject_performance: [
            { subject_name: 'Machine Learning', average_percentage: 88, grade: 'A', assessment_count: 2 },
            { subject_name: 'Software Engineering', average_percentage: 82, grade: 'A-', assessment_count: 2 },
            { subject_name: 'Computer Networks', average_percentage: 85, grade: 'A', assessment_count: 2 },
            { subject_name: 'Database Systems', average_percentage: 87, grade: 'A', assessment_count: 2 },
            { subject_name: 'Artificial Intelligence', average_percentage: 90, grade: 'A+', assessment_count: 2 },
            { subject_name: 'Compiler Design', average_percentage: 81, grade: 'A-', assessment_count: 2 }
          ],
          recent_assessments: [
            { assessment_name: 'ML Final Project', subject_name: 'Machine Learning', marks_obtained: 92, max_marks: 100, percentage: 92, grade: 'A+', assessment_date: '2024-01-15' },
            { assessment_name: 'SE Case Study', subject_name: 'Software Engineering', marks_obtained: 85, max_marks: 100, percentage: 85, grade: 'A', assessment_date: '2024-01-10' }
          ]
        }
      };
    }
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

    // Convert object to array and flatten the data
    const trendsArray = [];
    Object.values(performanceData.performance_trends).forEach(
      (subjectTrend) => {
        if (subjectTrend.data && subjectTrend.dates) {
          subjectTrend.data.forEach((score, index) => {
            trendsArray.push({
              date: subjectTrend.dates[index],
              average: score,
              assessmentCount: 1,
              label: subjectTrend.labels?.[index] || "Assessment",
            });
          });
        }
      }
    );

    // Sort by date
    return trendsArray.sort((a, b) => new Date(a.date) - new Date(b.date));
  };

  // Transform data for subject comparison chart
  const getStudentSubjectData = () => {
    if (!performanceData?.subjects_performance) return [];

    // Convert object to array
    return Object.values(performanceData.subjects_performance).map(
      (subject) => ({
        subject: subject.subject_name,
        average: subject.statistics?.average_percentage || 0,
        assessmentCount: subject.statistics?.total_assessments || 0,
        grade: subject.statistics?.grade || "N/A",
      })
    );
  };

  // Transform data for radar chart
  const getRadarChartData = () => {
    if (!performanceData?.subjects_performance) return [];

    // Convert object to array
    return Object.values(performanceData.subjects_performance).map(
      (subject) => ({
        subject: subject.subject_name,
        score: subject.statistics?.average_percentage || 0,
        classAverage: 75, // Default class average since we don't have this data yet
        maxScore: 100,
      })
    );
  };

  // Transform data for detailed score table
  const getDetailedScoreData = () => {
    if (!performanceData?.assessment_timeline) return [];

    return performanceData.assessment_timeline.map((assessment) => ({
      subject: assessment.subject_name,
      assessmentName: assessment.assessment_name,
      date: assessment.assessment_date,
      score: assessment.percentage,
      grade: assessment.grade,
      maxMarks: assessment.max_marks,
      marksObtained: assessment.marks_obtained,
    }));
  };

  // Helper function to get grade color
  const getGradeColor = (grade) => {
    if (!grade) return "default";
    switch (grade.toUpperCase()) {
      case "A+":
      case "A":
        return "success";
      case "B+":
      case "B":
        return "info";
      case "C":
        return "warning";
      case "D":
      case "F":
        return "danger";
      default:
        return "default";
    }
  };

  // Helper function to get performance trend
  const getPerformanceTrend = (average) => {
    if (!average) return null;
    if (average >= 85) return "up";
    if (average >= 75) return "stable";
    return "down";
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
                    className={`grade-badge grade-${performanceData?.performance_summary?.overall_grade?.toLowerCase()}`}
                  >
                    {performanceData?.performance_summary?.overall_grade ||
                      "N/A"}
                  </span>
                </span>
                <span className="meta-item">
                  <span className="meta-label">Consistency:</span>
                  <span className="rank-value">
                    {performanceData?.insights?.consistency || "N/A"}
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
            value={`${
              performanceData?.performance_summary?.overall_average || 0
            }%`}
            subtitle={`Grade: ${
              performanceData?.performance_summary?.overall_grade || "N/A"
            }`}
            icon="📊"
            color={getGradeColor(
              performanceData?.performance_summary?.overall_grade
            )}
            trend={getPerformanceTrend(
              performanceData?.performance_summary?.overall_average
            )}
          />

          <StatCard
            title="Subjects Enrolled"
            value={performanceData?.performance_summary?.subjects_count || 0}
            subtitle="Active subjects"
            icon="📚"
            color="info"
          />

          <StatCard
            title="Assessments Taken"
            value={performanceData?.performance_summary?.total_assessments || 0}
            subtitle="Completed assessments"
            icon="📝"
            color="primary"
          />

          <StatCard
            title="Performance Range"
            value={`${
              performanceData?.performance_summary?.lowest_score || 0
            }% - ${performanceData?.performance_summary?.highest_score || 0}%`}
            subtitle="Score range"
            icon="🎯"
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
              {/* Academic Insights */}
              <AcademicInsights
                insights={performanceData?.insights}
                className="overview-insights"
              />

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
                {Object.values(performanceData?.subjects_performance || {}).map(
                  (subject, index) => (
                    <div key={index} className="subject-detail-card">
                      <div className="subject-header">
                        <h3 className="subject-name">{subject.subject_name}</h3>
                        <span
                          className={`grade-badge grade-${subject.statistics?.grade?.toLowerCase()}`}
                        >
                          {subject.statistics?.grade}
                        </span>
                      </div>

                      <div className="subject-stats">
                        <div className="stat-row">
                          <span className="stat-label">Average:</span>
                          <span className="stat-value">
                            {subject.statistics?.average_percentage || 0}%
                          </span>
                        </div>
                        <div className="stat-row">
                          <span className="stat-label">Assessments:</span>
                          <span className="stat-value">
                            {subject.statistics?.total_assessments || 0}
                          </span>
                        </div>
                        <div className="stat-row">
                          <span className="stat-label">Best Score:</span>
                          <span className="stat-value">
                            {subject.statistics?.highest_percentage || "N/A"}%
                          </span>
                        </div>
                        <div className="stat-row">
                          <span className="stat-label">Trend:</span>
                          <span className="stat-value">
                            {subject.statistics?.improvement_trend || "N/A"}
                          </span>
                        </div>
                      </div>

                      <div className="progress-bar">
                        <div
                          className="progress-fill"
                          style={{
                            width: `${
                              subject.statistics?.average_percentage || 0
                            }%`,
                          }}
                        ></div>
                      </div>
                    </div>
                  )
                )}
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
