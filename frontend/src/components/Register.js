import React, { useState } from 'react';
import api from '../api/axios';

/**
 * Registration form component.
 * POSTs to /api/auth/register/. On success, redirects to login or auto-logs in.
 */
function Register({ onLoginSuccess, onSwitchToLogin }) {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);
    try {
      await api.post('/api/auth/register/', { username, password });
      // Auto-login after successful registration
      const loginRes = await api.post('/api/auth/login/', { username, password });
      if (loginRes.data) {
        onLoginSuccess();
      }
    } catch (err) {
      const msg = err.response?.data?.error
        || err.response?.data?.detail
        || err.message
        || 'Registration failed';
      setError(Array.isArray(msg) ? msg.join(', ') : String(msg));
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="auth-container">
      <h2>Create Account</h2>
      <form className="auth-form" onSubmit={handleSubmit}>
        {error && <div className="auth-error">{error}</div>}
        <div className="form-group">
          <label htmlFor="reg-username">Username</label>
          <input
            id="reg-username"
            type="text"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            required
            autoComplete="username"
          />
        </div>
        <div className="form-group">
          <label htmlFor="reg-password">Password</label>
          <input
            id="reg-password"
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
            autoComplete="new-password"
          />
        </div>
        <button type="submit" disabled={loading}>
          {loading ? 'Registering...' : 'Register'}
        </button>
      </form>
      {onSwitchToLogin && (
        <div className="auth-link">
          Already have an account?{' '}
          <a href="#" onClick={(e) => { e.preventDefault(); onSwitchToLogin(); }}>
            Login
          </a>
        </div>
      )}
    </div>
  );
}

export default Register;
