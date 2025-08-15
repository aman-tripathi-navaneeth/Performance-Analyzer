/**
 * Authentication Service - Handles user authentication and teacher management
 */

// In a real application, this would be stored in a database
// For demo purposes, we'll use localStorage to persist teacher data
const TEACHERS_STORAGE_KEY = "teachers_data";
const ADMIN_CREDENTIALS = {
  email: "aman@gmail.com",
  password: "aman123",
  role: "admin",
};

// Initialize with default admin and some sample teachers
const initializeTeachers = () => {
  const existingTeachers = localStorage.getItem(TEACHERS_STORAGE_KEY);
  if (!existingTeachers) {
    const defaultTeachers = [
      {
        id: 1,
        name: "Teacher",
        email: "aman@gmail.com",
        password: "aman123",
        role: "teacher",
        sections: ["CSE A", "CSE B"],
      },
    ];
    localStorage.setItem(TEACHERS_STORAGE_KEY, JSON.stringify(defaultTeachers));
  }
};

// Get all teachers
export const getTeachers = () => {
  initializeTeachers();
  const teachers = localStorage.getItem(TEACHERS_STORAGE_KEY);
  return teachers ? JSON.parse(teachers) : [];
};

// Add a new teacher
export const addTeacher = (teacherData) => {
  const teachers = getTeachers();
  const newTeacher = {
    ...teacherData,
    id: Date.now(),
    sections: [],
  };
  teachers.push(newTeacher);
  localStorage.setItem(TEACHERS_STORAGE_KEY, JSON.stringify(teachers));
  return newTeacher;
};

// Update teacher
export const updateTeacher = (teacherId, updates) => {
  const teachers = getTeachers();
  const updatedTeachers = teachers.map((teacher) =>
    teacher.id === teacherId ? { ...teacher, ...updates } : teacher
  );
  localStorage.setItem(TEACHERS_STORAGE_KEY, JSON.stringify(updatedTeachers));
  return updatedTeachers.find((t) => t.id === teacherId);
};

// Remove teacher
export const removeTeacher = (teacherId) => {
  const teachers = getTeachers();
  const filteredTeachers = teachers.filter(
    (teacher) => teacher.id !== teacherId
  );
  localStorage.setItem(TEACHERS_STORAGE_KEY, JSON.stringify(filteredTeachers));
  return true;
};

// Authenticate user with backend API
export const authenticateUser = async (email, password, role) => {
  try {
    const response = await fetch(`${process.env.REACT_APP_API_URL || 'http://localhost:5000/api/v1'}/auth/login`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        email,
        password,
        role
      })
    });

    const data = await response.json();

    if (response.ok && data.success) {
      return {
        success: true,
        user: data.user,
        token: data.token
      };
    } else {
      return {
        success: false,
        error: data.error || 'Authentication failed'
      };
    }
  } catch (error) {
    console.error('Authentication error:', error);
    return {
      success: false,
      error: 'Network error. Please check your connection.'
    };
  }
};

// Check if email already exists
export const emailExists = (email) => {
  const teachers = getTeachers();
  return (
    teachers.some((teacher) => teacher.email === email) ||
    email === ADMIN_CREDENTIALS.email
  );
};
