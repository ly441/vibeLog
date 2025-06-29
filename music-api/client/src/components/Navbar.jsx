// src/components/Navbar.jsx
import { Link } from "react-router-dom";
import "./Navbar.css";
<Link to="/songs">Songs</Link>


const Navbar = ({ onLoginClick, onLogout, isAuthenticated }) => {
  return (
    <nav className="navbar">
      <div className="logo">
        <Link to="/" className="logo-link">vibeLog</Link>
      </div>

      <div className="nav-links">
        <Link to="/artists">Artists</Link>
        <Link to="/genres">Genres</Link>
        <Link to="/songs">Songs</Link>
      </div>

      <input type="text" placeholder="Search..." className="search-bar" />

      <div className="auth-button">
        {!isAuthenticated ? (
          <button className="auth-btn" onClick={onLoginClick}>
            Login / Sign Up
          </button>
        ) : (
          <button className="auth-btn" onClick={onLogout}>
            Logout
          </button>
        )}
      </div>
    </nav>
  );
};


export default Navbar;
