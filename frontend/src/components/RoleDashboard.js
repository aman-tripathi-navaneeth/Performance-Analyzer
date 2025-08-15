import { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import DashboardPage from '../pages/DashboardPage';
import AdminDashboard from '../pages/AdminDashboard';

/**
 * RoleDashboard Component - Routes users to appropriate dashboard based on their role
 * Teachers see the performance analytics dashboard
 * Admins see the administrative dashboard
 */
const RoleDashboard = () => {
  const navigate = useNavigate();
  const userRole = localStorage.getItem('userRole');

  useEffect(() => {
    // If no role is found, default to teacher
    if (!userRole) {
      localStorage.setItem('userRole', 'teacher');
    }
  }, [userRole]);

  // Show admin dashboard for admins
  if (userRole === 'admin') {
    return <AdminDashboard />;
  }

  // Show teacher dashboard for teachers (default)
  return <DashboardPage />;
};

export default RoleDashboard;