import { useState } from "react";
import { useApp } from "../context/AppContext";
import "./AdminLogin.css";

const AdminLogin = ({ onClose }) => {
  const { dispatch, ACTIONS } = useApp();
  const [formData, setFormData] = useState({
    username: "",
    password: "",
  });
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  // Admin credentials for local authentication
  const ADMIN_CREDENTIALS = {
    username: "admin",
    password: "admin123",
  };

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: value,
    }));
    // Clear error when user starts typing
    if (error) setError("");
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError("");

    // Simulate API call delay
    await new Promise((resolve) => setTimeout(resolve, 1000));

    if (
      formData.username === ADMIN_CREDENTIALS.username &&
      formData.password === ADMIN_CREDENTIALS.password
    ) {
      // Successful login
      dispatch({ type: ACTIONS.SET_ADMIN_AUTHENTICATED, payload: true });
      dispatch({ type: ACTIONS.SET_ADMIN_MODE, payload: true });

      // Show success message
      alert("Login successful! Welcome to Admin Panel.");

      if (onClose) onClose();
    } else {
      setError("Invalid username or password. Please try again.");
    }

    setLoading(false);
  };

  const handleBackdropClick = (e) => {
    if (e.target === e.currentTarget && onClose) {
      onClose();
    }
  };

  return (
    <div className="admin-login-overlay" onClick={handleBackdropClick}>
      <div className="admin-login-modal">
        <div className="login-header">
          <h2>Admin Login</h2>
          <button className="close-button" onClick={onClose} type="button">
            ✕
          </button>
        </div>

        <form onSubmit={handleSubmit} className="login-form">
          {error && (
            <div className="error-message">
              <span className="error-icon">⚠️</span>
              {error}
            </div>
          )}

          <div className="form-group">
            <label htmlFor="username">Username</label>
            <input
              type="text"
              id="username"
              name="username"
              value={formData.username}
              onChange={handleInputChange}
              required
              disabled={loading}
              placeholder="Enter your username"
            />
          </div>

          <div className="form-group">
            <label htmlFor="password">Password</label>
            <input
              type="password"
              id="password"
              name="password"
              value={formData.password}
              onChange={handleInputChange}
              required
              disabled={loading}
              placeholder="Enter your password"
            />
          </div>

          <div className="form-actions">
            <button
              type="submit"
              className="login-button"
              disabled={loading || !formData.username || !formData.password}
            >
              {loading ? (
                <>
                  <span className="loading-spinner"></span>
                  Logging in...
                </>
              ) : (
                <>🔐 Login to Admin Panel</>
              )}
            </button>

            <button
              type="button"
              className="cancel-button"
              onClick={onClose}
              disabled={loading}
            >
              Cancel
            </button>
          </div>
        </form>

        <div className="login-footer">
          <p>
            <span className="security-icon">🔒</span>
            Secure admin access for Daily Post management
          </p>
        </div>
      </div>
    </div>
  );
};

export default AdminLogin;
