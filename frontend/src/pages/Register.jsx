import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import api from '../api/axios';

function Register({ onLogin }) {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      const response = await api.post('/api/auth/register', {
        email,
        password,
      });

      const userData = response.data;
      
      // After registration, automatically login
      const formData = new FormData();
      formData.append('username', email);
      formData.append('password', password);

      const loginResponse = await api.post('/api/auth/login', formData, {
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
        },
      });

      const { access_token } = loginResponse.data;
      localStorage.setItem('token', access_token);

      const payload = JSON.parse(atob(access_token.split('.')[1]));
      const loggedInUser = {
        email: payload.sub,
        role: payload.role,
      };

      onLogin(loggedInUser);
      navigate('/dashboard');
    } catch (err) {
      setError(err.response?.data?.detail || 'Registration failed. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="form-container">
      <h2>Register</h2>
      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label htmlFor="email">Email</label>
          <input
            type="email"
            id="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
          />
        </div>
        <div className="form-group">
          <label htmlFor="password">Password</label>
          <input
            type="password"
            id="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
        </div>
        {error && <div className="error">{error}</div>}
        <button type="submit" className="btn" disabled={loading}>
          {loading ? 'Registering...' : 'Register'}
        </button>
      </form>
      <p style={{ marginTop: '15px', textAlign: 'center' }}>
        Already have an account? <a href="/login">Login</a>
      </p>
    </div>
  );
}

export default Register;

