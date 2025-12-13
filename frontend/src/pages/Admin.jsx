import { useState, useEffect } from 'react';
import api from '../api/axios';

function Admin({ user, onLogout }) {
  const [sweets, setSweets] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  
  // Form state
  const [formData, setFormData] = useState({
    name: '',
    category: '',
    price: '',
    quantity: '',
  });
  const [editingId, setEditingId] = useState(null);
  const [restockId, setRestockId] = useState(null);
  const [restockQuantity, setRestockQuantity] = useState('');

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

  const handleInputChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setSuccess('');

    try {
      if (editingId) {
        // Update existing sweet
        await api.put(`/api/sweets/${editingId}`, formData);
        setSuccess('Sweet updated successfully!');
      } else {
        // Create new sweet
        await api.post('/api/sweets', formData);
        setSuccess('Sweet added successfully!');
      }
      resetForm();
      fetchSweets();
    } catch (err) {
      setError(err.response?.data?.detail || 'Operation failed. Please try again.');
    }
  };

  const handleEdit = (sweet) => {
    setEditingId(sweet.id);
    setFormData({
      name: sweet.name,
      category: sweet.category,
      price: sweet.price.toString(),
      quantity: sweet.quantity.toString(),
    });
  };

  const handleDelete = async (sweetId) => {
    if (!window.confirm('Are you sure you want to delete this sweet?')) {
      return;
    }

    try {
      await api.delete(`/api/sweets/${sweetId}`);
      setSuccess('Sweet deleted successfully!');
      fetchSweets();
    } catch (err) {
      setError(err.response?.data?.detail || 'Delete failed. Please try again.');
    }
  };

  const handleRestock = async (e) => {
    e.preventDefault();
    if (!restockId || !restockQuantity) return;

    try {
      await api.post(`/api/sweets/${restockId}/restock`, {
        quantity: parseInt(restockQuantity),
      });
      setSuccess('Sweet restocked successfully!');
      setRestockId(null);
      setRestockQuantity('');
      fetchSweets();
    } catch (err) {
      setError(err.response?.data?.detail || 'Restock failed. Please try again.');
    }
  };

  const resetForm = () => {
    setFormData({
      name: '',
      category: '',
      price: '',
      quantity: '',
    });
    setEditingId(null);
  };

  return (
    <div>
      <div className="navbar">
        <h1>Sweet Shop - Admin Panel</h1>
        <div className="navbar-actions">
          <span style={{ marginRight: '10px' }}>{user?.email}</span>
          <button onClick={onLogout}>Logout</button>
        </div>
      </div>
      <div className="container">
        <div className="admin-form">
          <h2>{editingId ? 'Update Sweet' : 'Add New Sweet'}</h2>
          <form onSubmit={handleSubmit}>
            <div className="form-row">
              <div className="form-group">
                <label>Name</label>
                <input
                  type="text"
                  name="name"
                  value={formData.name}
                  onChange={handleInputChange}
                  required
                />
              </div>
              <div className="form-group">
                <label>Category</label>
                <input
                  type="text"
                  name="category"
                  value={formData.category}
                  onChange={handleInputChange}
                  required
                />
              </div>
            </div>
            <div className="form-row">
              <div className="form-group">
                <label>Price</label>
                <input
                  type="number"
                  step="0.01"
                  name="price"
                  value={formData.price}
                  onChange={handleInputChange}
                  required
                />
              </div>
              <div className="form-group">
                <label>Quantity</label>
                <input
                  type="number"
                  name="quantity"
                  value={formData.quantity}
                  onChange={handleInputChange}
                  required
                />
              </div>
            </div>
            {error && <div className="error">{error}</div>}
            {success && <div className="success">{success}</div>}
            <div style={{ display: 'flex', gap: '10px' }}>
              <button type="submit" className="btn btn-small">
                {editingId ? 'Update' : 'Add Sweet'}
              </button>
              {editingId && (
                <button type="button" className="btn btn-small btn-secondary" onClick={resetForm}>
                  Cancel
                </button>
              )}
            </div>
          </form>
        </div>

        <h2>Manage Sweets</h2>
        {loading ? (
          <p>Loading...</p>
        ) : sweets.length === 0 ? (
          <p>No sweets found. Add your first sweet!</p>
        ) : (
          <div className="sweet-grid">
            {sweets.map((sweet) => (
              <div key={sweet.id} className="sweet-card">
                <h3>{sweet.name}</h3>
                <p><strong>Category:</strong> {sweet.category}</p>
                <p><strong>Price:</strong> ₹{sweet.price.toFixed(2)}</p>
                <p><strong>Stock:</strong> {sweet.quantity}</p>
                <div style={{ marginTop: '15px', display: 'flex', gap: '10px', flexWrap: 'wrap' }}>
                  <button
                    className="btn btn-small btn-secondary"
                    onClick={() => handleEdit(sweet)}
                  >
                    Edit
                  </button>
                  <button
                    className="btn btn-small btn-danger"
                    onClick={() => handleDelete(sweet.id)}
                  >
                    Delete
                  </button>
                  {restockId === sweet.id ? (
                    <form onSubmit={handleRestock} style={{ display: 'flex', gap: '5px', flex: '1 1 100%' }}>
                      <input
                        type="number"
                        placeholder="Quantity"
                        value={restockQuantity}
                        onChange={(e) => setRestockQuantity(e.target.value)}
                        style={{ flex: 1, padding: '5px' }}
                        required
                      />
                      <button type="submit" className="btn btn-small">Restock</button>
                      <button
                        type="button"
                        className="btn btn-small"
                        onClick={() => {
                          setRestockId(null);
                          setRestockQuantity('');
                        }}
                      >
                        Cancel
                      </button>
                    </form>
                  ) : (
                    <button
                      className="btn btn-small"
                      onClick={() => setRestockId(sweet.id)}
                    >
                      Restock
                    </button>
                  )}
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}

export default Admin;

