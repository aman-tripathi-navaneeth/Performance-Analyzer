import { Navigate, Outlet } from 'react-router-dom';
import { toast } from "sonner";

interface ProtectedRouteProps {
    allowedRole: string;
}

const ProtectedRoute = ({ allowedRole }: ProtectedRouteProps) => {
    const userStr = localStorage.getItem('user');

    if (!userStr) {
        toast.error('Please log in to access this page');
        return <Navigate to={`/${allowedRole}-login`} replace />;
    }

    try {
        const user = JSON.parse(userStr);
        if (user.role !== allowedRole) {
            toast.error('Unauthorized access');
            return <Navigate to="/" replace />;
        }
        return <Outlet />;
    } catch (error) {
        localStorage.removeItem('user');
        return <Navigate to={`/${allowedRole}-login`} replace />;
    }
};

export default ProtectedRoute;
