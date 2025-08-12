import React from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

const Navbar = () => {
  const { isAuthenticated, user, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  return (
    <nav className="navbar">
      <div className="container">
        <div className="navbar-content">
          <Link to="/" className="navbar-brand">
            Kidney Anomaly Detection
          </Link>
          
          <ul className="navbar-nav">
            {isAuthenticated ? (
              <>
                <li>
                  <Link to="/dashboard" className="nav-link">
                    Dashboard
                  </Link>
                </li>
                <li>
                  <Link to="/upload" className="nav-link">
                    Upload Scan
                  </Link>
                </li>
                <li>
                  <Link to="/results" className="nav-link">
                    Results
                  </Link>
                </li>
                <li>
                  <span className="nav-link">
                    Welcome, {user?.name}
                  </span>
                </li>
                <li>
                  <button 
                    onClick={handleLogout}
                    className="btn btn-secondary"
                    style={{ margin: 0 }}
                  >
                    Logout
                  </button>
                </li>
              </>
            ) : (
              <>
                <li>
                  <Link to="/login" className="nav-link">
                    Login
                  </Link>
                </li>
                <li>
                  <Link to="/register" className="nav-link">
                    Register
                  </Link>
                </li>
              </>
            )}
          </ul>
        </div>
      </div>
    </nav>
  );
};

export default Navbar;
