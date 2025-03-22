import React, { useState } from 'react';
import '../App.css';
import { useAuth } from '../context/AuthContext';

function Login({ onBack }) {
  const [formData, setFormData] = useState({
    username: '',
    password: ''
  });
  const { login, error } = useAuth();

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!formData.username || !formData.password) {
      return;
    }

    const success = await login(formData.username, formData.password);
    if (success) {
      onBack();
    }
  };

  return (
    <div className="auth-container">
      <div className="auth-box">
        <h2>Login</h2>
        {error && <div className="error-message">{error}</div>}
        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label htmlFor="username">Username</label>
            <input
              type="text"
              id="username"
              name="username"
              value={formData.username}
              onChange={handleChange}
              required
            />
          </div>
          <div className="form-group">
            <label htmlFor="password">Password</label>
            <input
              type="password"
              id="password"
              name="password"
              value={formData.password}
              onChange={handleChange}
              required
            />
          </div>
          <button type="submit" className="auth-submit-button">Login</button>
        </form>
        <button onClick={onBack} className="auth-back-button">Back to Chat</button>
      </div>
    </div>
  );
}

export default Login; 