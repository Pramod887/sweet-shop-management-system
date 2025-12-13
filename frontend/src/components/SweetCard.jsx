import { useState } from 'react';

function SweetCard({ sweet, onPurchase }) {
  const [quantity, setQuantity] = useState(1);
  const isOutOfStock = sweet.quantity === 0;

  const handlePurchase = () => {
    if (!isOutOfStock && quantity > 0 && quantity <= sweet.quantity) {
      onPurchase(sweet.id, quantity);
    }
  };

  return (
    <div className="sweet-card">
      <h3>{sweet.name}</h3>
      <p><strong>Category:</strong> {sweet.category}</p>
      <p><strong>Price:</strong> ₹{sweet.price.toFixed(2)}</p>
      <p><strong>Stock:</strong> {sweet.quantity}</p>
      {!isOutOfStock && (
        <div style={{ marginTop: '15px' }}>
          <input
            type="number"
            min="1"
            max={sweet.quantity}
            value={quantity}
            onChange={(e) => setQuantity(parseInt(e.target.value) || 1)}
            style={{ width: '60px', padding: '5px', marginRight: '10px' }}
          />
          <button
            className="btn btn-small"
            onClick={handlePurchase}
            disabled={quantity <= 0 || quantity > sweet.quantity}
          >
            Purchase
          </button>
        </div>
      )}
      {isOutOfStock && (
        <p style={{ color: '#f44336', marginTop: '15px', fontWeight: 'bold' }}>
          Out of Stock
        </p>
      )}
    </div>
  );
}

export default SweetCard;

