import React, { useState, useRef } from 'react';
import Webcam from 'react-webcam';
import { attendanceAPI } from '../../services/api';
import AttendanceResults from './AttendanceResults';

const LiveScanner = ({ classId, students }) => {
  const webcamRef = useRef(null);
  const [scanning, setScanning] = useState(false);
  const [countdown, setCountdown] = useState(3);
  const [result, setResult] = useState(null);

  const handleScan = () => {
    setScanning(true);
    setCountdown(3);
    setResult(null);

    // Countdown timer
    const countdownInterval = setInterval(() => {
      setCountdown((prev) => {
        if (prev <= 1) {
          clearInterval(countdownInterval);
          return 0;
        }
        return prev - 1;
      });
    }, 1000);

    // Capture after 3 seconds
    setTimeout(async () => {
      try {
        const imageSrc = webcamRef.current.getScreenshot();
        const response = await attendanceAPI.mark(classId, { frame_base64: imageSrc });
        setResult(response.data);
      } catch (error) {
        alert('Error marking attendance: ' + (error.response?.data?.detail || error.message));
      } finally {
        setScanning(false);
      }
    }, 3000);
  };

  if (students.length === 0) {
    return (
      <div className="bg-yellow-100 border border-yellow-400 text-yellow-700 px-4 py-3 rounded mb-6">
        No students with registered faces. Please add students first.
      </div>
    );
  }

  return (
    <div className="bg-white rounded-lg shadow p-6 mb-6">
      <h3 className="text-lg font-semibold mb-4">Take Attendance</h3>

      {!result && (
        <div>
          <Webcam ref={webcamRef} screenshotFormat="image/jpeg" className="w-full max-w-2xl mx-auto rounded-lg" />

          {scanning ? (
            <div className="mt-4 text-center">
              <div className="text-6xl font-bold text-blue-600 animate-pulse">{countdown || 'Scanning...'}</div>
              <p className="text-gray-600 mt-2">Position all students in view</p>
            </div>
          ) : (
            <button
              onClick={handleScan}
              className="mt-4 w-full max-w-2xl mx-auto block bg-green-600 text-white px-6 py-3 rounded-lg hover:bg-green-700 text-lg font-semibold"
            >
              🎯 Start 3-Second Scan
            </button>
          )}
        </div>
      )}

      {result && <AttendanceResults result={result} onTakeAnother={() => setResult(null)} />}
    </div>
  );
};

export default LiveScanner;