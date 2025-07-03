// src/components/AuthModal.jsx
import { useState } from "react";
import "./AuthModal.css";

// Base API URL from environment
const API = import.meta.env.VITE_BACKEND_URL;

const AuthModal = ({ onClose, onLoginSuccess }) => {
  const [isLogin, setIsLogin] = useState(true);
  const [formData, setFormData] = useState({ username: "", email: "", password: "" });

  const handleChange = (e) =>
    setFormData({ ...formData, [e.target.name]: e.target.value });

  const handleSubmit = async (e) => {
    e.preventDefault();
    // Make sure this matches your Flask routes (register vs signup)
    const endpoint = isLogin ? "/login" : "/register";
    const url = `${API}${endpoint}`;

    const payload = isLogin
      ? { username: formData.username, password: formData.password }
      : { username: formData.username, email: formData.email, password: formData.password };

    try {
      const response = await fetch(url, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });

      let data = {};
      try {
        data = await response.json();
      } catch {
        console.error("Failed to parse JSON from auth response");
      }

      if (response.ok) {
        const token = data.access_token || data.token;
        if (token) {
          localStorage.setItem("token", token);
          onLoginSuccess();
        } else {
          alert("Login succeeded but no token was returned.");
        }
      } else {
        alert(data.message || data.error || "Login/Signup failed");
      }
    } catch (err) {
      console.error("Network or server error during auth:", err);
      alert("An error occurred. Please try again.");
    }
  };

  return (
    <div className="auth-modal">
      <div className="auth-modal-content">
        <button className="close-btn" onClick={onClose}>
          close
        </button>
        <h2>{isLogin ? "Login" : "Sign Up"}</h2>
        <form onSubmit={handleSubmit}>
          <input
            name="username"
            placeholder="Username"
            value={formData.username}
            onChange={handleChange}
            required
          />
          {!isLogin && (
            <input
              name="email"
              placeholder="Email"
              value={formData.email}
              onChange={handleChange}
              required
            />
          )}
          <input
            name="password"
            type="password"
            placeholder="Password"
            value={formData.password}
            onChange={handleChange}
            required
          />
          <button type="submit">{isLogin ? "Login" : "Sign Up"}</button>
        </form>
        <p
          onClick={() => setIsLogin(!isLogin)}
          className="toggle-auth"
        >
          {isLogin
            ? "Don't have an account? Sign Up"
            : "Already have an account? Log In"}
        </p>
      </div>
    </div>
  );
};

export default AuthModal;
