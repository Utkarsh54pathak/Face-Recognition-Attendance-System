import React, { useRef } from 'react';
import Webcam from 'react-webcam';

const WebcamCapture = ({ onCapture, webcamRef }) => {
  const capture = () => {
    const imageSrc = webcamRef.current.getScreenshot();
    onCapture(imageSrc);
  };

  return (
    <div>
      <Webcam
        ref={webcamRef}
        screenshotFormat="image/jpeg"
        className="w-full rounded-lg"
      />
      <button
        onClick={capture}
        className="mt-4 w-full bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700"
      >
        Capture Photo
      </button>
    </div>
  );
};

export default WebcamCapture;