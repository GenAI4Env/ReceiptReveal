import React from 'react';
import '../App.css';
import { useAuth } from '../context/AuthContext';
import treeIcon from '../assets/tree_icon.png';

function Profile({ onBack }) {
  const { user } = useAuth();

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
          <h2>{user?.username}</h2>
        </div>
        
        <div className="profile-stats">
          <div className="stat-item">
            <span className="stat-label">Reveal Coins</span>
            <span className="stat-value">{user?.coins || 0}</span>
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