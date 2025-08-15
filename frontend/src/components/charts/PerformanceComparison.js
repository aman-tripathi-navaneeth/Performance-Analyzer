import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
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
} from 'recharts';
import './PerformanceComparison.css';

const PerformanceComparison = ({ studentId, classYear, classSection }) => {
  const navigate = useNavigate();
  const [comparisonData, setComparisonData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [chartType, setChartType] = useState('bar');
  const [selectedTerm, setSelectedTerm] = useState('current');
  const [showExportMenu, setShowExportMenu] = useState(false);

  useEffect(() => {
    if (studentId && classYear && classSection) {
      loadComparisonData();
    }
  }, [studentId, classYear, classSection]);

  const loadComparisonData = async () => {
    try {
      setLoading(true);
      setError(null);

      // Simulate API call - replace with actual API
      await new Promise(resolve => setTimeout(resolve, 1000));
      
      // Mock data for demonstration
      const mockData = {
        student: {
          name: "Akash Gupta",
          id: studentId,
          overall: 85.6,
          subjects: [
            { name: "Mathematics", score: 88, trend: "up" },
            { name: "Physics", score: 82, trend: "down" },
            { name: "Chemistry", score: 85, trend: "up" },
            { name: "Computer Science", score: 90, trend: "up" },
            { name: "English", score: 78, trend: "down" }
          ]
        },
        class: {
          name: `${classYear} ${classSection}`,
          overall: 79.2,
          subjects: [
            { name: "Mathematics", score: 82 },
            { name: "Physics", score: 78 },
            { name: "Chemistry", score: 80 },
            { name: "Computer Science", score: 85 },
            { name: "English", score: 75 }
          ]
        }
      };

      setComparisonData(mockData);
    } catch (error) {
      console.error('Error loading comparison data:', error);
      setError('Error loading comparison data');
    } finally {
      setLoading(false);
    }
  };

  const chartColors = {
    student: '#1A73E8',
    class: '#DADCE0',
    success: '#34A853',
    warning: '#FBBC05',
    error: '#EA4335'
  };

  const getChartData = () => {
    if (!comparisonData) return [];

    return comparisonData.student.subjects.map(subject => ({
      subject: subject.name,
      [comparisonData.student.name]: subject.score,
      [`${comparisonData.class.name} (Class)`]: comparisonData.class.subjects.find(
        s => s.name === subject.name
      )?.score || 0
    }));
  };

  const CustomTooltip = ({ active, payload, label }) => {
    if (active && payload && payload.length) {
      return (
        <div className="bg-white p-4 border border-gray-200 rounded-lg shadow-xl backdrop-blur-sm">
          <p className="font-semibold text-gray-900 text-sm mb-2">{label}</p>
          {payload.map((entry, index) => (
            <p
              key={index}
              className="font-medium text-sm"
              style={{ color: entry.color }}
            >
              {entry.name}: {entry.value.toFixed(1)}%
            </p>
          ))}
        </div>
      );
    }
    return null;
  };

  const getPerformanceInsight = () => {
    if (!comparisonData) return '';
    
    const aboveAverage = comparisonData.student.subjects.filter(subject => {
      const classSubject = comparisonData.class.subjects.find(s => s.name === subject.name);
      return subject.score > (classSubject?.score || 0);
    }).length;
    
    const totalSubjects = comparisonData.student.subjects.length;
    
    if (aboveAverage === totalSubjects) {
      return `${comparisonData.student.name} is performing above average in all subjects. Excellent work!`;
    } else if (aboveAverage > totalSubjects / 2) {
      return `${comparisonData.student.name} is performing above average in ${aboveAverage} out of ${totalSubjects} subjects. Keep up the good work!`;
    } else {
      return `${comparisonData.student.name} has room for improvement. Focus on subjects where performance is below class average.`;
    }
  };

  const handleExport = (format) => {
    // Implement export functionality
    console.log(`Exporting as ${format}`);
    setShowExportMenu(false);
  };

  const handleBackClick = () => {
    navigate(-1);
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="flex items-center space-x-3">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
          <p className="text-gray-600 font-medium">Loading comparison data...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="text-red-500 text-lg mb-4">⚠️</div>
          <p className="text-gray-600 mb-4">{error}</p>
          <button
            onClick={handleBackClick}
            className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
          >
            ← Go Back
          </button>
        </div>
      </div>
    );
  }

  if (!comparisonData) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="text-gray-400 text-4xl mb-4">📊</div>
          <h3 className="text-xl font-semibold text-gray-700 mb-2">No Comparison Data Available</h3>
          <p className="text-gray-500 mb-6">No performance data available for this student and class.</p>
          <button
            onClick={handleBackClick}
            className="px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors shadow-md"
          >
            ← Go Back
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50 performance-comparison">
      {/* Header Section */}
      <div className="bg-white shadow-sm border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between">
            <div className="flex-1">
              <div className="flex items-center space-x-3 mb-2">
                <button
                  onClick={handleBackClick}
                  className="p-2 text-gray-400 hover:text-gray-600 transition-colors"
                >
                  <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
                  </svg>
                </button>
                <h1 className="text-2xl sm:text-3xl font-bold text-gray-900">
                  📊 Performance Comparison
                </h1>
              </div>
              <p className="text-lg text-gray-600">
                {comparisonData.student.name} vs {comparisonData.class.name}
              </p>
            </div>
            
            <div className="mt-4 sm:mt-0 flex items-center space-x-3">
              <select
                value={selectedTerm}
                onChange={(e) => setSelectedTerm(e.target.value)}
                className="px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
              >
                <option value="current">Current Term</option>
                <option value="previous">Previous Term</option>
                <option value="year">Full Year</option>
              </select>
              
              <div className="relative">
                <button
                  onClick={() => setShowExportMenu(!showExportMenu)}
                  className="px-4 py-2 bg-white border border-gray-300 rounded-lg hover:bg-gray-50 transition-colors flex items-center space-x-2"
                >
                  <span>📥</span>
                  <span>Export</span>
                </button>
                
                {showExportMenu && (
                  <div className="absolute right-0 mt-2 w-48 bg-white rounded-lg shadow-lg border border-gray-200 z-10 export-menu">
                    <button
                      onClick={() => handleExport('pdf')}
                      className="w-full px-4 py-2 text-left hover:bg-gray-50 rounded-t-lg"
                    >
                      📄 Export as PDF
                    </button>
                    <button
                      onClick={() => handleExport('csv')}
                      className="w-full px-4 py-2 text-left hover:bg-gray-50 rounded-b-lg"
                    >
                      📊 Export as CSV
                    </button>
                  </div>
                )}
              </div>
            </div>
          </div>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Chart Type Selector */}
        <div className="mb-8">
          <div className="flex flex-wrap gap-3 chart-selector">
            <button
              onClick={() => setChartType('bar')}
              className={`flex items-center space-x-2 px-6 py-3 rounded-full font-medium transition-all duration-200 chart-selector-btn ${
                chartType === 'bar'
                  ? 'bg-blue-600 text-white shadow-lg transform scale-105 active'
                  : 'bg-white text-gray-700 hover:bg-gray-50 hover:shadow-md border border-gray-200'
              }`}
            >
              <span>📊</span>
              <span>Bar Chart</span>
            </button>
            <button
              onClick={() => setChartType('line')}
              className={`flex items-center space-x-2 px-6 py-3 rounded-full font-medium transition-all duration-200 chart-selector-btn ${
                chartType === 'line'
                  ? 'bg-blue-600 text-white shadow-lg transform scale-105 active'
                  : 'bg-white text-gray-700 hover:bg-gray-50 hover:shadow-md border border-gray-200'
              }`}
            >
              <span>📈</span>
              <span>Line Chart</span>
            </button>
            <button
              onClick={() => setChartType('radar')}
              className={`flex items-center space-x-2 px-6 py-3 rounded-full font-medium transition-all duration-200 chart-selector-btn ${
                chartType === 'radar'
                  ? 'bg-blue-600 text-white shadow-lg transform scale-105 active'
                  : 'bg-white text-gray-700 hover:bg-gray-50 hover:shadow-md border border-gray-200'
              }`}
            >
              <span>🕸️</span>
              <span>Radar Chart</span>
            </button>
          </div>
        </div>

        {/* Overall Performance Section */}
        <div className="mb-8">
          <h2 className="text-xl font-semibold text-gray-900 mb-6">Overall Performance</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-200">
              <div className="flex items-center justify-between mb-4">
                <h3 className="font-semibold text-gray-900 text-lg">{comparisonData.student.name}</h3>
                <span className="text-2xl font-bold text-blue-600">{comparisonData.student.overall.toFixed(1)}%</span>
              </div>
              <div className="w-full bg-gray-200 rounded-full h-3">
                <div 
                  className="bg-gradient-to-r from-blue-600 to-blue-500 h-3 rounded-full transition-all duration-500 progress-bar"
                  style={{ width: `${comparisonData.student.overall}%` }}
                ></div>
              </div>
            </div>
            
            <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-200">
              <div className="flex items-center justify-between mb-4">
                <h3 className="font-semibold text-gray-900 text-lg">{comparisonData.class.name} (Class Average)</h3>
                <span className="text-2xl font-bold text-gray-600">{comparisonData.class.overall.toFixed(1)}%</span>
              </div>
              <div className="w-full bg-gray-200 rounded-full h-3">
                <div 
                  className="bg-gray-400 h-3 rounded-full transition-all duration-500 progress-bar"
                  style={{ width: `${comparisonData.class.overall}%` }}
                ></div>
              </div>
            </div>
          </div>
        </div>

        {/* Chart Display */}
        <div className="mb-8">
          <h2 className="text-xl font-semibold text-gray-900 mb-6">Subject-wise Comparison</h2>
          
          <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-200 chart-container">
            <ResponsiveContainer width="100%" height={500}>
              {chartType === 'radar' && (
                <RadarChart data={getChartData()}>
                  <PolarGrid stroke="#E5E7EB" strokeWidth={1} />
                  <PolarAngleAxis
                    dataKey="subject"
                    tick={{ fill: "#374151", fontSize: 14, fontWeight: "500" }}
                  />
                  <PolarRadiusAxis
                    angle={90}
                    domain={[0, 100]}
                    tick={{ fill: "#374151", fontSize: 12 }}
                  />
                  <Tooltip content={<CustomTooltip />} />
                  <Legend />
                  <Radar
                    name={comparisonData.student.name}
                    dataKey={comparisonData.student.name}
                    stroke={chartColors.student}
                    fill={chartColors.student}
                    fillOpacity={0.3}
                    strokeWidth={3}
                  />
                  <Radar
                    name={`${comparisonData.class.name} (Class)`}
                    dataKey={`${comparisonData.class.name} (Class)`}
                    stroke={chartColors.class}
                    fill={chartColors.class}
                    fillOpacity={0.3}
                    strokeWidth={3}
                  />
                </RadarChart>
              )}

              {chartType === 'bar' && (
                <BarChart data={getChartData()}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#E5E7EB" strokeWidth={1} />
                  <XAxis
                    dataKey="subject"
                    tick={{ fill: "#374151", fontSize: 14, fontWeight: "500" }}
                    axisLine={{ stroke: "#D1D5DB" }}
                    tickLine={{ stroke: "#D1D5DB" }}
                    angle={-45}
                    textAnchor="end"
                    height={80}
                    interval={0}
                  />
                  <YAxis
                    tick={{ fill: "#374151", fontSize: 12 }}
                    domain={[0, 100]}
                    axisLine={{ stroke: "#D1D5DB" }}
                    tickLine={{ stroke: "#D1D5DB" }}
                  />
                  <Tooltip content={<CustomTooltip />} />
                  <Legend />
                  <Bar
                    dataKey={comparisonData.student.name}
                    name={comparisonData.student.name}
                    fill={chartColors.student}
                    radius={[6, 6, 0, 0]}
                  />
                  <Bar
                    dataKey={`${comparisonData.class.name} (Class)`}
                    name={`${comparisonData.class.name} (Class)`}
                    fill={chartColors.class}
                    radius={[6, 6, 0, 0]}
                  />
                </BarChart>
              )}

              {chartType === 'line' && (
                <LineChart data={getChartData()}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#E5E7EB" strokeWidth={1} />
                  <XAxis
                    dataKey="subject"
                    tick={{ fill: "#374151", fontSize: 14, fontWeight: "500" }}
                    axisLine={{ stroke: "#D1D5DB" }}
                    tickLine={{ stroke: "#D1D5DB" }}
                    angle={-45}
                    textAnchor="end"
                    height={80}
                    interval={0}
                  />
                  <YAxis
                    tick={{ fill: "#374151", fontSize: 12 }}
                    domain={[0, 100]}
                    axisLine={{ stroke: "#D1D5DB" }}
                    tickLine={{ stroke: "#D1D5DB" }}
                  />
                  <Tooltip content={<CustomTooltip />} />
                  <Legend />
                  <Line
                    type="monotone"
                    dataKey={comparisonData.student.name}
                    name={comparisonData.student.name}
                    stroke={chartColors.student}
                    strokeWidth={4}
                    dot={{ fill: chartColors.student, strokeWidth: 2, r: 8 }}
                    activeDot={{ r: 10, stroke: chartColors.student, strokeWidth: 3 }}
                  />
                  <Line
                    type="monotone"
                    dataKey={`${comparisonData.class.name} (Class)`}
                    name={`${comparisonData.class.name} (Class)`}
                    stroke={chartColors.class}
                    strokeWidth={4}
                    dot={{ fill: chartColors.class, strokeWidth: 2, r: 8 }}
                    activeDot={{ r: 10, stroke: chartColors.class, strokeWidth: 3 }}
                  />
                </LineChart>
              )}
            </ResponsiveContainer>
          </div>
        </div>

        {/* Subject Cards Grid */}
        <div className="mb-8">
          <h2 className="text-xl font-semibold text-gray-900 mb-6">Detailed Subject Analysis</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {comparisonData.student.subjects.map((subject, index) => {
              const classSubject = comparisonData.class.subjects.find(
                s => s.name === subject.name
              );
              const difference = subject.score - (classSubject?.score || 0);
              const isAboveAverage = difference > 0;
              const performanceColor = isAboveAverage ? chartColors.success : chartColors.error;
              
              return (
                <div
                  key={index}
                  className="bg-white p-6 rounded-lg shadow-sm border border-gray-200 hover:shadow-md transition-shadow subject-card"
                >
                  <div className="flex items-center justify-between mb-4">
                    <h3 className="font-semibold text-gray-900 text-lg">{subject.name}</h3>
                    <span className={`text-sm ${subject.trend === 'up' ? 'text-green-600' : 'text-red-600'}`}>
                      {subject.trend === 'up' ? '⬆️' : '⬇️'}
                    </span>
                  </div>
                  
                  <div className="space-y-3">
                    <div className="flex justify-between items-center">
                      <span className="text-sm text-gray-600">{comparisonData.student.name}:</span>
                      <span className="font-semibold text-blue-600">{subject.score.toFixed(1)}%</span>
                    </div>
                    
                    <div className="flex justify-between items-center">
                      <span className="text-sm text-gray-600">Class Average:</span>
                      <span className="font-semibold text-gray-600">{(classSubject?.score || 0).toFixed(1)}%</span>
                    </div>
                    
                    <div className="pt-2 border-t border-gray-200">
                      <div className="flex justify-between items-center">
                        <span className="text-sm font-medium">Difference:</span>
                        <span className={`font-bold ${isAboveAverage ? 'text-green-600' : 'text-red-600'}`}>
                          {isAboveAverage ? '+' : ''}{difference.toFixed(1)}%
                        </span>
                      </div>
                    </div>
                    
                    <div className="w-full bg-gray-200 rounded-full h-2">
                      <div 
                        className="h-2 rounded-full transition-all duration-500 progress-bar"
                        style={{ 
                          width: `${subject.score}%`,
                          backgroundColor: performanceColor
                        }}
                      ></div>
                    </div>
                  </div>
                </div>
              );
            })}
          </div>
        </div>

        {/* Footer Section */}
        <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-200">
          <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between">
            <div className="flex-1 mb-4 sm:mb-0">
              <h3 className="text-lg font-semibold text-gray-900 mb-2">Performance Summary</h3>
              <p className="text-gray-600">{getPerformanceInsight()}</p>
            </div>
            
            <div className="flex space-x-3 export-buttons">
              <button
                onClick={() => handleExport('pdf')}
                className="px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors flex items-center space-x-2 btn-primary"
              >
                <span>📄</span>
                <span>Download Report</span>
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default PerformanceComparison;
