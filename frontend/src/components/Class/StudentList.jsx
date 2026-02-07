import React, { useState } from 'react';
import AddStudentModal from './AddStudentModal';
import { studentAPI } from '../../services/api';

const StudentList = ({ students, classId, onRefresh }) => {
  const [showAddModal, setShowAddModal] = useState(false);

  const handleDelete = async (studentId) => {
    if (window.confirm('Delete this student?')) {
      try {
        await studentAPI.delete(studentId);
        onRefresh();
      } catch (error) {
        alert('Error deleting student');
      }
    }
  };

  return (
    <div>
      <div className="flex justify-between mb-6">
        <h2 className="text-xl font-semibold">Students ({students.length})</h2>
        <button
          onClick={() => setShowAddModal(true)}
          className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700"
        >
          + Add Student
        </button>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {students.map((student) => (
          <div key={student.id} className="bg-white rounded-lg shadow p-4">
            <div className="flex items-start space-x-4">
              {student.photo && (
                <img src={`data:image/jpeg;base64,${student.photo}`} alt={student.name} className="w-16 h-16 rounded-full object-cover" />
              )}
              <div className="flex-1">
                <h3 className="font-semibold">{student.name}</h3>
                {student.roll_number && <p className="text-sm text-gray-600">Roll: {student.roll_number}</p>}
                <p className="text-xs text-gray-500 mt-1">{student.has_face_data ? '✓ Face registered' : '⚠ No face'}</p>
              </div>
              <button onClick={() => handleDelete(student.id)} className="text-red-600 hover:text-red-800">
                🗑️
              </button>
            </div>
          </div>
        ))}
      </div>

      {showAddModal && (
        <AddStudentModal
          classId={classId}
          onClose={() => setShowAddModal(false)}
          onSuccess={() => {
            setShowAddModal(false);
            onRefresh();
          }}
        />
      )}
    </div>
  );
};

export default StudentList;