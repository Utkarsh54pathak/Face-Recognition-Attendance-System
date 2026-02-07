import face_recognition
import numpy as np
from .face_detector import FaceDetector

class FaceEncoder:
    """Handles face encoding (embedding generation)"""
    
    @staticmethod
    def generate_encoding(base64_image: str):
        """
        Generate face encoding from base64 image
        
        Returns:
            Tuple of (encoding, face_image)
        """
        image = FaceDetector.base64_to_image(base64_image)
        face_locations = face_recognition.face_locations(image)
        
        if len(face_locations) == 0:
            raise ValueError("No face detected")
        
        if len(face_locations) > 1:
            raise ValueError("Multiple faces detected")
        
        encodings = face_recognition.face_encodings(image, face_locations)
        
        if len(encodings) == 0:
            raise ValueError("Could not generate face encoding")
        
        # Extract face region
        top, right, bottom, left = face_locations[0]
        face_image = image[top:bottom, left:right]
        
        return encodings[0], face_image
    
    @staticmethod
    def generate_encodings_from_frame(base64_frame: str):
        """
        Generate encodings for all faces in a frame
        
        Returns:
            List of encodings
        """
        image = FaceDetector.base64_to_image(base64_frame)
        
        # Resize for faster processing
        import cv2
        small_frame = cv2.resize(image, (0, 0), fx=0.5, fy=0.5)
        
        face_locations = face_recognition.face_locations(small_frame)
        
        if len(face_locations) == 0:
            return []
        
        encodings = face_recognition.face_encodings(small_frame, face_locations)
        return encodings
    
    @staticmethod
    def encoding_to_bytes(encoding: np.ndarray) -> bytes:
        """Convert numpy encoding to bytes for storage"""
        return encoding.tobytes()
    
    @staticmethod
    def bytes_to_encoding(encoding_bytes: bytes) -> np.ndarray:
        """Convert bytes back to numpy encoding"""
        return np.frombuffer(encoding_bytes, dtype=np.float64)
