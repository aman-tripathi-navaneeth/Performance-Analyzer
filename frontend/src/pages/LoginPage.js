import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../contexts/AuthContext";
import { authenticateUser } from "../services/authService";
import "./LoginPage.css";

/**
 * LoginPage Component - Authentication page for Ideal Performance Analyzer
 * Styled to match the college's design aesthetic with logo and clean form
 */
const LoginPage = () => {
  const navigate = useNavigate();
  const { login } = useAuth();

  // Form state
  const [formData, setFormData] = useState({
    email: "",
    password: "",
    role: "teacher", // Default to teacher
  });

  // UI state
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [showPassword, setShowPassword] = useState(false);

  // Handle input changes
  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: value,
    }));
    // Clear error when user starts typing
    if (error) setError("");
  };

  // Handle form submission
  const handleSubmit = async (e) => {
    e.preventDefault();

    // Basic validation
    if (!formData.email.trim()) {
      setError("Email ID is required");
      return;
    }

    if (!formData.password.trim()) {
      setError("Password is required");
      return;
    }

    // Email validation
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(formData.email)) {
      setError("Please enter a valid email address");
      return;
    }

    try {
      setLoading(true);
      setError("");

      // Authenticate user with the authentication service
      const authResult = await authenticateUser(
        formData.email,
        formData.password,
        formData.role
      );

      if (authResult.success) {
        // Use auth context to login with role
        login(authResult.user.email, authResult.token, authResult.user.role);

        // Navigate to dashboard (role-based routing will handle the rest)
        navigate("/");
      } else {
        setError(authResult.error || "Invalid credentials. Please try again.");
      }
    } catch (err) {
      setError("Login failed. Please check your credentials and try again.");
    } finally {
      setLoading(false);
    }
  };

  // Handle forgot password
  const handleForgotPassword = () => {
    alert("Please contact your administrator to reset your password.");
  };

  return (
    <div className="login-page">
      <div className="login-background">
        <div className="background-pattern"></div>
        <div className="background-gradient"></div>
      </div>

      <div className="login-container">
        <div className="login-card">
          {/* College Logo */}
          <div className="login-header">
            <div className="college-logo">
              <img
                src="/images/College Logo.jpeg"
                alt="Ideal Institute of Technology Logo"
                className="logo-image"
                onError={(e) => {
                  // Fallback if image doesn't load
                  e.target.style.display = "none";
                  e.target.nextElementSibling.style.display = "block";
                }}
              />
              {/* Fallback logo if image fails to load */}
              <div className="logo-fallback" style={{ display: "none" }}>
                <div className="fallback-circle">
                  <div className="fallback-book">📚</div>
                  <div className="fallback-text">IDEAL</div>
                </div>
              </div>
            </div>

            <h1 className="app-title">IDEAL Performance Analyzer</h1>
            <p className="app-subtitle">Sign in with your Email ID</p>
          </div>

          {/* Login Form */}
          <form className="login-form" onSubmit={handleSubmit}>
            {/* Role Selection */}
            <div className="form-group">
              <label className="form-label">Login As</label>
              <div className="role-selection">
                <div className="role-option">
                  <input
                    type="radio"
                    id="teacher"
                    name="role"
                    value="teacher"
                    checked={formData.role === "teacher"}
                    onChange={handleInputChange}
                    disabled={loading}
                  />
                  <label htmlFor="teacher" className="role-label">
                    <span className="role-icon">👨‍🏫</span>
                    <span className="role-text">Teacher</span>
                    <span className="role-description">
                      Access student performance data
                    </span>
                  </label>
                </div>
                <div className="role-option">
                  <input
                    type="radio"
                    id="admin"
                    name="role"
                    value="admin"
                    checked={formData.role === "admin"}
                    onChange={handleInputChange}
                    disabled={loading}
                  />
                  <label htmlFor="admin" className="role-label">
                    <span className="role-icon">👨‍💼</span>
                    <span className="role-text">Administrator</span>
                    <span className="role-description">
                      Manage teachers and sections
                    </span>
                  </label>
                </div>
              </div>
            </div>

            {/* Email Field */}
            <div className="form-group">
              <label htmlFor="email" className="form-label">
                Email ID
              </label>
              <div className="input-wrapper">
                <span className="input-icon"></span>
                <input
                  type="email"
                  id="email"
                  name="email"
                  className="form-input"
                  placeholder="Enter your email address"
                  value={formData.email}
                  onChange={handleInputChange}
                  disabled={loading}
                  autoComplete="email"
                  required
                />
              </div>
              <p className="input-hint">Use your institutional email address</p>
            </div>

            {/* Password Field */}
            <div className="form-group">
              <label htmlFor="password" className="form-label">
                Password
              </label>
              <div className="input-wrapper">
                <span className="input-icon"></span>
                <input
                  type={showPassword ? "text" : "password"}
                  id="password"
                  name="password"
                  className="form-input"
                  placeholder="Enter your password"
                  value={formData.password}
                  onChange={handleInputChange}
                  disabled={loading}
                  autoComplete="current-password"
                  required
                />
                <button
                  type="button"
                  className="password-toggle"
                  onClick={() => setShowPassword(!showPassword)}
                  disabled={loading}
                >
                  {showPassword ? "👁️" : "👁️‍🗨️"}
                </button>
              </div>
            </div>

            {/* Error Message */}
            {error && (
              <div className="error-message">
                <span className="error-icon"></span>
                {error}
              </div>
            )}

            {/* Submit Button */}
            <button
              type="submit"
              className={`login-button ${loading ? "loading" : ""}`}
              disabled={loading}
            >
              {loading ? (
                <>
                  <div className="loading-spinner"></div>
                  Signing In...
                </>
              ) : (
                "Sign In"
              )}
            </button>

            {/* Forgot Password */}
            <div className="form-footer">
              <button
                type="button"
                className="forgot-password-link"
                onClick={handleForgotPassword}
                disabled={loading}
              >
                Don't have an account? Contact Administrator
              </button>
            </div>
          </form>
        </div>

        {/* Footer */}
        <div className="login-footer">
          <p className="footer-text">
            © 2024 Ideal Institute of Technology. All rights reserved.
          </p>
          <p className="footer-version">Performance Analyzer v1.0</p>
        </div>
      </div>
    </div>
  );
};

export default LoginPage;
