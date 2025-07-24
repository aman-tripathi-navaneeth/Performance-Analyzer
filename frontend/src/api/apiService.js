import axios from 'axios';

// Base API configuration
const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000/api/v1';

// Create axios instance with default configuration
const apiClient = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000, // 30 seconds timeout for file uploads
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor for adding auth tokens (if needed in future)
apiClient.interceptors.request.use(
  (config) => {
    // Add auth token if available
    const token = localStorage.getItem('authToken');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor for handling common errors
apiClient.interceptors.response.use(
  (response) => {
    return response;
  },
  (error) => {
    // Handle common error scenarios
    if (error.response?.status === 401) {
      // Handle unauthorized access
      localStorage.removeItem('authToken');
      // Redirect to login if needed
    } else if (error.response?.status >= 500) {
      // Handle server errors
      console.error('Server error:', error.response.data);
    }
    return Promise.reject(error);
  }
);

// API Service Functions

/**
 * Get class overview data for dashboard
 * @returns {Promise} Class overview data including statistics, performance, and charts
 */
export const getClassOverview = async () => {
  try {
    const response = await apiClient.get('/class/overview');
    return response.data;
  } catch (error) {
    console.error('Error fetching class overview:', error);
    throw new Error(
      error.response?.data?.error || 
      'Failed to fetch class overview data'
    );
  }
};

/**
 * Search students by name or roll number
 * @param {string} query - Search query (name or roll number)
 * @param {number} page - Page number for pagination (default: 1)
 * @param {number} perPage - Items per page (default: 20)
 * @returns {Promise} Search results with student data and pagination info
 */
export const searchStudents = async (query = '', page = 1, perPage = 20) => {
  try {
    const params = new URLSearchParams();
    if (query.trim()) {
      params.append('search', query.trim());
    }
    params.append('page', page.toString());
    params.append('per_page', perPage.toString());

    const response = await apiClient.get(`/students?${params.toString()}`);
    return response.data;
  } catch (error) {
    console.error('Error searching students:', error);
    throw new Error(
      error.response?.data?.error || 
      'Failed to search students'
    );
  }
};

/**
 * Get all students (without search filter)
 * @param {number} page - Page number for pagination (default: 1)
 * @param {number} perPage - Items per page (default: 20)
 * @returns {Promise} All students with pagination info
 */
export const getAllStudents = async (page = 1, perPage = 20) => {
  return searchStudents('', page, perPage);
};

/**
 * Get detailed student performance data
 * @param {string} studentId - Student UUID
 * @returns {Promise} Detailed student performance data
 */
export const getStudentPerformance = async (studentId) => {
  try {
    if (!studentId) {
      throw new Error('Student ID is required');
    }

    const response = await apiClient.get(`/students/${studentId}/performance`);
    return response.data;
  } catch (error) {
    console.error('Error fetching student performance:', error);
    throw new Error(
      error.response?.data?.error || 
      'Failed to fetch student performance data'
    );
  }
};

/**
 * Get basic student information
 * @param {string} studentId - Student UUID
 * @returns {Promise} Basic student information
 */
export const getStudentInfo = async (studentId) => {
  try {
    if (!studentId) {
      throw new Error('Student ID is required');
    }

    const response = await apiClient.get(`/students/${studentId}`);
    return response.data;
  } catch (error) {
    console.error('Error fetching student info:', error);
    throw new Error(
      error.response?.data?.error || 
      'Failed to fetch student information'
    );
  }
};

/**
 * Upload Excel file with student performance data
 * @param {Object} fileData - File upload data
 * @param {File} fileData.file - Excel file to upload
 * @param {string} fileData.subjectName - Subject name
 * @param {string} fileData.assessmentName - Assessment name
 * @param {string} fileData.assessmentDate - Assessment date (YYYY-MM-DD)
 * @param {number} fileData.maxMarks - Maximum marks for the assessment
 * @param {Function} onUploadProgress - Progress callback function
 * @returns {Promise} Upload result with processing information
 */
export const uploadFile = async (fileData, onUploadProgress = null) => {
  try {
    const { file, subjectName, year, section, assessmentType } = fileData;

    // Validate required fields
    if (!file) {
      throw new Error('File is required');
    }
    if (!subjectName?.trim()) {
      throw new Error('Subject name is required');
    }
    if (!year) {
      throw new Error('Year is required');
    }
    if (!section) {
      throw new Error('Section is required');
    }

    // Create FormData for file upload
    const formData = new FormData();
    formData.append('file', file);
    formData.append('subjectName', subjectName.trim());
    formData.append('year', year.toString());
    formData.append('section', section);
    
    if (assessmentType) {
      formData.append('assessmentType', assessmentType);
    }

    // Upload with progress tracking
    const response = await apiClient.post('/upload/subject', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
      onUploadProgress: (progressEvent) => {
        if (onUploadProgress && progressEvent.total) {
          const percentCompleted = Math.round(
            (progressEvent.loaded * 100) / progressEvent.total
          );
          onUploadProgress(percentCompleted);
        }
      },
    });

    return response.data;
  } catch (error) {
    console.error('Error uploading file:', error);
    throw new Error(
      error.response?.data?.error || 
      'Failed to upload file'
    );
  }
};

/**
 * Get subjects list
 * @returns {Promise} List of all subjects
 */
export const getSubjects = async () => {
  try {
    const response = await apiClient.get('/upload/subjects');
    return response.data;
  } catch (error) {
    console.error('Error fetching subjects:', error);
    throw new Error(
      error.response?.data?.error || 
      'Failed to fetch subjects'
    );
  }
};

// Utility functions

/**
 * Check if API is available
 * @returns {Promise<boolean>} True if API is responding
 */
export const checkApiHealth = async () => {
  try {
    await apiClient.get('/class/overview');
    return true;
  } catch (error) {
    console.error('API health check failed:', error);
    return false;
  }
};

/**
 * Format API error for user display
 * @param {Error} error - Error object from API call
 * @returns {string} User-friendly error message
 */
export const formatApiError = (error) => {
  if (error.response?.data?.error) {
    return error.response.data.error;
  } else if (error.message) {
    return error.message;
  } else {
    return 'An unexpected error occurred. Please try again.';
  }
};

// Export the configured axios instance for custom requests
export { apiClient };

// Default export
const apiService = {
  getClassOverview,
  searchStudents,
  getAllStudents,
  getStudentPerformance,
  getStudentInfo,
  uploadFile,
  getSubjects,
  checkApiHealth,
  formatApiError,
};

export default apiService;