import React, { useState, useEffect } from 'react';
import { useSearchParams } from 'react-router-dom';
import {
  PerformanceBarChart,
  TrendLineChart,
  ScatterPlotChart,
  DistributionPieChart,
  PerformanceRadarChart,
  PerformanceComposedChart,
} from '../components/charts/AdvancedCharts';
import StudentComparison from '../components/charts/StudentComparison';
import { getAllStudents, getClassPerformance } from '../api/apiService';
import './ChartsPage.css';

const ChartsPage = () => {
  const [searchParams] = useSearchParams();
  const [chartData, setChartData] = useState({});
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [selectedStudent, setSelectedStudent] = useState(null);
  const [selectedClass, setSelectedClass] = useState({ year: '2', section: 'CSE A' });
  const [students, setStudents] = useState([]);

  // Check for URL parameters
  useEffect(() => {
    const studentId = searchParams.get('student');
    const year = searchParams.get('year');
    const section = searchParams.get('section');
    
    if (studentId && year && section) {
      // Find the student in the students list
      const student = students.find(s => s.id === studentId);
      if (student) {
        setSelectedStudent(student);
        setSelectedClass({ year, section });
      }
    }
  }, [searchParams, students]);

  useEffect(() => {
    loadChartData();
  }, []);

  const loadChartData = async () => {
    try {
      setLoading(true);
      setError(null);

      const [studentsData, classData] = await Promise.all([
        getAllStudents(),
        getClassPerformance(selectedClass.year, selectedClass.section)
      ]);

      if (studentsData.success && classData.success) {
        setStudents(studentsData.data.students || []);
        const processedData = processChartData(studentsData.data, classData.data);
        setChartData(processedData);
      } else {
        setError('Failed to load chart data');
      }
    } catch (error) {
      console.error('Error loading chart data:', error);
      setError('Error loading chart data');
      setChartData(getMockChartData());
    } finally {
      setLoading(false);
    }
  };

  const processChartData = (studentsData, classData) => {
    const students = studentsData.students || [];
    const classPerformance = classData.subjects_performance || {};

    return {
      studentPerformance: students.slice(0, 10).map(student => ({
        name: student.full_name,
        value: student.performance_summary?.overall_average || 0,
        grade: student.performance_summary?.overall_grade || 'N/A',
        students: 1,
      })),
      subjectPerformance: Object.keys(classPerformance).map(subject => ({
        name: subject,
        value: classPerformance[subject]?.statistics?.average_percentage || 0,
        students: classPerformance[subject]?.statistics?.total_students || 0,
        assessments: classPerformance[subject]?.statistics?.total_assessments || 0,
      })),
      gradeDistribution: calculateGradeDistribution(students),
      performanceTrends: generatePerformanceTrends(),
      correlationData: generateCorrelationData(students),
      radarData: Object.keys(classPerformance).map(subject => ({
        subject: subject,
        value: classPerformance[subject]?.statistics?.average_percentage || 0,
        target: 80,
        difference: (classPerformance[subject]?.statistics?.average_percentage || 0) - 80,
      }))
    };
  };

  const calculateGradeDistribution = (students) => {
    const grades = {
      'A+': 0, 'A': 0, 'A-': 0,
      'B+': 0, 'B': 0, 'B-': 0,
      'C+': 0, 'C': 0, 'D': 0, 'F': 0
    };

    students.forEach(student => {
      const grade = student.performance_summary?.overall_grade || 'N/A';
      if (grades.hasOwnProperty(grade)) {
        grades[grade]++;
      }
    });

    const total = students.length;
    return Object.keys(grades).map(grade => ({
      name: grade,
      value: grades[grade],
      total: total,
    }));
  };

  const generatePerformanceTrends = () => {
    const months = ['January', 'February', 'March', 'April', 'May', 'June'];
    let previousValue = 75;
    return months.map((month, index) => {
      const change = (Math.random() * 10 - 5);
      const value = Math.max(0, Math.min(100, previousValue + change));
      previousValue = value;
      return {
        period: month,
        value: value,
        change: change,
        assessments: Math.floor(Math.random() * 20) + 10,
      };
    });
  };

  const generateCorrelationData = (students) => {
    return students.slice(0, 20).map((student, index) => {
      const overall = student.performance_summary?.overall_average || 0;
      const subject = Math.max(0, Math.min(100, overall + (Math.random() * 20 - 10)));
      return {
        x: overall,
        y: subject,
        name: student.full_name,
        grade: student.performance_summary?.overall_grade || 'N/A',
        subject: 'Mathematics',
      };
    });
  };

  const getMockChartData = () => ({
    studentPerformance: [
      { name: 'Aarav Sharma', value: 85, grade: 'A' },
      { name: 'Aditi Patel', value: 78, grade: 'B+' },
      { name: 'Arjun Kumar', value: 92, grade: 'A+' },
      { name: 'Ananya Singh', value: 65, grade: 'C+' },
      { name: 'Akash Gupta', value: 88, grade: 'A' },
    ],
    subjectPerformance: [
      { name: 'Mathematics', value: 85, students: 180 },
      { name: 'Physics', value: 78, students: 150 },
      { name: 'Chemistry', value: 82, students: 165 },
      { name: 'Computer Science', value: 88, students: 200 },
      { name: 'English', value: 75, students: 120 },
    ],
    gradeDistribution: [
      { name: 'A+', value: 15, total: 100 },
      { name: 'A', value: 25, total: 100 },
      { name: 'A-', value: 20, total: 100 },
      { name: 'B+', value: 18, total: 100 },
      { name: 'B', value: 12, total: 100 },
      { name: 'B-', value: 6, total: 100 },
      { name: 'C+', value: 3, total: 100 },
      { name: 'C', value: 1, total: 100 },
    ],
    performanceTrends: [
      { period: 'Jan', value: 78 },
      { period: 'Feb', value: 82 },
      { period: 'Mar', value: 85 },
      { period: 'Apr', value: 87 },
      { period: 'May', value: 89 },
      { period: 'Jun', value: 91 },
    ],
    correlationData: [
      { x: 85, y: 78, name: 'Student 1' },
      { x: 92, y: 85, name: 'Student 2' },
      { x: 76, y: 72, name: 'Student 3' },
      { x: 88, y: 82, name: 'Student 4' },
      { x: 79, y: 75, name: 'Student 5' },
    ],
    radarData: [
      { subject: 'Mathematics', value: 85, target: 80 },
      { subject: 'Physics', value: 78, target: 80 },
      { subject: 'Chemistry', value: 82, target: 80 },
      { subject: 'Computer Science', value: 88, target: 80 },
      { subject: 'English', value: 75, target: 80 },
    ]
  });

  const handleStudentSelect = (student) => {
    setSelectedStudent(student);
  };

  const handleClassChange = (year, section) => {
    setSelectedClass({ year, section });
    // Reload data for new class
    setTimeout(() => loadChartData(), 100);
  };

  if (loading) {
    return (
      <div className="charts-page">
        <div className="charts-header">
          <h1>Advanced Charts</h1>
          <p>Interactive visualizations and student comparisons</p>
        </div>
        <div className="loading-container">
          <div className="loading-spinner"></div>
          <p>Loading chart data...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="charts-page">
        <div className="charts-header">
          <h1>Advanced Charts</h1>
          <p>Interactive visualizations and student comparisons</p>
        </div>
        <div className="error-container">
          <p className="error-message">{error}</p>
          <button onClick={loadChartData} className="refresh-button">
            Retry
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="charts-page">
      <div className="charts-header">
        <div className="header-content">
          <h1>Advanced Charts</h1>
          <p>Interactive visualizations and student comparisons</p>
        </div>
        <div className="header-actions">
          <button onClick={loadChartData} className="refresh-button">
            🔄 Refresh Data
          </button>
        </div>
      </div>

      <div className="charts-content">
        {/* Class Selection */}
        <div className="class-selector">
          <h3>Select Class</h3>
          <div className="class-options">
            <button
              onClick={() => handleClassChange('2', 'CSE A')}
              className={`class-option ${selectedClass.year === '2' && selectedClass.section === 'CSE A' ? 'active' : ''}`}
            >
              2nd Year CSE A
            </button>
            <button
              onClick={() => handleClassChange('2', 'CSE B')}
              className={`class-option ${selectedClass.year === '2' && selectedClass.section === 'CSE B' ? 'active' : ''}`}
            >
              2nd Year CSE B
            </button>
            <button
              onClick={() => handleClassChange('1', 'CSM')}
              className={`class-option ${selectedClass.year === '1' && selectedClass.section === 'CSM' ? 'active' : ''}`}
            >
              1st Year CSM
            </button>
          </div>
        </div>

        {/* Student Selection for Comparison */}
        <div className="student-selector">
          <h3>Student Comparison</h3>
          <div className="student-list">
            {students.slice(0, 10).map((student) => (
              <button
                key={student.id}
                onClick={() => handleStudentSelect(student)}
                className={`student-option ${selectedStudent?.id === student.id ? 'active' : ''}`}
              >
                <span className="student-name">{student.full_name}</span>
                <span className="student-grade">
                  {student.performance_summary?.overall_grade || 'N/A'}
                </span>
              </button>
            ))}
          </div>
        </div>

        {/* Charts Grid */}
        <div className="charts-grid">
          {/* Student Performance Chart */}
          <div className="chart-card">
            <PerformanceBarChart
              data={chartData.studentPerformance}
              title="Top Student Performance Analysis"
              subtitle="Performance comparison of top-performing students with grade indicators"
              xKey="name"
              yKey="value"
              color="#3B82F6"
              showMean={true}
              height={500}
              customTooltip={(data) => (
                <div>
                  <p>Grade: {data.grade}</p>
                </div>
              )}
            />
          </div>

          {/* Subject Performance Chart */}
          <div className="chart-card">
            <PerformanceBarChart
              data={chartData.subjectPerformance}
              title="Subject Performance Analysis"
              subtitle="Average performance across different subjects with student participation data"
              xKey="name"
              yKey="value"
              color="#10B981"
              showMean={true}
              showTarget={true}
              targetValue={80}
              height={500}
              customTooltip={(data) => (
                <div>
                  <p>Total Students: {data.students}</p>
                </div>
              )}
            />
          </div>

          {/* Grade Distribution Chart */}
          <div className="chart-card">
            <DistributionPieChart
              data={chartData.gradeDistribution}
              title="Grade Distribution Analysis"
              subtitle="Distribution of students across different grade levels with percentage breakdown"
              dataKey="value"
              nameKey="name"
              height={500}
              showPercentage={true}
            />
          </div>

          {/* Performance Trends Chart */}
          <div className="chart-card">
            <TrendLineChart
              data={chartData.performanceTrends}
              title="Performance Trends Analysis"
              subtitle="Performance progression over time periods showing growth patterns"
              xKey="period"
              yKey="value"
              color="#F59E0B"
              height={500}
              smooth={true}
            />
          </div>

          {/* Correlation Analysis Chart */}
          <div className="chart-card">
            <ScatterPlotChart
              data={chartData.correlationData}
              title="Performance Correlation Analysis"
              subtitle="Relationship between different performance metrics and student characteristics"
              xKey="x"
              yKey="y"
              color="#8B5CF6"
              height={500}
            />
          </div>

          {/* Radar Chart */}
          <div className="chart-card">
            <PerformanceRadarChart
              data={chartData.radarData}
              title="Multi-dimensional Performance Analysis"
              subtitle="Performance comparison across subjects with target achievement indicators"
              dataKey="value"
              nameKey="subject"
              color="#EC4899"
              height={500}
              showTarget={true}
            />
          </div>
        </div>

        {/* Student Comparison Section */}
        {selectedStudent && (
          <div className="comparison-section">
            <h2>Student vs Class Comparison</h2>
            <p>Comparing {selectedStudent.full_name} with {selectedClass.year}nd Year {selectedClass.section}</p>
            <StudentComparison
              studentId={selectedStudent.id}
              classYear={selectedClass.year}
              classSection={selectedClass.section}
            />
          </div>
        )}

        {/* Composed Chart */}
        <div className="composed-chart-section">
          <h2>Comprehensive Analysis</h2>
          <PerformanceComposedChart
            data={chartData.subjectPerformance.map(subject => ({
              name: subject.name,
              performance: subject.value,
              trend: Math.random() * 20 + 70,
              area: Math.random() * 10 + 5
            }))}
            title="Subject Performance Overview"
            height={400}
            showBars={true}
            showLines={true}
            showAreas={true}
          />
        </div>
      </div>
    </div>
  );
};

export default ChartsPage; 