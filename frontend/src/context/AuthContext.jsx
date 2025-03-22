import React, { createContext, useContext, useState, useEffect } from 'react';
import { dbService } from '../services/dbService';

const AuthContext = createContext(null);

export const AuthProvider = ({ children }) => {
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [user, setUser] = useState(null);
  const [error, setError] = useState('');

  useEffect(() => {
    // Check for existing user session
    const storedUser = localStorage.getItem('user');
    if (storedUser) {
      const userData = JSON.parse(storedUser);
      setUser(userData);
      setIsLoggedIn(true);
    }
  }, []);

  const login = async (username, password) => {
    try {
      const userData = await dbService.verifyUser(username, password);
      if (userData) {
        setUser(userData);
        setIsLoggedIn(true);
        localStorage.setItem('user', JSON.stringify(userData));
        setError('');
        return true;
      }
      setError('Invalid username or password');
      return false;
    } catch (err) {
      setError(err.message);
      return false;
    }
  };

  const logout = () => {
    setUser(null);
    setIsLoggedIn(false);
    localStorage.removeItem('user');
    setError('');
  };

  const signup = async (username, password) => {
    try {
      const userData = await dbService.addUser(username, password);
      if (userData) {
        setUser(userData);
        setIsLoggedIn(true);
        localStorage.setItem('user', JSON.stringify(userData));
        setError('');
        return true;
      }
      setError('Username already exists');
      return false;
    } catch (err) {
      setError(err.message);
      return false;
    }
  };

  return (
    <AuthContext.Provider value={{ isLoggedIn, user, error, login, logout, signup }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
}; 