import React, { createContext, useState, useContext, useEffect } from 'react';
import { getAuth, saveAuth, clearAuth } from '../services/auth';

const AuthContext = createContext(null);

export const AuthProvider = ({ children }) => {
  const [teacher, setTeacher] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const { teacher: savedTeacher } = getAuth();
    if (savedTeacher) {
      setTeacher(savedTeacher);
    }
    setLoading(false);
  }, []);

  const login = (token, teacherData) => {
    saveAuth(token, teacherData);
    setTeacher(teacherData);
  };

  const logout = () => {
    clearAuth();
    setTeacher(null);
  };

  if (loading) {
    return <div>Loading...</div>;
  }

  return (
    <AuthContext.Provider value={{ teacher, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => useContext(AuthContext);