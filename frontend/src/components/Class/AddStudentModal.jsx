import React, { useState, useRef } from 'react';
import Webcam from 'react-webcam';
import { studentAPI } from '../../services/api';

const AddStudentModal = ({ classId, onClose, onSuccess }) => {
  const webcamRef = useRef(null);
  const [formData, setFormData] = useState({ name: '', roll_number: '' });
  const [showWebcam, setShowWebcam] = useState(false);
  const [capturedImage, setCapturedImage] = useState(null);
  const [loading, setLoading] = useState(false);

  const capture = () => {
    const imageSrc = webcamRef.current.getScreenshot();
    setCapturedImage(imageSrc);
    setShowWebcam(false);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!capturedImage) {
      alert('Please capture a photo');
      return;
    }

    setLoading(true);
    try {
      await studentAPI.create(classId, { ...formData, photo_base64: capturedImage });
      onSuccess();
    } catch (error) {
      alert(error.response?.data?.detail || 'Error adding student');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
      <div className="bg-white rounded-lg p-6 w-full max-w-md max-h-screen overflow-y-auto">
        <h2 className="text-2xl font-bold mb-4">Add New Student</h2>
        <form onSubmit={handleSubmit}>
          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium mb-2">Name *</label>
              <input
                type="text"
                required
                className="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500"
                value={formData.name}
                onChange={(e) => setFormData({ ...formData, name: e.target.value })}
              />
            </div>
            <div>
              <label className="block text-sm font-medium mb-2">Roll Number</label>
              <input
                type="text"
                className="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500"
                value={formData.roll_number}
                onChange={(e) => setFormData({ ...formData, roll_number: e.target.value })}
              />
            </div>
            <div>
              <label className="block text-sm font-medium mb-2">Photo *</label>
              {!showWebcam && !capturedImage && (
                <button
                  type="button"
                  onClick={() => setShowWebcam(true)}
                  className="w-full bg-gray-100 border-2 border-dashed border-gray-300 rounded-lg py-8 hover:bg-gray-200"
                >
                  📷 Capture Photo
                </button>
              )}
              {showWebcam && (
                <div>
                  <Webcam ref={webcamRef} screenshotFormat="image/jpeg" className="w-full rounded-lg mb-2" />
                  <button type="button" onClick={capture} className="w-full bg-blue-600 text-white px-4 py-2 rounded-lg">
                    Capture
                  </button>
                </div>
              )}
              {capturedImage && (
                <div className="relative">
                  <img src={capturedImage} alt="Captured" className="w-full rounded-lg" />
                  <button
                    type="button"
                    onClick={() => { setCapturedImage(null); setShowWebcam(true); }}
                    className="absolute top-2 right-2 bg-red-600 text-white p-2 rounded-full"
                  >
                    ✕
                  </button>
                </div>
              )}
            </div>
          </div>
          <div className="mt-6 flex space-x-3">
            <button type="button" onClick={onClose} className="flex-1 px-4 py-2 border rounded-lg hover:bg-gray-50">
              Cancel
            </button>
            <button type="submit" disabled={loading} className="flex-1 bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 disabled:bg-gray-400">
              {loading ? 'Adding...' : 'Add Student'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default AddStudentModal;