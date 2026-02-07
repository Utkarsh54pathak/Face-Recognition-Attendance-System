import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { classAPI, studentAPI } from '../../services/api';
import Navbar from '../Common/Navbar';
import StudentList from './StudentList';
import LiveScanner from '../Attendance/LiveScanner';
import AttendanceHistory from '../Attendance/AttendanceHistory';

const ClassDetail = () => {
  const { classId } = useParams();
  const navigate = useNavigate();
  const [classData, setClassData] = useState(null);
  const [students, setStudents] = useState([]);
  const [activeTab, setActiveTab] = useState('students');
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchClassData();
    fetchStudents();
  }, [classId]);

  const fetchClassData = async () => {
    try {
      const response = await classAPI.getOne(classId);
      setClassData(response.data);
    } catch (error) {
      console.error('Error:', error);
    }
  };

  const fetchStudents = async () => {
    try {
      const response = await studentAPI.getAll(classId);
      setStudents(response.data);
    } catch (error) {
      console.error('Error:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-100">
      <Navbar />
      <div className="max-w-7xl mx-auto px-4 py-8">
        <div className="mb-6">
          <button onClick={() => navigate('/dashboard')} className="text-blue-600 hover:text-blue-800 mb-4">
            ← Back to Dashboard
          </button>
          <h1 className="text-3xl font-bold text-gray-900">{classData?.name}</h1>
          {classData?.subject && <p className="text-gray-600">{classData.subject}</p>}
        </div>

        {/* Tabs */}
        <div className="border-b mb-6">
          <nav className="-mb-px flex space-x-8">
            {['students', 'attendance'].map((tab) => (
              <button
                key={tab}
                onClick={() => setActiveTab(tab)}
                className={`py-4 px-1 border-b-2 font-medium text-sm ${
                  activeTab === tab
                    ? 'border-blue-500 text-blue-600'
                    : 'border-transparent text-gray-500 hover:text-gray-700'
                }`}
              >
                {tab.charAt(0).toUpperCase() + tab.slice(1)}
              </button>
            ))}
          </nav>
        </div>

        {/* Tab Content */}
        {loading ? (
          <div className="text-center py-12">
            <div className="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
          </div>
        ) : (
          <>
            {activeTab === 'students' && <StudentList students={students} classId={classId} onRefresh={fetchStudents} />}
            {activeTab === 'attendance' && (
              <div>
                <LiveScanner classId={classId} students={students} />
                <AttendanceHistory classId={classId} />
              </div>
            )}
          </>
        )}
      </div>
    </div>
  );
};

export default ClassDetail;