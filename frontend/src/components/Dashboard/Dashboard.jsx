import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { classAPI } from '../../services/api';
import Navbar from '../Common/Navbar';
import ClassCard from './ClassCard';
import CreateClassModal from './CreateClassModal';

const Dashboard = () => {
  const navigate = useNavigate();
  const [classes, setClasses] = useState([]);
  const [searchTerm, setSearchTerm] = useState('');
  const [loading, setLoading] = useState(true);
  const [showModal, setShowModal] = useState(false);

  useEffect(() => {
    fetchClasses();
  }, []);

  const fetchClasses = async (search = '') => {
    try {
      const response = await classAPI.getAll(search);
      setClasses(response.data);
    } catch (error) {
      console.error('Error fetching classes:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleSearch = (value) => {
    setSearchTerm(value);
    fetchClasses(value);
  };

  return (
    <div className="min-h-screen bg-gray-100">
      <Navbar />
      <div className="max-w-7xl mx-auto px-4 py-8">
        <div className="mb-6 flex gap-4">
          <input
            type="text"
            placeholder="Search classes..."
            className="flex-1 px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500"
            value={searchTerm}
            onChange={(e) => handleSearch(e.target.value)}
          />
          <button
            onClick={() => setShowModal(true)}
            className="bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700"
          >
            Create Class
          </button>
        </div>

        {loading ? (
          <div className="text-center py-12">
            <div className="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
          </div>
        ) : classes.length === 0 ? (
          <div className="text-center py-12 bg-white rounded-lg shadow">
            <h3 className="text-lg font-medium text-gray-900">No classes found</h3>
            <p className="text-sm text-gray-500 mt-1">Create your first class to get started</p>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {classes.map((cls) => (
              <ClassCard key={cls.id} classData={cls} onClick={() => navigate(`/class/${cls.id}`)} />
            ))}
          </div>
        )}

        {showModal && (
          <CreateClassModal
            onClose={() => setShowModal(false)}
            onSuccess={() => {
              setShowModal(false);
              fetchClasses(searchTerm);
            }}
          />
        )}
      </div>
    </div>
  );
};

export default Dashboard;