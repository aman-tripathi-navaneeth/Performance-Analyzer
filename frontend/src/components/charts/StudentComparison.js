import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import {
  RadarChart,
  PolarGrid,
  PolarAngleAxis,
  PolarRadiusAxis,
  Radar,
  ResponsiveContainer,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  LineChart,
  Line,
} from "recharts";
import { getStudentPerformance, getClassPerformance } from "../../api/apiService";
import "./StudentComparison.css";

const StudentComparison = ({ studentId, classYear, classSection }) => {
  const navigate = useNavigate();
  const [comparisonData, setComparisonData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [chartType, setChartType] = useState("radar");

  useEffect(() => {
    if (studentId && classYear && classSection) {
      loadComparisonData();
    }
  }, [studentId, classYear, classSection]);

  const loadComparisonData = async () => {
    try {
      setLoading(true);
      setError(null);

      // Load both student and class data
      const [studentData, classData] = await Promise.all([
        getStudentPerformance(studentId),
        getClassPerformance(classYear, classSection)
      ]);

      if (studentData.success && classData.success) {
        const comparison = createComparisonData(studentData.data, classData.data);
        setComparisonData(comparison);
      } else {
        setError("Failed to load comparison data");
      }
    } catch (error) {
      console.error("Error loading comparison data:", error);
      setError("Error loading comparison data");
      // Use mock data as fallback for development
      setComparisonData(getMockComparisonData());
    } finally {
      setLoading(false);
    }
  };

  const createComparisonData = (studentData, classData) => {
    const student = studentData.student || {};
    const classPerformance = classData.subjects_performance || {};
    
    // Create radar chart data
    const radarData = Object.keys(classPerformance).map(subject => ({
      subject: subject,
      student: studentData.performance?.[subject]?.average || 0,
      classAverage: classPerformance[subject]?.statistics?.average_percentage || 0,
      fullMark: 100
    }));

    // Create bar chart data
    const barData = radarData.map(item => ({
      name: item.subject,
      student: item.student,
      class: item.classAverage,
      difference: item.student - item.classAverage
    }));

    // Create overall performance data
    const overallStudent = radarData.reduce((sum, item) => sum + item.student, 0) / radarData.length;
    const overallClass = radarData.reduce((sum, item) => sum + item.classAverage, 0) / radarData.length;

    return {
      student: student,
      radar: radarData,
      bar: barData,
      overall: {
        student: overallStudent,
        class: overallClass,
        difference: overallStudent - overallClass
      }
    };
  };

  const getMockComparisonData = () => ({
    student: {
      name: "Aditi Patel",
      id: "21A91A0501",
      year: "2nd Year",
      section: "CSE A"
    },
    radar: [
      { subject: "Mathematics", student: 85, classAverage: 78, fullMark: 100 },
      { subject: "Data Structures", student: 92, classAverage: 82, fullMark: 100 },
      { subject: "Database Systems", student: 88, classAverage: 75, fullMark: 100 },
      { subject: "OOP", student: 90, classAverage: 80, fullMark: 100 },
      { subject: "Networks", student: 78, classAverage: 72, fullMark: 100 }
    ],
    bar: [
      { name: "Math", student: 85, class: 78, difference: 7 },
      { name: "DS", student: 92, class: 82, difference: 10 },
      { name: "DBMS", student: 88, class: 75, difference: 13 },
      { name: "OOP", student: 90, class: 80, difference: 10 },
      { name: "Networks", student: 78, class: 72, difference: 6 }
    ],
    overall: {
      student: 86.6,
      class: 77.4,
      difference: 9.2
    }
  });

  const CustomTooltip = ({ active, payload, label }) => {
    if (active && payload && payload.length) {
      return (
        <div className="comparison-tooltip">
          <p className="tooltip-label">{label}</p>
          {payload.map((entry, index) => (
            <p key={index} style={{ color: entry.color }}>
              {entry.name}: {entry.value.toFixed(1)}%
            </p>
          ))}
        </div>
      );
    }
    return null;
  };

  const handleBackToAnalysis = () => {
    navigate(-1);
  };

  if (loading) {
    return (
      <div className="student-comparison-container">
        <div className="comparison-loading">
          <div className="loading-spinner"></div>
          <p>Loading comparison data...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="student-comparison-container">
        <div className="comparison-error">
          <div className="error-icon">⚠️</div>
          <p>{error}</p>
          <button onClick={loadComparisonData} className="retry-button">
            Try Again
          </button>
        </div>
      </div>
    );
  }

  if (!comparisonData) return null;

  return (
    <div className="student-comparison-container">
      {/* Header Section */}
      <div className="comparison-header">
        <button onClick={handleBackToAnalysis} className="back-button">
          <span className="back-icon">←</span>
          Back to Analysis
        </button>
        
        <div className="header-content">
          <h1 className="comparison-title">Student vs Class Comparison</h1>
          <p className="comparison-subtitle">
            Comparing {comparisonData.student.name} with {classYear} Year {classSection}
          </p>
        </div>
      </div>

      {/* Overall Performance Cards */}
      <div className="performance-overview">
        <div className="performance-card student-card">
          <div className="card-header">
            <h3>{comparisonData.student.name}</h3>
            <span className="card-badge student-badge">Student</span>
          </div>
          <div className="performance-score">
            <span className="score-value">{comparisonData.overall.student.toFixed(1)}%</span>
            <span className="score-label">Overall Performance</span>
          </div>
        </div>

        <div className="performance-card class-card">
          <div className="card-header">
            <h3>{classYear} Year {classSection}</h3>
            <span className="card-badge class-badge">Class Average</span>
          </div>
          <div className="performance-score">
            <span className="score-value">{comparisonData.overall.class.toFixed(1)}%</span>
            <span className="score-label">Class Average</span>
          </div>
        </div>

        <div className="performance-card difference-card">
          <div className="card-header">
            <h3>Performance Gap</h3>
            <span className={`card-badge ${comparisonData.overall.difference >= 0 ? 'positive-badge' : 'negative-badge'}`}>
              {comparisonData.overall.difference >= 0 ? 'Above Average' : 'Below Average'}
            </span>
          </div>
          <div className="performance-score">
            <span className={`score-value ${comparisonData.overall.difference >= 0 ? 'positive' : 'negative'}`}>
              {comparisonData.overall.difference >= 0 ? '+' : ''}{comparisonData.overall.difference.toFixed(1)}%
            </span>
            <span className="score-label">Difference</span>
          </div>
        </div>
      </div>

      {/* Chart Type Selector */}
      <div className="chart-selector">
        <button
          onClick={() => setChartType("radar")}
          className={`chart-tab ${chartType === "radar" ? "active" : ""}`}
        >
          🎯 Radar View
        </button>
        <button
          onClick={() => setChartType("bar")}
          className={`chart-tab ${chartType === "bar" ? "active" : ""}`}
        >
          📊 Bar Comparison
        </button>
        <button
          onClick={() => setChartType("line")}
          className={`chart-tab ${chartType === "line" ? "active" : ""}`}
        >
          📈 Line Comparison
        </button>
      </div>

      {/* Charts Container */}
      <div className="charts-section">
        {chartType === "radar" && (
          <div className="chart-container radar-container">
            <div className="chart-header">
              <h2 className="chart-title">🎯 Strengths & Weaknesses Analysis</h2>
              <p className="chart-subtitle">
                Multi-dimensional view of performance across all subjects
              </p>
            </div>
            <div className="chart-wrapper">
              <ResponsiveContainer width="100%" height={500}>
                <RadarChart data={comparisonData.radar} margin={{ top: 40, right: 80, bottom: 40, left: 80 }}>
                  <PolarGrid stroke="rgba(226, 232, 240, 0.6)" strokeWidth={1} />
                  <PolarAngleAxis
                    dataKey="subject"
                    tick={{ fill: "#64748b", fontSize: 12, fontWeight: "600" }}
                  />
                  <PolarRadiusAxis
                    angle={90}
                    domain={[0, 100]}
                    tick={{ fill: "#64748b", fontSize: 10 }}
                    tickCount={5}
                  />
                  <Tooltip content={<CustomTooltip />} />
                  <Legend 
                    wrapperStyle={{ 
                      paddingTop: '20px',
                      fontSize: '14px',
                      fontWeight: '600'
                    }}
                  />
                  <Radar
                    name="Student Performance"
                    dataKey="student"
                    stroke="#3b82f6"
                    fill="#3b82f6"
                    fillOpacity={0.3}
                    strokeWidth={3}
                  />
                  <Radar
                    name="Class Average"
                    dataKey="classAverage"
                    stroke="#10b981"
                    fill="#10b981"
                    fillOpacity={0.2}
                    strokeWidth={2}
                    strokeDasharray="5 5"
                  />
                </RadarChart>
              </ResponsiveContainer>
            </div>
          </div>
        )}

        {chartType === "bar" && (
          <div className="chart-container bar-container">
            <div className="chart-header">
              <h2 className="chart-title">📊 Subject-wise Comparison</h2>
              <p className="chart-subtitle">
                Direct comparison of student performance vs class average
              </p>
            </div>
            <div className="chart-wrapper">
              <ResponsiveContainer width="100%" height={500}>
                <BarChart data={comparisonData.bar} margin={{ top: 20, right: 30, left: 20, bottom: 60 }}>
                  <CartesianGrid strokeDasharray="3 3" stroke="rgba(226, 232, 240, 0.6)" strokeWidth={1} />
                  <XAxis
                    dataKey="name"
                    tick={{ fill: "#64748b", fontSize: 12, fontWeight: "600" }}
                    axisLine={{ stroke: "#d1d5db" }}
                    tickLine={{ stroke: "#d1d5db" }}
                    angle={-45}
                    textAnchor="end"
                    height={60}
                  />
                  <YAxis
                    tick={{ fill: "#64748b", fontSize: 12 }}
                    axisLine={{ stroke: "#d1d5db" }}
                    tickLine={{ stroke: "#d1d5db" }}
                    domain={[0, 100]}
                  />
                  <Tooltip content={<CustomTooltip />} />
                  <Legend 
                    wrapperStyle={{ 
                      paddingTop: '20px',
                      fontSize: '14px',
                      fontWeight: '600'
                    }}
                  />
                  <Bar
                    dataKey="student"
                    name="Student Performance"
                    fill="#3b82f6"
                    radius={[4, 4, 0, 0]}
                    stroke="#3b82f6"
                    strokeWidth={1}
                  />
                  <Bar
                    dataKey="class"
                    name="Class Average"
                    fill="#10b981"
                    radius={[4, 4, 0, 0]}
                    stroke="#10b981"
                    strokeWidth={1}
                  />
                </BarChart>
              </ResponsiveContainer>
            </div>
          </div>
        )}

        {chartType === "line" && (
          <div className="chart-container line-container">
            <div className="chart-header">
              <h2 className="chart-title">📈 Performance Trends</h2>
              <p className="chart-subtitle">
                Comparative performance trends across subjects
              </p>
            </div>
            <div className="chart-wrapper">
              <ResponsiveContainer width="100%" height={500}>
                <LineChart data={comparisonData.bar} margin={{ top: 20, right: 30, left: 20, bottom: 60 }}>
                  <CartesianGrid strokeDasharray="3 3" stroke="rgba(226, 232, 240, 0.6)" strokeWidth={1} />
                  <XAxis
                    dataKey="name"
                    tick={{ fill: "#64748b", fontSize: 12, fontWeight: "600" }}
                    axisLine={{ stroke: "#d1d5db" }}
                    tickLine={{ stroke: "#d1d5db" }}
                    angle={-45}
                    textAnchor="end"
                    height={60}
                  />
                  <YAxis
                    tick={{ fill: "#64748b", fontSize: 12 }}
                    axisLine={{ stroke: "#d1d5db" }}
                    tickLine={{ stroke: "#d1d5db" }}
                    domain={[0, 100]}
                  />
                  <Tooltip content={<CustomTooltip />} />
                  <Legend 
                    wrapperStyle={{ 
                      paddingTop: '20px',
                      fontSize: '14px',
                      fontWeight: '600'
                    }}
                  />
                  <Line
                    type="monotone"
                    dataKey="student"
                    name="Student Performance"
                    stroke="#3b82f6"
                    strokeWidth={4}
                    dot={{ fill: "#3b82f6", strokeWidth: 2, r: 6 }}
                    activeDot={{ r: 8, stroke: "#3b82f6", strokeWidth: 3 }}
                  />
                  <Line
                    type="monotone"
                    dataKey="class"
                    name="Class Average"
                    stroke="#10b981"
                    strokeWidth={3}
                    strokeDasharray="8 8"
                    dot={{ fill: "#10b981", strokeWidth: 2, r: 5 }}
                    activeDot={{ r: 7, stroke: "#10b981", strokeWidth: 2 }}
                  />
                </LineChart>
              </ResponsiveContainer>
            </div>
          </div>
        )}
      </div>

      {/* Subject-wise Comparison Table */}
      <div className="subjects-comparison-table">
        <div className="table-header">
          <h2 className="table-title">📈 Detailed Subject Analysis</h2>
          <p className="table-subtitle">Performance breakdown by subject</p>
        </div>
        
        <div className="comparison-table">
          <div className="table-row table-header-row">
            <div className="table-cell">Subject</div>
            <div className="table-cell">Student Score</div>
            <div className="table-cell">Class Average</div>
            <div className="table-cell">Difference</div>
            <div className="table-cell">Status</div>
          </div>
          
          {comparisonData.bar.map((subject, index) => (
            <div key={index} className="table-row">
              <div className="table-cell subject-name">{subject.name}</div>
              <div className="table-cell student-score">{subject.student.toFixed(1)}%</div>
              <div className="table-cell class-score">{subject.class.toFixed(1)}%</div>
              <div className={`table-cell difference ${subject.difference >= 0 ? 'positive' : 'negative'}`}>
                {subject.difference >= 0 ? '+' : ''}{subject.difference.toFixed(1)}%
              </div>
              <div className="table-cell">
                <span className={`status-badge ${subject.difference >= 0 ? 'above' : 'below'}`}>
                  {subject.difference >= 0 ? 'Above Average' : 'Below Average'}
                </span>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default StudentComparison; 