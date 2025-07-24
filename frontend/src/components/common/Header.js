import { useState, useEffect, useCallback } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import { searchStudents } from '../../api/apiService';
import { useAuth } from '../../contexts/AuthContext';
// Search functionality optimized with new hooks
import './Header.css';

/**
 * Header Component - Main navigation header for the Performance Analyzer
 * Features: App title, navigation menu, student search functionality
 */
const Header = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const { user, logout } = useAuth();
  
  // Simplified search state to fix performance issues
  const [searchQuery, setSearchQuery] = useState('');
  const [showSearchResults, setShowSearchResults] = useState(false);
  const [searchResults, setSearchResults] = useState([]);
  const [isSearching, setIsSearching] = useState(false);
  const [searchError, setSearchError] = useState('');

  // Navigation items
  const navigationItems = [
    { path: '/', label: 'Dashboard', icon: '📊' },
    { path: '/students', label: 'Students', icon: '👥' },
    { path: '/upload', label: 'Upload', icon: '📤' },
  ];

  // Search function with debouncing
  const search = useCallback(async (query) => {
    setSearchQuery(query);
    
    if (query.length < 2) {
      setSearchResults([]);
      setSearchError('');
      setShowSearchResults(false);
      return;
    }

    setIsSearching(true);
    setSearchError('');

    try {
      const results = await searchStudents(query, 1, 5); // Get top 5 results
      setSearchResults(results);
      setShowSearchResults(true);
    } catch (error) {
      setSearchError('Failed to search students');
      setSearchResults([]);
    } finally {
      setIsSearching(false);
    }
  }, []);

  // Clear search function
  const clearSearch = useCallback(() => {
    setSearchQuery('');
    setSearchResults([]);
    setSearchError('');
    setShowSearchResults(false);
  }, []);

  // Show search results when we have data and query is long enough
  useEffect(() => {
    if (searchQuery.length >= 2 && (searchResults?.data?.students || searchError)) {
      setShowSearchResults(true);
    } else {
      setShowSearchResults(false);
    }
  }, [searchQuery, searchResults, searchError]);

  // Handle search input change
  const handleSearchInputChange = useCallback((e) => {
    const value = e.target.value;
    search(value);
  }, [search]);

  // Handle student selection from search results
  const handleStudentSelect = useCallback((student) => {
    navigate(`/student/${student.id}`);
    clearSearch();
    setShowSearchResults(false);
  }, [navigate, clearSearch]);

  // Handle search form submission
  const handleSearchSubmit = useCallback((e) => {
    e.preventDefault();
    if (searchQuery.trim()) {
      navigate(`/students?search=${encodeURIComponent(searchQuery.trim())}`);
      setShowSearchResults(false);
    }
  }, [searchQuery, navigate]);

  // Close search results when clicking outside
  const handleSearchBlur = useCallback(() => {
    // Delay hiding to allow for click events on results
    setTimeout(() => {
      setShowSearchResults(false);
    }, 200);
  }, []);

  // Handle search input focus
  const handleSearchFocus = useCallback(() => {
    if (searchQuery.length >= 2 && (searchResults?.data?.students?.length > 0 || searchError)) {
      setShowSearchResults(true);
    }
  }, [searchQuery, searchResults, searchError]);

  // Handle keyboard navigation in search results
  const handleSearchKeyDown = useCallback((e) => {
    if (e.key === 'Escape') {
      setShowSearchResults(false);
    } else if (e.key === 'Enter' && !showSearchResults && searchQuery.trim()) {
      handleSearchSubmit(e);
    }
  }, [showSearchResults, searchQuery, handleSearchSubmit]);

  // Clear search results when navigating away
  useEffect(() => {
    setShowSearchResults(false);
  }, [location.pathname]);

  // Check if current path is active
  const isActivePath = (path) => {
    if (path === '/') {
      return location.pathname === '/';
    }
    return location.pathname.startsWith(path);
  };

  return (
    <header className="header">
      <div className="header-container">
        {/* Logo and Title */}
        <div className="header-brand">
          <button 
            className="brand-button"
            onClick={() => navigate('/')}
            aria-label="Go to dashboard"
          >
            <img 
              src="/images/College Logo.jpeg" 
              alt="Ideal Institute Logo" 
              className="brand-logo"
              onError={(e) => {
                e.target.style.display = 'none';
                e.target.nextElementSibling.style.display = 'inline';
              }}
            />
            <span className="brand-icon" style={{ display: 'none' }}>📈</span>
            <h1 className="brand-title">Performance Analyzer</h1>
          </button>
        </div>

        {/* Navigation Menu */}
        <nav className="header-nav" role="navigation" aria-label="Main navigation">
          <ul className="nav-list">
            {navigationItems.map((item) => (
              <li key={item.path} className="nav-item">
                <button
                  className={`nav-link ${isActivePath(item.path) ? 'nav-link-active' : ''}`}
                  onClick={() => navigate(item.path)}
                  aria-current={isActivePath(item.path) ? 'page' : undefined}
                >
                  <span className="nav-icon" aria-hidden="true">{item.icon}</span>
                  <span className="nav-label">{item.label}</span>
                </button>
              </li>
            ))}
          </ul>
        </nav>

        {/* Search Section */}
        <div className="header-search">
          <form onSubmit={handleSearchSubmit} className="search-form">
            <div className="search-input-container">
              <input
                type="text"
                className="search-input"
                placeholder="Search students by name or ID..."
                value={searchQuery}
                onChange={handleSearchInputChange}
                onFocus={handleSearchFocus}
                onBlur={handleSearchBlur}
                onKeyDown={handleSearchKeyDown}
                aria-label="Search students"
                aria-expanded={showSearchResults}
                aria-haspopup="listbox"
                autoComplete="off"
              />
              
              {/* Search Icon / Clear Button */}
              <div className="search-icon" aria-hidden="true">
                {isSearching ? (
                  <div className="loading-spinner-small"></div>
                ) : searchQuery ? (
                  <button
                    type="button"
                    className="search-clear-btn"
                    onClick={() => {
                      clearSearch();
                      setShowSearchResults(false);
                    }}
                    aria-label="Clear search"
                  >
                    ✕
                  </button>
                ) : (
                  <span>🔍</span>
                )}
              </div>

              {/* Search Results Dropdown */}
              {showSearchResults && (
                <div className="search-results" role="listbox" aria-label="Search results">
                  {searchError ? (
                    <div className="search-error" role="alert">
                      {searchError}
                    </div>
                  ) : searchResults?.data?.students?.length > 0 ? (
                    <>
                      {searchResults.data.students.map((student) => (
                        <button
                          key={student.id}
                          className="search-result-item"
                          onClick={() => handleStudentSelect(student)}
                          role="option"
                          aria-selected="false"
                        >
                          <div className="student-info">
                            <div className="student-name">{student.full_name}</div>
                            <div className="student-details">
                              {student.student_roll_number} • 
                              {student.performance_summary?.average_percentage 
                                ? ` ${student.performance_summary.average_percentage}% avg`
                                : ' No data'
                              }
                            </div>
                          </div>
                          <div className="student-grade">
                            {student.performance_summary?.grade || 'N/A'}
                          </div>
                        </button>
                      ))}
                      
                      {/* View All Results Link */}
                      <button
                        className="search-view-all"
                        onClick={() => {
                          navigate(`/students?search=${encodeURIComponent(searchQuery)}`);
                          setShowSearchResults(false);
                        }}
                      >
                        View all results for "{searchQuery}"
                      </button>
                    </>
                  ) : searchQuery.length >= 2 && !isSearching ? (
                    <div className="search-no-results">
                      No students found for "{searchQuery}"
                    </div>
                  ) : null}
                </div>
              )}
            </div>
          </form>
        </div>

        {/* User Actions */}
        <div className="header-actions">
          <div className="user-info">
            <span className="user-email">
              {user?.email || 'User'}
            </span>
          </div>
          <button
            className="logout-button"
            onClick={() => {
              logout();
              navigate('/login');
            }}
            title="Logout"
          >
            <span className="logout-icon">🚪</span>
            <span className="logout-text">Logout</span>
          </button>
        </div>
      </div>
    </header>
  );
};

export default Header;