import { useState, useEffect, useCallback } from 'react';
import { useNavigate, useSearchParams } from 'react-router-dom';
import { searchStudents, getAllStudents } from '../api/apiService';
import useFetchSimple from '../hooks/useFetchSimple';
import Header from '../components/common/Header';
import StatCard from '../components/common/StatCard';
import './StudentsPage.css';

/**
 * StudentsPage Component - List and search students with performance data
 * Displays paginated student list with search and filtering capabilities
 */
const StudentsPage = () => {
  const navigate = useNavigate();
  const [searchParams] = useSearchParams();
  const searchQuery = searchParams.get('search') || '';
  
  // State for search and filters
  const [currentSearch, setCurrentSearch] = useState(searchQuery);
  const [yearFilter, setYearFilter] = useState(searchParams.get('year') || '');
  const [sectionFilter, setSectionFilter] = useState(searchParams.get('section') || '');
  const [sortBy, setSortBy] = useState('name');
  const [sortOrder, setSortOrder] = useState('asc');
  const [gradeFilter, setGradeFilter] = useState('');

  // Create fetch function based on search query and filters
  const fetchStudents = useCallback(() => {
    const params = new URLSearchParams();
    if (currentSearch) params.append('search', currentSearch);
    if (yearFilter) params.append('year', yearFilter);
    if (sectionFilter) params.append('section', sectionFilter);
    params.append('per_page', '50');
    
    const queryString = params.toString();
    const url = queryString ? `/students?${queryString}` : '/students?per_page=50';
    
    // Use the search API with filters
    return fetch(`${process.env.REACT_APP_API_URL || 'http://localhost:5000/api/v1'}${url}`)
      .then(response => response.json())
      .then(result => result.success ? result.data : { students: [] });
  }, [currentSearch, yearFilter, sectionFilter]);

  // Use simplified fetch hook
  const { data: studentsData, loading, error, refresh } = useFetchSimple(fetchStudents, [currentSearch, yearFilter, sectionFilter]);
  
  const students = studentsData?.students || [];

  // Update search when URL params change
  useEffect(() => {
    setCurrentSearch(searchQuery);
  }, [searchQuery]);

  // Navigate to student profile (memoized)
  const navigateToStudent = useCallback((studentId) => {
    navigate(`/student/${studentId}`);
  }, [navigate]);

  // Handle search input change
  const handleSearchChange = (e) => {
    const value = e.target.value;
    setCurrentSearch(value);
    
    // Update URL without navigation
    const newParams = new URLSearchParams(searchParams);
    if (value) {
      newParams.set('search', value);
    } else {
      newParams.delete('search');
    }
    window.history.replaceState({}, '', `${window.location.pathname}?${newParams}`);
  };

  // Clear search
  const clearSearch = () => {
    setCurrentSearch('');
    const newParams = new URLSearchParams(searchParams);
    newParams.delete('search');
    window.history.replaceState({}, '', window.location.pathname);
  };

  // Get grade color class
  const getGradeClass = (grade) => {
    if (!grade) return 'grade-default';
    const gradeUpper = grade.toUpperCase();
    if (gradeUpper.includes('A')) return 'grade-a';
    if (gradeUpper.includes('B')) return 'grade-b';
    if (gradeUpper.includes('C')) return 'grade-c';
    if (gradeUpper.includes('D')) return 'grade-d';
    if (gradeUpper.includes('F')) return 'grade-f';
    return 'grade-default';
  };

  // Calculate summary stats
  const summaryStats = {
    total: students.length,
    averageScore: students.length > 0 
      ? Math.round(students.reduce((sum, student) => 
          sum + (student.performance_summary?.average_percentage || 0), 0) / students.length)
      : 0,
    topPerformers: students.filter(s => (s.performance_summary?.average_percentage || 0) >= 85).length,
    needsAttention: students.filter(s => (s.performance_summary?.average_percentage || 0) < 60).length
  };

  return (
    <div className="students-page">
      <Header />
      
      <div className="students-container">
        {/* Page Header */}
        <div className="students-header">
          <div className="header-content">
            <h1 className="students-title">Students Overview</h1>
            <p className="students-subtitle">
              {currentSearch 
                ? `Search results for "${currentSearch}"`
                : 'Complete list of all students with performance data'
              }
            </p>
          </div>
        </div>

        {/* Summary Statistics */}
        {students.length > 0 && (
          <div className="stats-grid">
            <StatCard
              title="Total Students"
              value={summaryStats.total}
              subtitle="In current view"
              icon="👥"
              color="primary"
            />
            
            <StatCard
              title="Average Score"
              value={`${summaryStats.averageScore}%`}
              subtitle="Class average"
              icon="📊"
              color="info"
            />
            
            <StatCard
              title="Top Performers"
              value={summaryStats.topPerformers}
              subtitle="85% and above"
              icon="🏆"
              color="success"
            />
            
            <StatCard
              title="Needs Attention"
              value={summaryStats.needsAttention}
              subtitle="Below 60%"
              icon="📊"
              color="warning"
            />
          </div>
        )}

        {/* Search and Filters */}
        <div className="students-controls">
          <div className="search-section">
            <div className="search-input-wrapper">
              <input
                type="text"
                className="search-input"
                placeholder="Search students by name or ID..."
                value={currentSearch}
                onChange={handleSearchChange}
              />
              {currentSearch && (
                <button
                  className="clear-search-btn"
                  onClick={clearSearch}
                  aria-label="Clear search"
                >
                  ✕
                </button>
              )}
            </div>
          </div>

          <div className="filters-section">
            <select
              className="filter-select"
              value={yearFilter}
              onChange={(e) => setYearFilter(e.target.value)}
            >
              <option value="">All Years</option>
              <option value="1">1st Year</option>
              <option value="2">2nd Year</option>
              <option value="3">3rd Year</option>
              <option value="4">4th Year</option>
            </select>

            <select
              className="filter-select"
              value={sectionFilter}
              onChange={(e) => setSectionFilter(e.target.value)}
            >
              <option value="">All Sections</option>
              <option value="CSEA">CSE A</option>
              <option value="CSEB">CSE B</option>
              <option value="CSM">CSM</option>
              <option value="ECE">ECE</option>
              <option value="COS">COS</option>
            </select>

            <select
              className="filter-select"
              value={gradeFilter}
              onChange={(e) => setGradeFilter(e.target.value)}
            >
              <option value="">All Grades</option>
              <option value="A">A Grade</option>
              <option value="B">B Grade</option>
              <option value="C">C Grade</option>
              <option value="D">D Grade</option>
              <option value="F">F Grade</option>
            </select>

            <select
              className="sort-select"
              value={`${sortBy}-${sortOrder}`}
              onChange={(e) => {
                const [field, order] = e.target.value.split('-');
                setSortBy(field);
                setSortOrder(order);
              }}
            >
              <option value="name-asc">Name (A-Z)</option>
              <option value="name-desc">Name (Z-A)</option>
              <option value="score-desc">Score (High-Low)</option>
              <option value="score-asc">Score (Low-High)</option>
            </select>
          </div>
        </div>

        {/* Students List */}
        <div className="students-content">
          {loading && students.length === 0 ? (
            <div className="students-loading">
              <div className="loading-spinner"></div>
              <p>Loading students...</p>
            </div>
          ) : error ? (
            <div className="students-error">

              <h3>Unable to Load Students</h3>
              <p>{error}</p>
              <button className="btn btn-primary" onClick={refresh}>
                Try Again
              </button>
            </div>
          ) : students.length === 0 ? (
            <div className="students-empty">
              <div className="empty-icon">👥</div>
              <h3>No Students Found</h3>
              <p>
                {currentSearch 
                  ? `No students match your search for "${currentSearch}"`
                  : 'No students have been added yet. Upload student data to get started.'
                }
              </p>
              {!currentSearch && (
                <button 
                  className="btn btn-primary"
                  onClick={() => navigate('/upload')}
                >
                  Upload Student Data
                </button>
              )}
            </div>
          ) : (
            <>
              <div className="students-grid">
                {students.map((student) => (
                  <div
                    key={student.id}
                    className="student-card"
                    onClick={() => navigateToStudent(student.id)}
                  >
                    <div className="student-avatar">
                      <span className="avatar-text">
                        {student.full_name?.charAt(0)?.toUpperCase() || 'S'}
                      </span>
                    </div>
                    
                    <div className="student-info">
                      <h3 className="student-name">{student.full_name}</h3>
                      <p className="student-id">{student.student_roll_number}</p>
                      
                      {/* Year and Section Info */}
                      {(student.year || student.section) && (
                        <div className="student-year-section">
                          {student.year && (
                            <span className={`year-badge year-${student.year}`}>
                              {student.year}{student.year === 1 ? 'st' : student.year === 2 ? 'nd' : student.year === 3 ? 'rd' : 'th'} Year
                            </span>
                          )}
                          {student.section && (
                            <span className={`section-badge section-${student.section.toLowerCase()}`}>
                              {student.section}
                            </span>
                          )}
                        </div>
                      )}
                      
                      {student.performance_summary && (
                        <div className="student-performance">
                          <div className="performance-score">
                            <span className="score-value">
                              {student.performance_summary.average_percentage}%
                            </span>
                            <span className={`grade-badge ${getGradeClass(student.performance_summary.grade)}`}>
                              {student.performance_summary.grade || 'N/A'}
                            </span>
                          </div>
                          
                          <div className="performance-details">
                            <span className="detail-item">
                              {student.performance_summary.subjects_count} subjects
                            </span>
                            <span className="detail-item">
                              {student.performance_summary.total_assessments} assessments
                            </span>
                          </div>
                        </div>
                      )}
                    </div>
                    
                    <div className="student-actions">
                      <span className="view-profile">View Profile →</span>
                    </div>
                  </div>
                ))}
              </div>

              {/* Showing all students at once for better performance */}
            </>
          )}
        </div>
      </div>
    </div>
  );
};

export default StudentsPage;