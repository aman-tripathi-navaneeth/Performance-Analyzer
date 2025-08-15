import React, { useState, useEffect } from 'react';
import Header from '../components/common/Header';
import './TeacherManagement.css';

/**
 * TeacherManagement Component - Admin interface for managing teachers
 * Allows admins to view, add, and manage teachers and sections
 */
const TeacherManagement = () => {
  const [teachers, setTeachers] = useState([]);
  const [sections, setSections] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [activeTab, setActiveTab] = useState('teachers');
  
  // Add teacher form state
  const [showAddTeacher, setShowAddTeacher] = useState(false);
  const [newTeacher, setNewTeacher] = useState({
    name: '',
    email: '',
    password: ''
  });
  const [addingTeacher, setAddingTeacher] = useState(false);
  
  // Add section form state
  const [showAddSection, setShowAddSection] = useState(false);
  const [newSection, setNewSection] = useState('');
  const [addingSection, setAddingSection] = useState(false);

  // Fetch teachers and sections on component mount
  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      setLoading(true);
      setError(null);
      
      // Get auth token
      const token = localStorage.getItem('authToken');
      if (!token) {
        setError('Authentication required');
        return;
      }

      const headers = {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      };

      // Fetch teachers and sections in parallel
      const [teachersResponse, sectionsResponse] = await Promise.all([
        fetch('http://localhost:5000/api/v1/admin/teachers', { headers }),
        fetch('http://localhost:5000/api/v1/admin/sections', { headers })
      ]);

      if (!teachersResponse.ok || !sectionsResponse.ok) {
        throw new Error('Failed to fetch data');
      }

      const teachersData = await teachersResponse.json();
      const sectionsData = await sectionsResponse.json();

      if (teachersData.success) {
        setTeachers(teachersData.data.teachers);
      }

      if (sectionsData.success) {
        setSections(sectionsData.data.sections);
      }

    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const handleAddTeacher = async (e) => {
    e.preventDefault();
    
    if (!newTeacher.name || !newTeacher.email || !newTeacher.password) {
      alert('Please fill in all fields');
      return;
    }

    try {
      setAddingTeacher(true);
      
      const token = localStorage.getItem('authToken');
      const response = await fetch('http://localhost:5000/api/v1/admin/teachers', {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(newTeacher)
      });

      const data = await response.json();

      if (data.success) {
        // Refresh teachers list
        await fetchData();
        
        // Reset form
        setNewTeacher({ name: '', email: '', password: '' });
        setShowAddTeacher(false);
        
        alert('Teacher added successfully!');
      } else {
        alert(data.error || 'Failed to add teacher');
      }

    } catch (err) {
      alert('Error adding teacher: ' + err.message);
    } finally {
      setAddingTeacher(false);
    }
  };

  const handleAddSection = async (e) => {
    e.preventDefault();
    
    if (!newSection.trim()) {
      alert('Please enter a section name');
      return;
    }

    try {
      setAddingSection(true);
      
      const token = localStorage.getItem('authToken');
      const response = await fetch('http://localhost:5000/api/v1/admin/sections', {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ name: newSection })
      });

      const data = await response.json();

      if (data.success) {
        // Refresh sections list
        await fetchData();
        
        // Reset form
        setNewSection('');
        setShowAddSection(false);
        
        alert('Section added successfully!');
      } else {
        alert(data.error || 'Failed to add section');
      }

    } catch (err) {
      alert('Error adding section: ' + err.message);
    } finally {
      setAddingSection(false);
    }
  };

  const formatDate = (dateString) => {
    if (!dateString) return 'Never';
    return new Date(dateString).toLocaleDateString();
  };

  if (loading) {
    return (
      <div className="teacher-management">
        <Header />
        <div className="container">
          <div className="loading">Loading teacher management...</div>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="teacher-management">
        <Header />
        <div className="container">
          <div className="error">Error: {error}</div>
        </div>
      </div>
    );
  }

  return (
    <div className="teacher-management">
      <Header />
      
      <div className="container">
        <div className="page-header">
          <h1>👨‍🏫 Teacher Management</h1>
          <p>Manage teachers and sections in your institution</p>
        </div>

        {/* Tab Navigation */}
        <div className="tab-navigation">
          <button 
            className={`tab-button ${activeTab === 'teachers' ? 'active' : ''}`}
            onClick={() => setActiveTab('teachers')}
          >
            👨‍🏫 Teachers ({teachers.length})
          </button>
          <button 
            className={`tab-button ${activeTab === 'sections' ? 'active' : ''}`}
            onClick={() => setActiveTab('sections')}
          >
            🏫 Sections ({sections.length})
          </button>
        </div>

        {/* Teachers Tab */}
        {activeTab === 'teachers' && (
          <div className="tab-content">
            <div className="section-header">
              <h2>Teachers</h2>
              <button 
                className="btn btn-primary"
                onClick={() => setShowAddTeacher(true)}
              >
                ➕ Add Teacher
              </button>
            </div>

            <div className="teachers-grid">
              {teachers.map(teacher => (
                <div key={teacher.id} className="teacher-card">
                  <div className="teacher-info">
                    <div className="teacher-avatar">
                      {teacher.name.charAt(0).toUpperCase()}
                    </div>
                    <div className="teacher-details">
                      <h3>{teacher.name}</h3>
                      <p className="email">{teacher.email}</p>
                      <div className="teacher-meta">
                        <span className={`status ${teacher.is_active ? 'active' : 'inactive'}`}>
                          {teacher.is_active ? '✅ Active' : '❌ Inactive'}
                        </span>
                        <span className="joined">
                          Joined: {formatDate(teacher.created_at)}
                        </span>
                        <span className="last-login">
                          Last Login: {formatDate(teacher.last_login)}
                        </span>
                      </div>
                    </div>
                  </div>
                  <div className="teacher-actions">
                    <button className="btn btn-secondary btn-sm">
                      ✏️ Edit
                    </button>
                    <button className="btn btn-warning btn-sm">
                      {teacher.is_active ? '🚫 Deactivate' : '✅ Activate'}
                    </button>
                  </div>
                </div>
              ))}
            </div>

            {teachers.length === 0 && (
              <div className="empty-state">
                <p>No teachers found. Add your first teacher!</p>
              </div>
            )}
          </div>
        )}

        {/* Sections Tab */}
        {activeTab === 'sections' && (
          <div className="tab-content">
            <div className="section-header">
              <h2>Sections</h2>
              <button 
                className="btn btn-primary"
                onClick={() => setShowAddSection(true)}
              >
                ➕ Add Section
              </button>
            </div>

            <div className="sections-grid">
              {sections.map(section => (
                <div key={section.id} className="section-card">
                  <div className="section-info">
                    <h3>{section.name}</h3>
                    <p>Created: {formatDate(section.created_at)}</p>
                  </div>
                  <div className="section-actions">
                    <button className="btn btn-secondary btn-sm">
                      ✏️ Edit
                    </button>
                    <button className="btn btn-danger btn-sm">
                      🗑️ Delete
                    </button>
                  </div>
                </div>
              ))}
            </div>

            {sections.length === 0 && (
              <div className="empty-state">
                <p>No sections found. Add your first section!</p>
              </div>
            )}
          </div>
        )}
      </div>

      {/* Add Teacher Modal */}
      {showAddTeacher && (
        <div className="modal-overlay">
          <div className="modal">
            <div className="modal-header">
              <h3>➕ Add New Teacher</h3>
              <button 
                className="close-btn"
                onClick={() => setShowAddTeacher(false)}
              >
                ✕
              </button>
            </div>
            
            <form onSubmit={handleAddTeacher} className="modal-form">
              <div className="form-group">
                <label>Teacher Name *</label>
                <input
                  type="text"
                  value={newTeacher.name}
                  onChange={(e) => setNewTeacher({...newTeacher, name: e.target.value})}
                  placeholder="Enter teacher's full name"
                  required
                />
              </div>
              
              <div className="form-group">
                <label>Email Address *</label>
                <input
                  type="email"
                  value={newTeacher.email}
                  onChange={(e) => setNewTeacher({...newTeacher, email: e.target.value})}
                  placeholder="Enter email address"
                  required
                />
              </div>
              
              <div className="form-group">
                <label>Password *</label>
                <input
                  type="password"
                  value={newTeacher.password}
                  onChange={(e) => setNewTeacher({...newTeacher, password: e.target.value})}
                  placeholder="Enter password (min 6 characters)"
                  minLength="6"
                  required
                />
              </div>
              
              <div className="modal-actions">
                <button 
                  type="button" 
                  className="btn btn-secondary"
                  onClick={() => setShowAddTeacher(false)}
                >
                  Cancel
                </button>
                <button 
                  type="submit" 
                  className="btn btn-primary"
                  disabled={addingTeacher}
                >
                  {addingTeacher ? 'Adding...' : 'Add Teacher'}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* Add Section Modal */}
      {showAddSection && (
        <div className="modal-overlay">
          <div className="modal">
            <div className="modal-header">
              <h3>➕ Add New Section</h3>
              <button 
                className="close-btn"
                onClick={() => setShowAddSection(false)}
              >
                ✕
              </button>
            </div>
            
            <form onSubmit={handleAddSection} className="modal-form">
              <div className="form-group">
                <label>Section Name *</label>
                <input
                  type="text"
                  value={newSection}
                  onChange={(e) => setNewSection(e.target.value)}
                  placeholder="Enter section name (e.g., CSE A, ECE B)"
                  required
                />
              </div>
              
              <div className="modal-actions">
                <button 
                  type="button" 
                  className="btn btn-secondary"
                  onClick={() => setShowAddSection(false)}
                >
                  Cancel
                </button>
                <button 
                  type="submit" 
                  className="btn btn-primary"
                  disabled={addingSection}
                >
                  {addingSection ? 'Adding...' : 'Add Section'}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};

export default TeacherManagement;