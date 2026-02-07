import React from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../../contexts/AuthContext';

const Navbar = () => {
  const { teacher, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/');
  };

  return (
    <nav className="bg-white shadow">
      <div className="max-w-7xl mx-auto px-4 py-4">
        <div className="flex justify-between items-center">
          <div className="flex items-center space-x-4">
            {teacher?.photo && (
              <img
                src={`data:image/jpeg;base64,${teacher.photo}`}
                alt={teacher.name}
                className="h-10 w-10 rounded-full"
              />
            )}
            <div>
              <h2 className="font-semibold">{teacher?.name}</h2>
              <p className="text-xs text-gray-600">{teacher?.email}</p>
            </div>
          </div>
          <button
            onClick={handleLogout}
            className="bg-red-600 text-white px-4 py-2 rounded hover:bg-red-700"
          >
            Logout
          </button>
        </div>
      </div>
    </nav>
  );
};

export default Navbar;