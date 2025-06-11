import { useState } from 'react'
import { Lock, User } from 'lucide-react'
import AdminPanel from './AdminPanel'
import './AdminAuth.css'

const AdminAuth = () => {
  const [isAuthenticated, setIsAuthenticated] = useState(false)
  const [credentials, setCredentials] = useState({
    username: '',
    password: ''
  })
  const [error, setError] = useState('')

  // Simple authentication (in a real app, this would be more secure)
  const ADMIN_CREDENTIALS = {
    username: 'admin',
    password: 'admin123'
  }

  const handleLogin = (e) => {
    e.preventDefault()
    
    if (credentials.username === ADMIN_CREDENTIALS.username && 
        credentials.password === ADMIN_CREDENTIALS.password) {
      setIsAuthenticated(true)
      setError('')
      // Store auth state in sessionStorage
      sessionStorage.setItem('adminAuth', 'true')
    } else {
      setError('Invalid username or password')
    }
  }

  const handleLogout = () => {
    setIsAuthenticated(false)
    sessionStorage.removeItem('adminAuth')
    setCredentials({ username: '', password: '' })
  }

  // Check if already authenticated on component mount
  useState(() => {
    const authState = sessionStorage.getItem('adminAuth')
    if (authState === 'true') {
      setIsAuthenticated(true)
    }
  }, [])

  if (isAuthenticated) {
    return (
      <div className="admin-wrapper">
        <div className="admin-nav">
          <div className="admin-nav-content">
            <h2>📰 Daily Post Admin</h2>
            <button className="logout-btn" onClick={handleLogout}>
              Logout
            </button>
          </div>
        </div>
        <AdminPanel />
      </div>
    )
  }

  return (
    <div className="admin-login">
      <div className="login-container">
        <div className="login-header">
          <Lock size={48} />
          <h1>Admin Login</h1>
          <p>Please enter your credentials to access the admin panel</p>
        </div>

        <form onSubmit={handleLogin} className="login-form">
          {error && <div className="error-message">{error}</div>}
          
          <div className="form-group">
            <label>
              <User size={20} />
              Username
            </label>
            <input
              type="text"
              value={credentials.username}
              onChange={(e) => setCredentials({
                ...credentials,
                username: e.target.value
              })}
              placeholder="Enter username"
              required
            />
          </div>

          <div className="form-group">
            <label>
              <Lock size={20} />
              Password
            </label>
            <input
              type="password"
              value={credentials.password}
              onChange={(e) => setCredentials({
                ...credentials,
                password: e.target.value
              })}
              placeholder="Enter password"
              required
            />
          </div>

          <button type="submit" className="login-btn">
            Login to Admin Panel
          </button>
        </form>

        <div className="login-info">
          <p><strong>Demo Credentials:</strong></p>
          <p>Username: admin</p>
          <p>Password: admin123</p>
        </div>
      </div>
    </div>
  )
}

export default AdminAuth
