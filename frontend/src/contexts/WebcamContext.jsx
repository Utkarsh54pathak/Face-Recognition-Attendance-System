import React, { createContext, useContext, useRef } from 'react';

const WebcamContext = createContext(null);

export const WebcamProvider = ({ children }) => {
  const webcamRef = useRef(null);

  const capture = () => {
    if (webcamRef.current) {
      return webcamRef.current.getScreenshot();
    }
    return null;
  };

  return (
    <WebcamContext.Provider value={{ webcamRef, capture }}>
      {children}
    </WebcamContext.Provider>
  );
};

export const useWebcam = () => useContext(WebcamContext);