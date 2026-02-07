import React from 'react';

const AttendanceResults = ({ result, onTakeAnother }) => {
  const percentage = Math.round((result.present_count / result.total_students) * 100);

  return (
    <div className="space-y-4">
      {/* Summary Cards */}
      <div className="grid grid-cols-3 gap-4">
        <div className="bg-blue-100 p-4 rounded-lg text-center">
          <p className="text-3xl font-bold text-blue-600">{result.total_students}</p>
          <p className="text-sm text-gray-600">Total</p>
        </div>
        <div className="bg-green-100 p-4 rounded-lg text-center">
          <p className="text-3xl font-bold text-green-600">{result.present_count}</p>
          <p className="text-sm text-gray-600">Present</p>
        </div>
        <div className="bg-red-100 p-4 rounded-lg text-center">
          <p className="text-3xl font-bold text-red-600">{result.absent_count}</p>
          <p className="text-sm text-gray-600">Absent</p>
        </div>
      </div>

      {/* Percentage */}
      <div className="bg-gray-50 p-4 rounded-lg text-center">
        <p className="text-4xl font-bold text-gray-800">{percentage}%</p>
        <p className="text-sm text-gray-600">Attendance Rate</p>
      </div>

      {/* Present Students */}
      {result.present_students.length > 0 && (
        <div>
          <h4 className="font-semibold text-green-600 mb-2">✓ Present ({result.present_count})</h4>
          <div className="grid grid-cols-2 gap-2">
            {result.present_students.map((student) => (
              <div key={student.id} className="bg-green-50 border border-green-200 p-2 rounded">
                <p className="font-medium">{student.name}</p>
                {student.roll_number && <p className="text-xs text-gray-600">{student.roll_number}</p>}
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Absent Students */}
      {result.absent_students.length > 0 && (
        <div>
          <h4 className="font-semibold text-red-600 mb-2">✗ Absent ({result.absent_count})</h4>
          <div className="grid grid-cols-2 gap-2">
            {result.absent_students.map((student) => (
              <div key={student.id} className="bg-red-50 border border-red-200 p-2 rounded">
                <p className="font-medium">{student.name}</p>
                {student.roll_number && <p className="text-xs text-gray-600">{student.roll_number}</p>}
              </div>
            ))}
          </div>
        </div>
      )}

      <button
        onClick={onTakeAnother}
        className="w-full bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700"
      >
        Take Another Attendance
      </button>
    </div>
  );
};

export default AttendanceResults;