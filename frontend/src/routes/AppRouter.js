import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';

// Import page components
import LoginPage from '../pages/LoginPage';
import DashboardPage from '../pages/DashboardPage';
import AdminDashboard from '../pages/AdminDashboard';
import RoleDashboard from '../components/RoleDashboard';
import StudentProfilePage from '../pages/StudentProfilePage';
import UploadPage from '../pages/UploadPage';
import StudentsPage from '../pages/StudentsPage';
import TeacherManagement from '../pages/TeacherManagement';
import ClassPerformancePage from '../pages/ClassPerformancePage';
import YearSelectionPage from '../pages/YearSelectionPage';
import YearPerformancePage from '../pages/YearPerformancePage';
import AnalyticsPage from '../pages/AnalyticsPage';
import ChartsPage from '../pages/ChartsPage';
import NotFoundPage from '../pages/NotFoundPage';
import NextGenAnalyticsPage from '../pages/NextGenAnalyticsPage';

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
              <RoleDashboard />
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
          path="/teacher-dashboard" 
          element={
            <ProtectedRoute>
              <DashboardPage />
            </ProtectedRoute>
          } 
        />

        {/* Students Dashboard - Main entry point */}
        <Route 
          path="/students" 
          element={
            <ProtectedRoute>
              <StudentsPage />
            </ProtectedRoute>
          } 
        />

        {/* Analytics Dashboard */}
        <Route 
          path="/analytics" 
          element={
            <ProtectedRoute>
              <AnalyticsPage />
            </ProtectedRoute>
          } 
        />

        {/* Charts Dashboard */}
        <Route 
          path="/charts" 
          element={
            <ProtectedRoute>
              <ChartsPage />
            </ProtectedRoute>
          } 
        />

        {/* Next-Gen Analytics (experimental) */}
        <Route 
          path="/analytics/next" 
          element={
            <ProtectedRoute>
              <NextGenAnalyticsPage />
            </ProtectedRoute>
          } 
        />

        {/* Year Performance - Shows sections for a specific year */}
        <Route 
          path="/students/year/:year" 
          element={
            <ProtectedRoute>
              <YearPerformancePage />
            </ProtectedRoute>
          } 
        />

        {/* Class Performance - Shows detailed class analytics */}
        <Route 
          path="/class-performance/:year/:section" 
          element={
            <ProtectedRoute>
              <ClassPerformancePage />
            </ProtectedRoute>
          } 
        />

        {/* Individual Student Profile */}
        <Route 
          path="/student/:studentId" 
          element={
            <ProtectedRoute>
              <StudentProfilePage />
            </ProtectedRoute>
          } 
        />

        {/* Upload Page */}
        <Route 
          path="/upload" 
          element={
            <ProtectedRoute>
              <UploadPage />
            </ProtectedRoute>
          } 
        />

        {/* Teacher Management - Admin only */}
        <Route 
          path="/admin/teachers" 
          element={
            <ProtectedRoute requireAdmin={true}>
              <TeacherManagement />
            </ProtectedRoute>
          } 
        />

        {/* Legacy route for backward compatibility */}
        <Route 
          path="/class/:year/:section" 
          element={
            <ProtectedRoute>
              <ClassPerformancePage />
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