import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { uploadFile } from '../api/apiService';
import Header from '../components/common/Header';
import FileUpload from '../components/common/FileUpload';
import './UploadPage.css';

/**
 * UploadPage Component - File upload interface for student performance data
 * Handles file selection, metadata input, and upload process with progress tracking
 */
const UploadPage = () => {
  const navigate = useNavigate();
  
  // Component state
  const [selectedFile, setSelectedFile] = useState(null);
  const [uploading, setUploading] = useState(false);
  const [uploadProgress, setUploadProgress] = useState(0);
  const [uploadResult, setUploadResult] = useState(null);
  const [error, setError] = useState('');
  
  // Form data state
  const [formData, setFormData] = useState({
    year: '',
    section: '',
    subjectName: '',
    assessmentType: ''
  });

  // Handle file selection from FileUpload component
  const handleFileSelect = (file) => {
    setSelectedFile(file);
    setError('');
    setUploadResult(null);
  };

  // Handle form input changes
  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  // Validate form data
  const validateForm = () => {
    if (!selectedFile) {
      return 'Please select a file to upload';
    }
    
    if (!formData.year) {
      return 'Year is required';
    }
    
    if (!formData.section) {
      return 'Section is required';
    }
    
    if (!formData.subjectName.trim()) {
      return 'Subject name is required';
    }
    
    return null;
  };

  // Handle file upload
  const handleUpload = async () => {
    // Validate form
    const validationError = validateForm();
    if (validationError) {
      setError(validationError);
      return;
    }

    try {
      setUploading(true);
      setError('');
      setUploadProgress(0);

      // Prepare upload data
      const uploadData = {
        file: selectedFile,
        year: formData.year,
        section: formData.section,
        subjectName: formData.subjectName.trim(),
        assessmentType: formData.assessmentType || 'General Assessment'
      };

      // Upload file with progress tracking
      const result = await uploadFile(uploadData, (progress) => {
        setUploadProgress(progress);
      });

      if (result.success) {
        setUploadResult(result);
        // Reset form after successful upload
        setSelectedFile(null);
        setFormData({
          year: '',
          section: '',
          subjectName: '',
          assessmentType: ''
        });
      } else {
        throw new Error(result.error || 'Upload failed');
      }
    } catch (err) {
      console.error('Upload error:', err);
      setError(err.message || 'Failed to upload file. Please try again.');
    } finally {
      setUploading(false);
      setUploadProgress(0);
    }
  };

  // Navigate to dashboard
  const goToDashboard = () => {
    navigate('/');
  };

  // Navigate to students page
  const goToStudents = () => {
    navigate('/students');
  };

  // Reset upload state
  const resetUpload = () => {
    setUploadResult(null);
    setError('');
  };

  return (
    <div className="upload-page">
      <Header />
      
      <div className="upload-container">
        {/* Page Header */}
        <div className="upload-header">
          <h1 className="upload-title">Upload Student Performance Data</h1>
          <p className="upload-subtitle">
            Upload Excel or CSV files containing student assessment data to analyze performance
          </p>
        </div>

        {/* Upload Success Message */}
        {uploadResult && (
          <div className="upload-success">
            <div className="success-icon">✅</div>
            <div className="success-content">
              <h3 className="success-title">Upload Successful!</h3>
              <p className="success-message">
                Your file has been processed successfully. 
                {uploadResult.data?.processed_records && (
                  <span> {uploadResult.data.processed_records} records were imported.</span>
                )}
              </p>
              <div className="success-actions">
                <button 
                  className="btn btn-primary"
                  onClick={goToDashboard}
                >
                  View Dashboard
                </button>
                <button 
                  className="btn btn-secondary"
                  onClick={goToStudents}
                >
                  View Students
                </button>
                <button 
                  className="btn btn-outline"
                  onClick={resetUpload}
                >
                  Upload Another File
                </button>
              </div>
            </div>
          </div>
        )}

        {/* Upload Form */}
        {!uploadResult && (
          <div className="upload-form">
            {/* File Upload Section */}
            <div className="form-section">
              <h2 className="section-title">📁 Select File</h2>
              <FileUpload
                onFileSelect={handleFileSelect}
                acceptedTypes=".xlsx,.xls,.csv"
                maxSize={10 * 1024 * 1024} // 10MB
                disabled={uploading}
              />
            </div>

            {/* Class Information Form */}
            {selectedFile && (
              <div className="form-section">
                <h2 className="section-title">🎓 Class Information</h2>
                <div className="form-grid">
                  <div className="form-group">
                    <label htmlFor="year" className="form-label required">
                      Year
                    </label>
                    <select
                      id="year"
                      name="year"
                      value={formData.year}
                      onChange={handleInputChange}
                      className="form-input"
                      disabled={uploading}
                      required
                    >
                      <option value="">Select Year</option>
                      <option value="1">1st Year</option>
                      <option value="2">2nd Year</option>
                      <option value="3">3rd Year</option>
                      <option value="4">4th Year</option>
                    </select>
                  </div>

                  <div className="form-group">
                    <label htmlFor="section" className="form-label required">
                      Section
                    </label>
                    <select
                      id="section"
                      name="section"
                      value={formData.section}
                      onChange={handleInputChange}
                      className="form-input"
                      disabled={uploading}
                      required
                    >
                      <option value="">Select Section</option>
                      <option value="CSEA">CSE A</option>
                      <option value="CSEB">CSE B</option>
                      <option value="CSM">CSM</option>
                      <option value="ECE">ECE</option>
                      <option value="COS">COS</option>
                    </select>
                  </div>

                  <div className="form-group">
                    <label htmlFor="subjectName" className="form-label required">
                      Subject Name
                    </label>
                    <input
                      type="text"
                      id="subjectName"
                      name="subjectName"
                      value={formData.subjectName}
                      onChange={handleInputChange}
                      className="form-input"
                      placeholder="e.g., Data Structures, Mathematics, Physics"
                      disabled={uploading}
                      required
                    />
                  </div>

                  <div className="form-group">
                    <label htmlFor="assessmentType" className="form-label">
                      Assessment Type (Optional)
                    </label>
                    <select
                      id="assessmentType"
                      name="assessmentType"
                      value={formData.assessmentType}
                      onChange={handleInputChange}
                      className="form-input"
                      disabled={uploading}
                    >
                      <option value="">Select Type</option>
                      <option value="Mid-term Exam">Mid-term Exam</option>
                      <option value="Final Exam">Final Exam</option>
                      <option value="Internal Assessment">Internal Assessment</option>
                      <option value="Quiz">Quiz</option>
                      <option value="Assignment">Assignment</option>
                      <option value="Lab Test">Lab Test</option>
                      <option value="Project">Project</option>
                    </select>
                  </div>
                </div>
              </div>
            )}

            {/* Upload Button and Progress */}
            {selectedFile && (
              <div className="upload-actions">
                {uploading ? (
                  <div className="upload-progress">
                    <div className="progress-info">
                      <span className="progress-text">Uploading... {uploadProgress}%</span>
                      <span className="progress-file">{selectedFile.name}</span>
                    </div>
                    <div className="progress-bar">
                      <div 
                        className="progress-fill"
                        style={{ width: `${uploadProgress}%` }}
                      ></div>
                    </div>
                  </div>
                ) : (
                  <button
                    className="btn btn-primary btn-large upload-submit-btn"
                    onClick={handleUpload}
                    disabled={!selectedFile}
                  >
                    <span>📤</span>
                    Upload and Process File
                  </button>
                )}
              </div>
            )}

            {/* Error Message */}
            {error && (
              <div className="upload-error">
                <div className="error-icon">⚠️</div>
                <div className="error-content">
                  <h4 className="error-title">Upload Failed</h4>
                  <p className="error-message">{error}</p>
                </div>
              </div>
            )}
          </div>
        )}

        {/* Upload Instructions */}
        <div className="upload-instructions">
          <h3 className="instructions-title">📋 File Format Guidelines</h3>
          <div className="instructions-content">
            <div className="instruction-section">
              <h4 className="instruction-heading">Required Columns:</h4>
              <ul className="instruction-list">
                <li><strong>Student Name</strong> - Full name of the student</li>
                <li><strong>Student ID/Roll Number</strong> - Unique identifier (e.g., 21A91A0501)</li>
                <li><strong>Score/Marks</strong> - Assessment score or percentage</li>
              </ul>
            </div>
            
            <div className="instruction-section">
              <h4 className="instruction-heading">Optional Columns:</h4>
              <ul className="instruction-list">
                <li><strong>Email</strong> - Student email address</li>
                <li><strong>Phone</strong> - Contact number</li>
                <li><strong>Remarks</strong> - Additional notes or comments</li>
                <li><strong>Grade</strong> - Letter grade (A, B, C, etc.)</li>
              </ul>
            </div>
            
            <div className="instruction-section">
              <h4 className="instruction-heading">College Structure:</h4>
              <ul className="instruction-list">
                <li><strong>Years:</strong> 1st, 2nd, 3rd, 4th Year</li>
                <li><strong>Sections:</strong> CSE A, CSE B, CSM, ECE, COS</li>
                <li><strong>Workflow:</strong> Select year and section first, then upload subject data</li>
                <li><strong>Multiple Files:</strong> Teachers can upload multiple files for the same year-section</li>
                <li><strong>Organization:</strong> Each file represents one subject for one year-section combination</li>
              </ul>
            </div>
            
            <div className="instruction-section">
              <h4 className="instruction-heading">Upload Example:</h4>
              <ul className="instruction-list">
                <li><strong>Scenario:</strong> Math teacher for 2nd Year CSE A students</li>
                <li><strong>Step 1:</strong> Select "2nd Year" and "CSE A"</li>
                <li><strong>Step 2:</strong> Enter "Mathematics" as subject name</li>
                <li><strong>Step 3:</strong> Choose "Mid-term Exam" as assessment type</li>
                <li><strong>Step 4:</strong> Upload Excel file with student scores</li>
                <li><strong>Result:</strong> Data organized as "Mathematics - Year 2 CSEA"</li>
              </ul>
            </div>
            
            <div className="instruction-section">
              <h4 className="instruction-heading">Tips for Best Results:</h4>
              <ul className="instruction-list">
                <li>Ensure the first row contains column headers</li>
                <li>Remove any empty rows or columns</li>
                <li>Use consistent data formats (e.g., all scores as numbers)</li>
                <li>Save Excel files in .xlsx format for better compatibility</li>
                <li>One file per subject per year-section combination</li>
              </ul>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default UploadPage;