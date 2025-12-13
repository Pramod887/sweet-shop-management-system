import { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import Login from './pages/Login';
import Register from './pages/Register';
import Dashboard from './pages/Dashboard';
import Admin from './pages/Admin';

function App() {
  const [user, setUser] = useState(null);

  useEffect(() => {
    const storedUser = localStorage.getItem('user');
    if (storedUser) {
      setUser(JSON.parse(storedUser));
    }
  }, []);

  const handleLogin = (userData) => {
    setUser(userData);
    localStorage.setItem('user', JSON.stringify(userData));
  };

  const handleLogout = () => {
    setUser(null);
    localStorage.removeItem('user');
    localStorage.removeItem('token');
  };

  const ProtectedRoute = ({ children, requireAdmin = false }) => {
    if (!user) {
      return <Navigate to="/login" />;
    }
    if (requireAdmin && user.role !== 'ADMIN') {
      return <Navigate to="/dashboard" />;
    }
    return children;
  };

  return (
    <Router>
      <Routes>
        <Route
          path="/login"
          element={
            user ? <Navigate to={user.role === 'ADMIN' ? '/admin' : '/dashboard'} /> : <Login onLogin={handleLogin} />
          }
        />
        <Route
          path="/register"
          element={
            user ? <Navigate to={user.role === 'ADMIN' ? '/admin' : '/dashboard'} /> : <Register onLogin={handleLogin} />
          }
        />
        <Route
          path="/dashboard"
          element={
            <ProtectedRoute>
              <Dashboard user={user} onLogout={handleLogout} />
            </ProtectedRoute>
          }
        />
        <Route
          path="/admin"
          element={
            <ProtectedRoute requireAdmin={true}>
              <Admin user={user} onLogout={handleLogout} />
            </ProtectedRoute>
          }
        />
        <Route path="/" element={<Navigate to={user ? (user.role === 'ADMIN' ? '/admin' : '/dashboard') : '/login'} />} />
      </Routes>
    </Router>
  );
}

export default App;

