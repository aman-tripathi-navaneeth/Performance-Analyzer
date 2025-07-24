import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';

// Import page components
import LoginPage from '../pages/LoginPage';
import DashboardPage from '../pages/DashboardPage';
import AdminDashboard from '../pages/AdminDashboard';
import StudentProfilePage from '../pages/StudentProfilePage';
import UploadPage from '../pages/UploadPage';
import StudentsPage from '../pages/StudentsPage';
import NotFoundPage from '../pages/NotFoundPage';

/**
 * ProtectedRoute - Component to protect routes that require authentication
 */
const ProtectedRoute = ({ children, requireAdmin = false }) => {
  const isAuthenticated = localStorage.getItem('authToken');
  const userRole = localStorage.getItem('userRole');
  
  if (!isAuthenticated) {
    return <Navigate to="/login" replace />;
  }
  
  if (requireAdmin && userRole !== 'admin') {
    return <Navigate to="/" replace />;
  }
  
  return children;
};

/**
 * AppRouter - Centralized routing configuration for the Performance Analyzer
 * Handles all navigation logic, route definitions, and authentication
 */
const AppRouter = () => {
  return (
    <BrowserRouter>
      <Routes>
        {/* Login Route - Public */}
        <Route 
          path="/login" 
          element={<LoginPage />} 
        />

        {/* Protected Routes - Require Authentication */}
        <Route 
          path="/" 
          element={
            <ProtectedRoute>
              <DashboardPage />
            </ProtectedRoute>
          } 
        />

        <Route 
          path="/admin" 
          element={
            <ProtectedRoute requireAdmin={true}>
              <AdminDashboard />
            </ProtectedRoute>
          } 
        />

        <Route 
          path="/students" 
          element={
            <ProtectedRoute>
              <StudentsPage />
            </ProtectedRoute>
          } 
        />

        <Route 
          path="/student/:studentId" 
          element={
            <ProtectedRoute>
              <StudentProfilePage />
            </ProtectedRoute>
          } 
        />

        <Route 
          path="/upload" 
          element={
            <ProtectedRoute>
              <UploadPage />
            </ProtectedRoute>
          } 
        />

        {/* Redirect legacy routes for backward compatibility */}
        <Route 
          path="/dashboard" 
          element={<Navigate to="/" replace />} 
        />

        {/* 404 Not Found Route - Must be last */}
        <Route 
          path="*" 
          element={<NotFoundPage />} 
        />
      </Routes>
    </BrowserRouter>
  );
};

export default AppRouter;