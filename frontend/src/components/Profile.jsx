import React, { useEffect, useState } from 'react';
import '../App.css';
import { useAuth } from '../context/AuthContext';
import treeIcon from '../assets/tree_icon.png';

function Profile({ onBack }) {
  const [loading, setLoading] = useState(false);
  const [coins, setCoins] = useState(0);
  const { user } = useAuth();

  useEffect(() => {
    const fetchCoins = async () => {
      setLoading(true);
      try {
        const response = await fetch('http://127.0.0.1:5000/db/coins', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ email: localStorage.getItem('email') }),
        });
        
        if (!response.ok) {
          throw new Error('Failed to fetch coins');
        }
        const data = await response.json();
        console.log(data)
        // Update the user object with the fetched coins without creating duplicate keys
        setCoins(data.coins);
      } catch (error) {
        console.error('Error fetching coins:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchCoins();
  }, []);

  return (
    <div className="auth-container">
      <div className="auth-box profile-box">
        <div className="profile-header">
          <div className="profile-image-container">
            <img 
              src={user?.profileImage || treeIcon} 
              alt="Profile" 
              className="profile-image"
            />
            <button className="change-image-button">Change Image</button>
          </div>
          <h2>{localStorage.getItem('email')}</h2>
        </div>
        
        <div className="profile-stats">
          <div className="stat-item">
            <span className="stat-label">Reveal Coins</span>
            <span className="stat-value">{coins || 0}</span>
          </div>
          <div className="stat-item">
            <span className="stat-label">Member Since</span>
            <span className="stat-value">
              {new Date(user?.createdAt).toLocaleDateString()}
            </span>
          </div>
        </div>

        <button onClick={onBack} className="auth-back-button">Back to Chat</button>
      </div>
    </div>
  );
}

export default Profile; 