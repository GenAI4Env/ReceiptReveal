// src/App.jsx
import React, { useState } from 'react';
import './App.css';
import logo from './assets/RRlogo.png';

function App() {
  const [messages, setMessages] = useState([]);
  const [inputText, setInputText] = useState('');
  const [selectedImage, setSelectedImage] = useState(null);
  const [isLoggedIn, setIsLoggedIn] = useState(false);

  const handleSend = () => {
    if (!inputText && !selectedImage) return;

    const newMessage = {
      text: inputText,
      image: selectedImage,
    };
    setMessages([...messages, newMessage]);
    setInputText('');
    setSelectedImage(null);
  };

  const handleImageUpload = (e) => {
    const file = e.target.files[0];
    if (file) {
      const imageUrl = URL.createObjectURL(file);
      setSelectedImage(imageUrl);
    }
  };

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
              <button className="auth-button">Profile</button>
              <button className="auth-button">Log Out</button>
            </>
          ) : (
            <>
              <button className="auth-button">Login</button>
              <button className="auth-button">Sign Up</button>
            </>
          )}
        </div>
      </header>
      <div className="chat-container">
        <div className="chat-box">
          {messages.map((msg, index) => (
            <div className="chat-message" key={index}>
              {msg.text && <p>{msg.text}</p>}
              {msg.image && <img src={msg.image} alt="uploaded" className="chat-image" />}
            </div>
          ))}
        </div>
        <div className="input-area">
          <input
            type="text"
            placeholder="Type your message..."
            value={inputText}
            onChange={(e) => setInputText(e.target.value)}
          />
          <input type="file" accept="image/*" onChange={handleImageUpload} />
          <button onClick={handleSend}>Send</button>
        </div>
      </div>
    </div>
  );
}

export default App;
