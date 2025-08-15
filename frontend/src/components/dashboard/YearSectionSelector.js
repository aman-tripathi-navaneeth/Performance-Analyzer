import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import './YearSectionSelector.css';

/**
 * YearSectionSelector Component - Allows selection of year and section
 * Shows available year/section combinations and navigates to class performance
 */
const YearSectionSelector = ({ data }) => {
  const navigate = useNavigate();
  const [availableClasses, setAvailableClasses] = useState([]);

  useEffect(() => {
    if (data?.year_section_distribution) {
      // Extract available year/section combinations from the data
      const classes = [];
      
      Object.entries(data.year_section_distribution).forEach(([yearKey, sections]) => {
        Object.entries(sections).forEach(([section, studentCount]) => {
          if (studentCount > 0) {
            // Extract year number from yearKey (e.g., "2nd Year" -> 2)
            const yearMatch = yearKey.match(/(\d+)/);
            const yearNumber = yearMatch ? parseInt(yearMatch[1]) : null;
            
            if (yearNumber) {
              classes.push({
                year: yearNumber,
                yearLabel: yearKey,
                section: section,
                studentCount: studentCount,
                classId: `${yearNumber}-${section}`
              });
            }
          }
        });
      });
      
      // Sort by year then section
      classes.sort((a, b) => {
        if (a.year !== b.year) return a.year - b.year;
        return a.section.localeCompare(b.section);
      });
      
      setAvailableClasses(classes);
    }
  }, [data]);

  const handleClassSelect = (year, section) => {
    // URL encode the section name to handle spaces and special characters
    const encodedSection = encodeURIComponent(section);
    navigate(`/class/${year}/${encodedSection}`);
  };

  const getClassIcon = (section) => {
    if (section.includes('CSE')) return '💻';
    if (section.includes('ECE')) return '⚡';
    if (section.includes('CSM')) return '🔬';
    if (section.includes('COS')) return '🌐';
    return '📚';
  };

  const getStudentCountColor = (count) => {
    if (count >= 30) return 'high';
    if (count >= 20) return 'medium';
    return 'low';
  };

  if (availableClasses.length === 0) {
    return (
      <div className="year-section-selector">
        <div className="selector-header">
          <h2>📊 Select Class for Performance Analysis</h2>
          <p>Choose a year and section to view detailed class performance</p>
        </div>
        
        <div className="no-classes">
          <div className="no-classes-icon">📚</div>
          <h3>No Classes Available</h3>
          <p>No performance data found. Please upload student data first.</p>
          <button 
            className="btn btn-primary"
            onClick={() => navigate('/upload')}
          >
            Upload Data
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="year-section-selector">
      <div className="selector-header">
        <h2>📊 Select Class for Performance Analysis</h2>
        <p>Choose a year and section to view detailed class performance and student insights</p>
      </div>

      <div className="classes-grid">
        {availableClasses.map((classInfo) => (
          <div 
            key={classInfo.classId}
            className="class-card"
            onClick={() => handleClassSelect(classInfo.year, classInfo.section)}
          >
            <div className="class-icon">
              {getClassIcon(classInfo.section)}
            </div>
            
            <div className="class-info">
              <h3 className="class-name">
                {classInfo.yearLabel} {classInfo.section}
              </h3>
              <div className="class-meta">
                <span className={`student-count ${getStudentCountColor(classInfo.studentCount)}`}>
                  👥 {classInfo.studentCount} students
                </span>
              </div>
            </div>
            
            <div className="class-arrow">
              →
            </div>
          </div>
        ))}
      </div>

      <div className="selector-footer">
        <div className="quick-actions">
          <button 
            className="btn btn-secondary"
            onClick={() => navigate('/students')}
          >
            📋 View All Students
          </button>
          <button 
            className="btn btn-secondary"
            onClick={() => navigate('/upload')}
          >
            📤 Upload New Data
          </button>
        </div>
      </div>
    </div>
  );
};

export default YearSectionSelector;