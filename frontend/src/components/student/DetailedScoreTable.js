import { useState, useMemo } from 'react';
import PropTypes from 'prop-types';
import './StudentComponents.css';

/**
 * DetailedScoreTable Component - Sortable table displaying student's performance records
 * Shows detailed assessment data with sorting and filtering capabilities
 */
const DetailedScoreTable = ({
  data = [],
  loading = false,
  error = null,
  pageSize = 10,
  showPagination = true,
  className = ''
}) => {
  // Component state
  const [sortConfig, setSortConfig] = useState({ key: 'date', direction: 'desc' });
  const [currentPage, setCurrentPage] = useState(1);
  const [filterSubject, setFilterSubject] = useState('');
  const [searchTerm, setSearchTerm] = useState('');

  // Get unique subjects for filter dropdown (always call hooks)
  const subjects = useMemo(() => {
    if (!data || data.length === 0) return [];
    const uniqueSubjects = [...new Set(data.map(item => item.subject || item.subjectName))];
    return uniqueSubjects.filter(Boolean).sort();
  }, [data]);

  // Filter and search data (always call hooks)
  const filteredData = useMemo(() => {
    if (!data || data.length === 0) return [];
    return data.filter(item => {
      const matchesSubject = !filterSubject || 
        (item.subject || item.subjectName || '').toLowerCase().includes(filterSubject.toLowerCase());
      
      const matchesSearch = !searchTerm || 
        (item.assessmentName || item.assessment || '').toLowerCase().includes(searchTerm.toLowerCase()) ||
        (item.subject || item.subjectName || '').toLowerCase().includes(searchTerm.toLowerCase());
      
      return matchesSubject && matchesSearch;
    });
  }, [data, filterSubject, searchTerm]);

  // Sort data (always call hooks)
  const sortedData = useMemo(() => {
    if (!filteredData || filteredData.length === 0 || !sortConfig.key) return filteredData;

    return [...filteredData].sort((a, b) => {
      let aValue = a[sortConfig.key];
      let bValue = b[sortConfig.key];

      // Handle different data types
      if (sortConfig.key === 'date') {
        aValue = new Date(aValue);
        bValue = new Date(bValue);
      } else if (sortConfig.key === 'score' || sortConfig.key === 'percentage') {
        aValue = parseFloat(aValue) || 0;
        bValue = parseFloat(bValue) || 0;
      } else {
        aValue = String(aValue || '').toLowerCase();
        bValue = String(bValue || '').toLowerCase();
      }

      if (aValue < bValue) {
        return sortConfig.direction === 'asc' ? -1 : 1;
      }
      if (aValue > bValue) {
        return sortConfig.direction === 'asc' ? 1 : -1;
      }
      return 0;
    });
  }, [filteredData, sortConfig]);

  // Calculate statistics (always call hooks)
  const stats = useMemo(() => {
    if (!sortedData || sortedData.length === 0) {
      return { total: 0, average: 0, highest: 0, lowest: 0 };
    }
    const scores = sortedData.map(item => item.score || item.percentage || 0);
    return {
      total: sortedData.length,
      average: scores.length > 0 ? Math.round(scores.reduce((sum, score) => sum + score, 0) / scores.length) : 0,
      highest: scores.length > 0 ? Math.max(...scores) : 0,
      lowest: scores.length > 0 ? Math.min(...scores) : 0
    };
  }, [sortedData]);

  // Loading state
  if (loading) {
    return (
      <div className={`score-table-container ${className}`}>
        <div className="table-loading">
          <div className="loading-spinner"></div>
          <p>Loading assessment data...</p>
        </div>
      </div>
    );
  }

  // Error state
  if (error) {
    return (
      <div className={`score-table-container ${className}`}>
        <div className="table-error">
          <div className="error-icon">⚠️</div>
          <p className="error-message">{error}</p>
        </div>
      </div>
    );
  }

  // Empty data state
  if (!data || data.length === 0) {
    return (
      <div className={`score-table-container ${className}`}>
        <div className="table-empty">
          <div className="empty-icon">📋</div>
          <p className="empty-message">No assessment records found</p>
          <p className="empty-subtitle">Assessment data will appear here once evaluations are completed</p>
        </div>
      </div>
    );
  }

  // Pagination
  const totalPages = Math.ceil(sortedData.length / pageSize);
  const startIndex = (currentPage - 1) * pageSize;
  const paginatedData = showPagination 
    ? sortedData.slice(startIndex, startIndex + pageSize)
    : sortedData;

  // Handle sorting
  const handleSort = (key) => {
    setSortConfig(prevConfig => ({
      key,
      direction: prevConfig.key === key && prevConfig.direction === 'asc' ? 'desc' : 'asc'
    }));
  };

  // Get sort icon
  const getSortIcon = (columnKey) => {
    if (sortConfig.key !== columnKey) return '↕️';
    return sortConfig.direction === 'asc' ? '↑' : '↓';
  };

  // Format date
  const formatDate = (dateString) => {
    if (!dateString) return 'N/A';
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric'
    });
  };

  // Get grade color class
  const getGradeClass = (score) => {
    if (score >= 90) return 'grade-excellent';
    if (score >= 80) return 'grade-good';
    if (score >= 70) return 'grade-average';
    if (score >= 60) return 'grade-below-average';
    return 'grade-poor';
  };

  // Stats are now calculated at the top with other hooks

  return (
    <div className={`score-table-container ${className}`}>
      {/* Table Controls */}
      <div className="table-controls">
        <div className="controls-left">
          <div className="search-box">
            <input
              type="text"
              placeholder="Search assessments..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="search-input"
            />
            <span className="search-icon">🔍</span>
          </div>
          
          <select
            value={filterSubject}
            onChange={(e) => setFilterSubject(e.target.value)}
            className="subject-filter"
          >
            <option value="">All Subjects</option>
            {subjects.map(subject => (
              <option key={subject} value={subject}>{subject}</option>
            ))}
          </select>
        </div>

        <div className="controls-right">
          <div className="table-stats">
            <span className="stat-item">Total: {stats.total}</span>
            <span className="stat-item">Avg: {stats.average}%</span>
            <span className="stat-item">Best: {stats.highest}%</span>
          </div>
        </div>
      </div>

      {/* Table */}
      <div className="table-wrapper">
        <table className="score-table">
          <thead>
            <tr>
              <th 
                className="sortable-header"
                onClick={() => handleSort('subject')}
              >
                Subject {getSortIcon('subject')}
              </th>
              <th 
                className="sortable-header"
                onClick={() => handleSort('assessmentName')}
              >
                Assessment Name {getSortIcon('assessmentName')}
              </th>
              <th 
                className="sortable-header"
                onClick={() => handleSort('date')}
              >
                Date {getSortIcon('date')}
              </th>
              <th 
                className="sortable-header score-column"
                onClick={() => handleSort('score')}
              >
                Score {getSortIcon('score')}
              </th>
              <th className="grade-column">Grade</th>
            </tr>
          </thead>
          <tbody>
            {paginatedData.map((record, index) => (
              <tr key={index} className="table-row">
                <td className="subject-cell">
                  <span className="subject-name">
                    {record.subject || record.subjectName || 'Unknown'}
                  </span>
                </td>
                <td className="assessment-cell">
                  <span className="assessment-name">
                    {record.assessmentName || record.assessment || 'N/A'}
                  </span>
                </td>
                <td className="date-cell">
                  {formatDate(record.date)}
                </td>
                <td className="score-cell">
                  <span className={`score-value ${getGradeClass(record.score || record.percentage || 0)}`}>
                    {record.score || record.percentage || 0}%
                  </span>
                </td>
                <td className="grade-cell">
                  <span className={`grade-badge ${getGradeClass(record.score || record.percentage || 0)}`}>
                    {record.grade || calculateGrade(record.score || record.percentage || 0)}
                  </span>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {/* Pagination */}
      {showPagination && totalPages > 1 && (
        <div className="table-pagination">
          <div className="pagination-info">
            Showing {startIndex + 1}-{Math.min(startIndex + pageSize, sortedData.length)} of {sortedData.length} records
          </div>
          
          <div className="pagination-controls">
            <button
              className="pagination-btn"
              onClick={() => setCurrentPage(prev => Math.max(1, prev - 1))}
              disabled={currentPage === 1}
            >
              Previous
            </button>
            
            <div className="page-numbers">
              {Array.from({ length: Math.min(5, totalPages) }, (_, i) => {
                const pageNum = Math.max(1, Math.min(totalPages - 4, currentPage - 2)) + i;
                return (
                  <button
                    key={pageNum}
                    className={`page-btn ${currentPage === pageNum ? 'active' : ''}`}
                    onClick={() => setCurrentPage(pageNum)}
                  >
                    {pageNum}
                  </button>
                );
              })}
            </div>
            
            <button
              className="pagination-btn"
              onClick={() => setCurrentPage(prev => Math.min(totalPages, prev + 1))}
              disabled={currentPage === totalPages}
            >
              Next
            </button>
          </div>
        </div>
      )}
    </div>
  );
};

// Helper function to calculate grade from score
const calculateGrade = (score) => {
  if (score >= 97) return 'A+';
  if (score >= 93) return 'A';
  if (score >= 90) return 'A-';
  if (score >= 87) return 'B+';
  if (score >= 83) return 'B';
  if (score >= 80) return 'B-';
  if (score >= 77) return 'C+';
  if (score >= 73) return 'C';
  if (score >= 70) return 'C-';
  if (score >= 67) return 'D+';
  if (score >= 65) return 'D';
  return 'F';
};

// PropTypes for type checking
DetailedScoreTable.propTypes = {
  /** Array of performance records */
  data: PropTypes.arrayOf(
    PropTypes.shape({
      subject: PropTypes.string,
      subjectName: PropTypes.string,
      assessmentName: PropTypes.string,
      assessment: PropTypes.string,
      date: PropTypes.string,
      score: PropTypes.number,
      percentage: PropTypes.number,
      grade: PropTypes.string
    })
  ),
  
  /** Loading state */
  loading: PropTypes.bool,
  
  /** Error message to display */
  error: PropTypes.string,
  
  /** Number of records per page */
  pageSize: PropTypes.number,
  
  /** Whether to show pagination */
  showPagination: PropTypes.bool,
  
  /** Additional CSS classes */
  className: PropTypes.string
};

export default DetailedScoreTable;