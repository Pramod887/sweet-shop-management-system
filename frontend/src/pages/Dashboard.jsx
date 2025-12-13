import { useState, useEffect } from 'react';
import api from '../api/axios';
import SweetCard from '../components/SweetCard';

function Dashboard({ user, onLogout }) {
  const [sweets, setSweets] = useState([]);
  const [searchQuery, setSearchQuery] = useState('');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    fetchSweets();
  }, []);

  const fetchSweets = async () => {
    try {
      setLoading(true);
      const response = await api.get('/api/sweets');
      setSweets(response.data);
      setError('');
    } catch (err) {
      setError('Failed to load sweets. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const handleSearch = async () => {
    if (!searchQuery.trim()) {
      fetchSweets();
      return;
    }

    try {
      setLoading(true);
      const response = await api.get(`/api/sweets/search?query=${encodeURIComponent(searchQuery)}`);
      setSweets(response.data);
      setError('');
    } catch (err) {
      setError('Search failed. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const handlePurchase = async (sweetId, quantity = 1) => {
    try {
      await api.post(`/api/sweets/${sweetId}/purchase`, { quantity });
      fetchSweets(); // Refresh the list
      alert('Purchase successful!');
    } catch (err) {
      alert(err.response?.data?.detail || 'Purchase failed. Please try again.');
    }
  };

  return (
    <div>
      <div className="navbar">
        <h1>Sweet Shop - Dashboard</h1>
        <div className="navbar-actions">
          <span style={{ marginRight: '10px' }}>{user?.email}</span>
          <button onClick={onLogout}>Logout</button>
        </div>
      </div>
      <div className="container">
        <h2>Available Sweets</h2>
        <div style={{ display: 'flex', gap: '10px', marginBottom: '20px' }}>
          <input
            type="text"
            className="search-bar"
            placeholder="Search by name or category..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            onKeyPress={(e) => e.key === 'Enter' && handleSearch()}
          />
          <button className="btn btn-secondary" onClick={handleSearch} style={{ width: 'auto', padding: '12px 24px' }}>
            Search
          </button>
        </div>
        {error && <div className="error">{error}</div>}
        {loading ? (
          <p>Loading...</p>
        ) : sweets.length === 0 ? (
          <p>No sweets found.</p>
        ) : (
          <div className="sweet-grid">
            {sweets.map((sweet) => (
              <SweetCard key={sweet.id} sweet={sweet} onPurchase={handlePurchase} />
            ))}
          </div>
        )}
      </div>
    </div>
  );
}

export default Dashboard;

