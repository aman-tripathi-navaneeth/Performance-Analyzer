/**
 * Test helpers and utilities for the Performance Analyzer
 */

/**
 * Mock student data for testing
 */
export const mockStudentData = {
  students: [
    {
      id: 1,
      full_name: "John Doe",
      student_roll_number: "STU001",
      performance_summary: {
        average_percentage: 85,
        grade: "A",
        total_subjects: 5,
        total_assessments: 12
      }
    },
    {
      id: 2,
      full_name: "Jane Smith",
      student_roll_number: "STU002",
      performance_summary: {
        average_percentage: 72,
        grade: "B",
        total_subjects: 5,
        total_assessments: 12
      }
    }
  ]
};

/**
 * Mock class overview data for testing
 */
export const mockClassOverview = {
  total_students: 25,
  average_score: 78.5,
  grade_distribution: {
    A: 5,
    B: 8,
    C: 7,
    D: 3,
    F: 2
  },
  subject_averages: {
    Math: 82,
    Science: 75,
    English: 78,
    History: 80,
    Geography: 73
  }
};

/**
 * Validate student data structure
 */
export const validateStudentData = (student) => {
  const required = ['id', 'full_name', 'student_roll_number'];
  return required.every(field => student.hasOwnProperty(field));
};

/**
 * Format percentage for display
 */
export const formatPercentage = (value) => {
  if (typeof value !== 'number') return 'N/A';
  return `${Math.round(value)}%`;
};

/**
 * Get grade color class
 */
export const getGradeColorClass = (grade) => {
  if (!grade) return 'grade-default';
  const gradeUpper = grade.toUpperCase();
  if (gradeUpper.includes('A')) return 'grade-a';
  if (gradeUpper.includes('B')) return 'grade-b';
  if (gradeUpper.includes('C')) return 'grade-c';
  if (gradeUpper.includes('D')) return 'grade-d';
  if (gradeUpper.includes('F')) return 'grade-f';
  return 'grade-default';
};