// src/App.jsx
import React, { useState } from 'react';
import './App.css';
import logo from './assets/RRlogo.png';
import userIcon from './assets/user.png';
import leafIcon from './assets/leaf.png';
import SignUp from './components/SignUp';
import Login from './components/Login';
import { useAuth } from './context/AuthContext';
import Profile from './components/Profile';

function App() {
  const [messages, setMessages] = useState([]);
  const [inputText, setInputText] = useState('');
  const [selectedImage, setSelectedImage] = useState(null);
  const [showSignUp, setShowSignUp] = useState(false);
  const [showLogin, setShowLogin] = useState(false);
  const [showProfile, setShowProfile] = useState(false);
  const { isLoggedIn, logout } = useAuth();

  const handleSend = () => {
    if (!inputText && !selectedImage) return;

    const newMessage = {
      text: inputText,
      image: selectedImage,
      isUser: true,
      timestamp: new Date().toISOString()
    };

    // Add user message
    setMessages(prev => [...prev, newMessage]);

    // Simulate AI response (you can replace this with actual API call)
    setTimeout(() => {
      const aiMessage = {
        text: "I'm processing your receipt...",
        isUser: false,
        timestamp: new Date().toISOString()
      };
      setMessages(prev => [...prev, aiMessage]);
    }, 1000);

    setInputText('');
    setSelectedImage(null);
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  const handleImageUpload = (e) => {
    const file = e.target.files[0];
    if (file) {
      const imageUrl = URL.createObjectURL(file);
      setSelectedImage(imageUrl);
    }
  };

  if (showSignUp) {
    return <SignUp onBack={() => setShowSignUp(false)} />;
  }

  if (showLogin) {
    return <Login onBack={() => setShowLogin(false)} />;
  }

  if (showProfile) {
    return <Profile onBack={() => setShowProfile(false)} />;
  }

  return (
    <div className="app">
      <header className="header">
        <div className="header-left">
          <img src={logo} alt="ReceiptReveal Logo" className="header-logo" />
          <h1 className="app-name">ReceiptReveal</h1>
        </div>
        <div className="header-right">
          {isLoggedIn ? (
            <>
              <button className="auth-button" onClick={() => setShowProfile(true)}>Profile</button>
              <button className="auth-button" onClick={logout}>Log Out</button>
            </>
          ) : (
            <>
              <button className="auth-button" onClick={() => setShowLogin(true)}>Login</button>
              <button className="auth-button" onClick={() => setShowSignUp(true)}>Sign Up</button>
            </>
          )}
        </div>
      </header>
      <div className="chat-container">
        <div className="chat-box">
          {messages.map((msg, index) => (
            <div className={`chat-message ${msg.isUser ? 'user-message' : 'ai-message'}`} key={index}>
              <div className="message-icon">
                <img src={msg.isUser ? userIcon : leafIcon} alt={msg.isUser ? "User" : "AI"} />
              </div>
              <div className="message-content">
                {msg.text && <p>{msg.text}</p>}
                {msg.image && <img src={msg.image} alt="uploaded" className="chat-image" />}
              </div>
            </div>
          ))}
        </div>
        <div className="input-area">
          <input
            type="text"
            placeholder="Type your message..."
            value={inputText}
            onChange={(e) => setInputText(e.target.value)}
            onKeyPress={handleKeyPress}
          />
          <input type="file" accept="image/*" onChange={handleImageUpload} />
          <button onClick={handleSend}>Send</button>
        </div>
      </div>
    </div>
  );
}

export default App;
