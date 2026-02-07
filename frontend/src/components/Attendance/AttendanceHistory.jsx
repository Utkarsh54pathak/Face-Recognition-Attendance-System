import React, { useState, useEffect } from 'react';
import { attendanceAPI } from '../../services/api';

const AttendanceHistory = ({ classId }) => {
  const [history, setHistory] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchHistory();
  }, [classId]);

  const fetchHistory = async () => {
    try {
      const response = await attendanceAPI.getHistory(classId);
      setHistory(response.data);
    } catch (error) {
      console.error('Error:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return <div className="text-center py-4">Loading history...</div>;
  }

  return (
    <div className="bg-white rounded-lg shadow p-6">
      <h3 className="text-lg font-semibold mb-4">Attendance History</h3>

      {history.length === 0 ? (
        <p className="text-gray-600">No attendance records yet</p>
      ) : (
        <div className="space-y-2">
          {history.map((record) => {
            const percentage = Math.round((record.present_count / record.total_students) * 100);
            return (
              <div key={record.date} className="border-b py-3 flex justify-between items-center">
                <div>
                  <p className="font-semibold">{new Date(record.date).toLocaleDateString()}</p>
                  <p className="text-sm text-gray-600">
                    Present: {record.present_count} / {record.total_students}
                  </p>
                </div>
                <div className="text-right">
                  <p className={`text-2xl font-bold ${percentage >= 75 ? 'text-green-600' : 'text-red-600'}`}>
                    {percentage}%
                  </p>
                </div>
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
};

export default AttendanceHistory;