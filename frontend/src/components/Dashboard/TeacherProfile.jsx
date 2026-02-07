import React from 'react';
import { useAuth } from '../../contexts/AuthContext';

const TeacherProfile = () => {
  const { teacher } = useAuth();
  
  return (
    <div className="bg-white rounded-lg shadow p-6">
      <div className="flex items-center space-x-4">
        {teacher?.photo && (
          <img src={`data:image/jpeg;base64,${teacher.photo}`} alt={teacher.name} className="h-16 w-16 rounded-full" />
        )}
        <div>
          <h2 className="text-xl font-semibold">{teacher?.name}</h2>
          <p className="text-gray-600">{teacher?.email}</p>
        </div>
      </div>
    </div>
  );
};

export default TeacherProfile;