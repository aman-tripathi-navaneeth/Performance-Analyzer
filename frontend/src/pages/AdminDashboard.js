import { useState, useEffect } from 'react';
import { useAuth } from '../contexts/AuthContext';
import Header from '../components/common/Header';
import './AdminDashboard.css';

/**
 * AdminDashboard Component - Administrative interface for managing teachers and sections
 * Only accessible by users with admin role
 */
const AdminDashboard = () => {
  const { user } = useAuth();
  
  // State for teachers management
  const [teachers, setTeachers] = useState([
    { id: 1, name: 'Dr. John Smith', email: 'john.smith@college.edu', role: 'teacher', sections: ['CSE A', 'CSE B'] },
    { id: 2, name: 'Prof. Sarah Johnson', email: 'sarah.johnson@college.edu', role: 'teacher', sections: ['ECE'] },
    { id: 3, name: 'Dr. Mike Wilson', email: 'mike.wilson@college.edu', role: 'admin', sections: [] },
  ]);
  
  // State for sections management
  const [sections, setSections] = useState(['CSE A', 'CSE B', 'CSM', 'ECE', 'COS']);
  
  // State for forms
  const [showAddTeacher, setShowAddTeacher] = useState(false);
  const [showAddSection, setShowAddSection] = useState(false);
  const [newTeacher, setNewTeacher] = useState({ name: '', email: '', role: 'teacher' });
  const [newSection, setNewSection] = useState('');
  
  // State for loading and messages
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState('');

  // Handle add teacher
  const handleAddTeacher = async (e) => {
    e.preventDefault();
    if (!newTeacher.name.trim() || !newTeacher.email.trim()) {
      setMessage('Please fill in all required fields');
      return;
    }

    setLoading(true);
    try {
      // Simulate API call
      await new Promise(resolve => setTimeout(resolve, 1000));
      
      const teacher = {
        id: Date.now(),
        name: newTeacher.name.trim(),
        email: newTeacher.email.trim(),
        role: newTeacher.role,
        sections: []
      };
      
      setTeachers(prev => [...prev, teacher]);
      setNewTeacher({ name: '', email: '', role: 'teacher' });
      setShowAddTeacher(false);
      setMessage(`Teacher ${teacher.name} added successfully!`);
      
      setTimeout(() => setMessage(''), 3000);
    } catch (error) {
      setMessage('Failed to add teacher. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  // Handle add section
  const handleAddSection = async (e) => {
    e.preventDefault();
    if (!newSection.trim()) {
      setMessage('Please enter a section name');
      return;
    }

    if (sections.includes(newSection.trim())) {
      setMessage('Section already exists');
      return;
    }

    setLoading(true);
    try {
      // Simulate API call
      await new Promise(resolve => setTimeout(resolve, 500));
      
      setSections(prev => [...prev, newSection.trim()]);
      setNewSection('');
      setShowAddSection(false);
      setMessage(`Section ${newSection.trim()} added successfully!`);
      
      setTimeout(() => setMessage(''), 3000);
    } catch (error) {
      setMessage('Failed to add section. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  // Handle promote teacher to admin
  const handlePromoteTeacher = async (teacherId) => {
    setLoading(true);
    try {
      // Simulate API call
      await new Promise(resolve => setTimeout(resolve, 1000));
      
      setTeachers(prev => prev.map(teacher => 
        teacher.id === teacherId 
          ? { ...teacher, role: teacher.role === 'admin' ? 'teacher' : 'admin' }
          : teacher
      ));
      
      const teacher = teachers.find(t => t.id === teacherId);
      const newRole = teacher.role === 'admin' ? 'teacher' : 'admin';
      setMessage(`${teacher.name} ${newRole === 'admin' ? 'promoted to' : 'demoted from'} administrator!`);
      
      setTimeout(() => setMessage(''), 3000);
    } catch (error) {
      setMessage('Failed to update teacher role. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  // Handle remove teacher
  const handleRemoveTeacher = async (teacherId) => {
    if (!window.confirm('Are you sure you want to remove this teacher?')) {
      return;
    }

    setLoading(true);
    try {
      // Simulate API call
      await new Promise(resolve => setTimeout(resolve, 1000));
      
      const teacher = teachers.find(t => t.id === teacherId);
      setTeachers(prev => prev.filter(teacher => teacher.id !== teacherId));
      setMessage(`Teacher ${teacher.name} removed successfully!`);
      
      setTimeout(() => setMessage(''), 3000);
    } catch (error) {
      setMessage('Failed to remove teacher. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  // Handle remove section
  const handleRemoveSection = async (sectionName) => {
    if (!window.confirm(`Are you sure you want to remove section ${sectionName}?`)) {
      return;
    }

    setLoading(true);
    try {
      // Simulate API call
      await new Promise(resolve => setTimeout(resolve, 500));
      
      setSections(prev => prev.filter(section => section !== sectionName));
      setMessage(`Section ${sectionName} removed successfully!`);
      
      setTimeout(() => setMessage(''), 3000);
    } catch (error) {
      setMessage('Failed to remove section. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="admin-dashboard">
      <Header />
      
      <div className="admin-container">
        {/* Page Header */}
        <div className="admin-header">
          <h1 className="admin-title">Administrator Dashboard</h1>
          <p className="admin-subtitle">Manage teachers, sections, and system settings</p>
        </div>

        {/* Message Display */}
        {message && (
          <div className="admin-message">
            <span className="message-icon">ℹ️</span>
            {message}
          </div>
        )}

        {/* Quick Stats */}
        <div className="admin-stats">
          <div className="stat-card">
            <div className="stat-icon">👨‍🏫</div>
            <div className="stat-info">
              <div className="stat-number">{teachers.filter(t => t.role === 'teacher').length}</div>
              <div className="stat-label">Teachers</div>
            </div>
          </div>
          <div className="stat-card">
            <div className="stat-icon">👨‍💼</div>
            <div className="stat-info">
              <div className="stat-number">{teachers.filter(t => t.role === 'admin').length}</div>
              <div className="stat-label">Administrators</div>
            </div>
          </div>
          <div className="stat-card">
            <div className="stat-icon">🏫</div>
            <div className="stat-info">
              <div className="stat-number">{sections.length}</div>
              <div className="stat-label">Sections</div>
            </div>
          </div>
        </div>

        {/* Main Content */}
        <div className="admin-content">
          {/* Teachers Management */}
          <div className="admin-section">
            <div className="section-header">
              <h2 className="section-title">Teachers Management</h2>
              <button 
                className="btn btn-primary"
                onClick={() => setShowAddTeacher(true)}
                disabled={loading}
              >
                <span>➕</span>
                Add Teacher
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
                      <h3 className="teacher-name">{teacher.name}</h3>
                      <p className="teacher-email">{teacher.email}</p>
                      <span className={`role-badge role-${teacher.role}`}>
                        {teacher.role === 'admin' ? '👨‍💼 Administrator' : '👨‍🏫 Teacher'}
                      </span>
                    </div>
                  </div>
                  
                  <div className="teacher-actions">
                    <button
                      className={`btn btn-sm ${teacher.role === 'admin' ? 'btn-warning' : 'btn-success'}`}
                      onClick={() => handlePromoteTeacher(teacher.id)}
                      disabled={loading}
                    >
                      {teacher.role === 'admin' ? 'Demote' : 'Promote'}
                    </button>
                    <button
                      className="btn btn-sm btn-danger"
                      onClick={() => handleRemoveTeacher(teacher.id)}
                      disabled={loading}
                    >
                      Remove
                    </button>
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Sections Management */}
          <div className="admin-section">
            <div className="section-header">
              <h2 className="section-title">Sections Management</h2>
              <button 
                className="btn btn-primary"
                onClick={() => setShowAddSection(true)}
                disabled={loading}
              >
                <span>➕</span>
                Add Section
              </button>
            </div>

            <div className="sections-grid">
              {sections.map(section => (
                <div key={section} className="section-card">
                  <div className="section-info">
                    <div className="section-icon">🏫</div>
                    <div className="section-name">{section}</div>
                  </div>
                  <button
                    className="btn btn-sm btn-danger"
                    onClick={() => handleRemoveSection(section)}
                    disabled={loading}
                  >
                    Remove
                  </button>
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* Add Teacher Modal */}
        {showAddTeacher && (
          <div className="modal-overlay">
            <div className="modal">
              <div className="modal-header">
                <h3>Add New Teacher</h3>
                <button 
                  className="modal-close"
                  onClick={() => setShowAddTeacher(false)}
                >
                  ✕
                </button>
              </div>
              
              <form onSubmit={handleAddTeacher} className="modal-form">
                <div className="form-group">
                  <label className="form-label">Teacher Name</label>
                  <input
                    type="text"
                    className="form-input"
                    placeholder="Enter teacher's full name"
                    value={newTeacher.name}
                    onChange={(e) => setNewTeacher(prev => ({ ...prev, name: e.target.value }))}
                    required
                  />
                </div>
                
                <div className="form-group">
                  <label className="form-label">Email Address</label>
                  <input
                    type="email"
                    className="form-input"
                    placeholder="teacher@college.edu"
                    value={newTeacher.email}
                    onChange={(e) => setNewTeacher(prev => ({ ...prev, email: e.target.value }))}
                    required
                  />
                </div>
                
                <div className="form-group">
                  <label className="form-label">Role</label>
                  <select
                    className="form-input"
                    value={newTeacher.role}
                    onChange={(e) => setNewTeacher(prev => ({ ...prev, role: e.target.value }))}
                  >
                    <option value="teacher">Teacher</option>
                    <option value="admin">Administrator</option>
                  </select>
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
                    disabled={loading}
                  >
                    {loading ? 'Adding...' : 'Add Teacher'}
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
                <h3>Add New Section</h3>
                <button 
                  className="modal-close"
                  onClick={() => setShowAddSection(false)}
                >
                  ✕
                </button>
              </div>
              
              <form onSubmit={handleAddSection} className="modal-form">
                <div className="form-group">
                  <label className="form-label">Section Name</label>
                  <input
                    type="text"
                    className="form-input"
                    placeholder="e.g., CSE C, IT A, MECH B"
                    value={newSection}
                    onChange={(e) => setNewSection(e.target.value)}
                    required
                  />
                  <p className="input-hint">Enter the section name (e.g., CSE A, ECE, IT B)</p>
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
                    disabled={loading}
                  >
                    {loading ? 'Adding...' : 'Add Section'}
                  </button>
                </div>
              </form>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default AdminDashboard;