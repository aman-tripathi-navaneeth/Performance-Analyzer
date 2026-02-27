import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { toast } from "sonner";
import { User, Lock, GraduationCap } from 'lucide-react';
import Navbar from '../components/Navbar';

const StudentLoginPage = () => {
    const [enrollmentId, setEnrollmentId] = useState('');
    const [password, setPassword] = useState('');
    const [isLoading, setIsLoading] = useState(false);
    const navigate = useNavigate();

    useEffect(() => {
        const userStr = localStorage.getItem('user');
        if (userStr) {
            try {
                const user = JSON.parse(userStr);
                if (user.role === 'student') {
                    navigate('/student-dashboard');
                }
            } catch (e) {
                // Ignore JSON parse errors
            }
        }
    }, [navigate]);

    const handleSubmit = (e: React.FormEvent) => {
        e.preventDefault();
        setIsLoading(true);

        setTimeout(() => {
            // Simulate demo student login
            if (enrollmentId === 'student1' && password === 'password') {
                localStorage.setItem('user', JSON.stringify({ role: 'student', username: enrollmentId }));
                toast.success('Student login successful!');
                navigate('/student-dashboard'); // Redirect to protected dashboard
            } else {
                toast.error('Invalid credentials. Try Enrollment ID: student1, password: password');
            }
            setIsLoading(false);
        }, 1000);
    };

    return (
        <div className="min-h-screen bg-background text-foreground transition-colors duration-300">
            <Navbar />
            <div className="container mx-auto px-4 md:px-6 py-24 flex items-center justify-center min-h-[calc(100vh-80px)]">
                <div className="w-full max-w-md mx-auto">
                    <div className="glass-card p-8 rounded-xl animate-scale-in">
                        <h2 className="text-3xl font-bold mb-2 text-center text-primary font-jetbrains">Student Portal</h2>
                        <p className="text-muted-foreground text-center mb-8">Access your academic profile</p>

                        <form onSubmit={handleSubmit} className="space-y-6">
                            <div className="space-y-2">
                                <label htmlFor="student-id" className="block text-sm font-medium">
                                    Enrollment ID
                                </label>
                                <div className="relative">
                                    <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none text-muted-foreground">
                                        <GraduationCap size={18} />
                                    </div>
                                    <input
                                        id="student-id"
                                        type="text"
                                        value={enrollmentId}
                                        onChange={(e) => setEnrollmentId(e.target.value)}
                                        className="bg-secondary/50 border border-border/50 text-foreground block w-full pl-10 py-3 rounded-lg focus:ring-2 focus:ring-primary/50 focus:border-primary/50 transition-all duration-200"
                                        placeholder="Enter your Enrollment ID"
                                        required
                                    />
                                </div>
                            </div>

                            <div className="space-y-2">
                                <label htmlFor="student-password" className="block text-sm font-medium">
                                    Password
                                </label>
                                <div className="relative">
                                    <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none text-muted-foreground">
                                        <Lock size={18} />
                                    </div>
                                    <input
                                        id="student-password"
                                        type="password"
                                        value={password}
                                        onChange={(e) => setPassword(e.target.value)}
                                        className="bg-secondary/50 border border-border/50 text-foreground block w-full pl-10 py-3 rounded-lg focus:ring-2 focus:ring-primary/50 focus:border-primary/50 transition-all duration-200"
                                        placeholder="Enter your password"
                                        required
                                    />
                                </div>
                            </div>

                            <div className="pt-2">
                                <button
                                    type="submit"
                                    disabled={isLoading}
                                    className={`stellar-btn w-full py-3 ${isLoading ? 'opacity-70 cursor-not-allowed' : ''}`}
                                >
                                    {isLoading ? 'Logging in...' : 'Log In'}
                                </button>
                            </div>

                            <div className="text-sm text-center text-muted-foreground mt-4 p-4 bg-secondary/30 rounded-lg">
                                <p>Demo credentials:</p>
                                <p>Enrollment ID: <span className="font-semibold text-foreground">student1</span></p>
                                <p>Password: <span className="font-semibold text-foreground">password</span></p>
                            </div>
                        </form>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default StudentLoginPage;
