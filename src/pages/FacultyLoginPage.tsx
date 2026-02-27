import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { toast } from "sonner";
import { User, Lock } from 'lucide-react';
import Navbar from '../components/Navbar';

const FacultyLoginPage = () => {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [isLoading, setIsLoading] = useState(false);
    const navigate = useNavigate();

    useEffect(() => {
        const userStr = localStorage.getItem('user');
        if (userStr) {
            try {
                const user = JSON.parse(userStr);
                if (user.role === 'faculty') {
                    navigate('/faculty-dashboard');
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
            // Simulate demo faculty login
            if ((username === 'faculty1' && password === 'password') || (username === 'admin' && password === 'admin') || (username === 'sairaj' && password === 'root') || (username === 'anjali' && password === 'root') || (username === 'ravi' && password === 'root') || (username === 'abhishek' && password === 'root')) {
                localStorage.setItem('user', JSON.stringify({ role: 'faculty', username }));
                toast.success('Faculty login successful!');
                navigate('/faculty-dashboard'); // Redirect to protected dashboard
            } else {
                toast.error('Invalid credentials. Try username: faculty1, password: password');
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
                        <h2 className="text-3xl font-bold mb-2 text-center text-primary font-jetbrains">Faculty Portal</h2>
                        <p className="text-muted-foreground text-center mb-8">Access academic tools and analytics</p>

                        <form onSubmit={handleSubmit} className="space-y-6">
                            <div className="space-y-2">
                                <label htmlFor="faculty-username" className="block text-sm font-medium">
                                    Faculty Username
                                </label>
                                <div className="relative">
                                    <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none text-muted-foreground">
                                        <User size={18} />
                                    </div>
                                    <input
                                        id="faculty-username"
                                        type="text"
                                        value={username}
                                        onChange={(e) => setUsername(e.target.value)}
                                        className="bg-secondary/50 border border-border/50 text-foreground block w-full pl-10 py-3 rounded-lg focus:ring-2 focus:ring-primary/50 focus:border-primary/50 transition-all duration-200"
                                        placeholder="Enter your username"
                                        required
                                    />
                                </div>
                            </div>

                            <div className="space-y-2">
                                <label htmlFor="faculty-password" className="block text-sm font-medium">
                                    Password
                                </label>
                                <div className="relative">
                                    <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none text-muted-foreground">
                                        <Lock size={18} />
                                    </div>
                                    <input
                                        id="faculty-password"
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
                                <p>HOD: username: <span className="font-semibold text-foreground">admin</span>, password: <span className="font-semibold text-foreground">admin</span></p>
                                <p>Faculty: username: <span className="font-semibold text-foreground">faculty1</span>, password: <span className="font-semibold text-foreground">password</span></p>
                            </div>
                        </form>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default FacultyLoginPage;
