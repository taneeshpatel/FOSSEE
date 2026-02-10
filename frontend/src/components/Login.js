import React, { useState } from 'react';
import api from '../api/axios';

/**
 * Login form component.
 * POSTs to /api/auth/login/ and calls onLoginSuccess on success.
 */
function Login({ onLoginSuccess, onSwitchToRegister }) {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);
    try {
      const res = await api.post('/api/auth/login/', { username, password });
      if (res.data) {
        onLoginSuccess();
      }
    } catch (err) {
      const msg = err.response?.data?.error
        || err.response?.data?.detail
        || err.message
        || 'Login failed';
      setError(Array.isArray(msg) ? msg.join(', ') : String(msg));
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="auth-container">
      <h2>Chemical Equipment Visualizer</h2>
      <form className="auth-form" onSubmit={handleSubmit}>
        {error && <div className="auth-error">{error}</div>}
        <div className="form-group">
          <label htmlFor="username">Username</label>
          <input
            id="username"
            type="text"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            required
            autoComplete="username"
          />
        </div>
        <div className="form-group">
          <label htmlFor="password">Password</label>
          <input
            id="password"
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
            autoComplete="current-password"
          />
        </div>
        <button type="submit" disabled={loading}>
          {loading ? 'Logging in...' : 'Login'}
        </button>
      </form>
      {onSwitchToRegister && (
        <div className="auth-link">
          Don't have an account?{' '}
          <a href="#" onClick={(e) => { e.preventDefault(); onSwitchToRegister(); }}>
            Register
          </a>
        </div>
      )}
    </div>
  );
}

export default Login;
