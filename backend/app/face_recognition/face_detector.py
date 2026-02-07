import face_recognition
import numpy as np
import base64
from io import BytesIO
from PIL import Image
import cv2

class FaceDetector:
    """Handles face detection in images"""
    
    @staticmethod
    def base64_to_image(base64_string: str) -> np.ndarray:
        """Convert base64 string to numpy array image"""
        try:
            if "," in base64_string:
                base64_string = base64_string.split(",")[1]
            
            image_data = base64.b64decode(base64_string)
            image = Image.open(BytesIO(image_data))
            
            if image.mode != 'RGB':
                image = image.convert('RGB')
            
            return np.array(image)
        except Exception as e:
            raise ValueError(f"Failed to decode base64 image: {str(e)}")
    
    @staticmethod
    def image_to_base64(image: np.ndarray) -> str:
        """Convert numpy array image to base64 string"""
        try:
            pil_image = Image.fromarray(image)
            buffered = BytesIO()
            pil_image.save(buffered, format="JPEG")
            return base64.b64encode(buffered.getvalue()).decode()
        except Exception as e:
            raise ValueError(f"Failed to encode image to base64: {str(e)}")
    
    @staticmethod
    def detect_faces(image: np.ndarray, model: str = "hog"):
        """
        Detect faces in an image
        
        Args:
            image: numpy array image
            model: "hog" (faster, CPU) or "cnn" (more accurate, GPU)
        
        Returns:
            List of face locations [(top, right, bottom, left), ...]
        """
        return face_recognition.face_locations(image, model=model)
    
    @staticmethod
    def detect_single_face(base64_image: str):
        """
        Detect a single face in a base64 image
        
        Returns:
            Tuple of (face_location, face_image)
        """
        image = FaceDetector.base64_to_image(base64_image)
        face_locations = FaceDetector.detect_faces(image)
        
        if len(face_locations) == 0:
            raise ValueError("No face detected in the image")
        
        if len(face_locations) > 1:
            raise ValueError("Multiple faces detected. Please ensure only one face is in the frame")
        
        top, right, bottom, left = face_locations[0]
        face_image = image[top:bottom, left:right]
        
        return face_locations[0], face_image
    
    @staticmethod
    def detect_multiple_faces(base64_frame: str):
        """
        Detect multiple faces in a frame
        
        Returns:
            List of face locations
        """
        image = FaceDetector.base64_to_image(base64_frame)
        
        # Resize for faster processing
        small_frame = cv2.resize(image, (0, 0), fx=0.5, fy=0.5)
        
        return face_recognition.face_locations(small_frame)
    
    @staticmethod
    def verify_face_quality(base64_image: str) -> dict:
        """
        Verify if the image has good quality for face recognition
        
        Returns:
            dict with 'valid' and 'message' keys
        """
        image = FaceDetector.base64_to_image(base64_image)
        
        height, width = image.shape[:2]
        if width < 200 or height < 200:
            return {
                "valid": False,
                "message": "Image resolution too low. Please ensure good lighting and camera quality."
            }
        
        face_locations = FaceDetector.detect_faces(image)
        
        if len(face_locations) == 0:
            return {
                "valid": False,
                "message": "No face detected. Please ensure your face is clearly visible."
            }
        
        if len(face_locations) > 1:
            return {
                "valid": False,
                "message": "Multiple faces detected. Only one person should be in frame."
            }
        
        top, right, bottom, left = face_locations[0]
        face_width = right - left
        face_height = bottom - top
        
        if face_width < 80 or face_height < 80:
            return {
                "valid": False,
                "message": "Face too small. Please move closer to the camera."
            }
        
        return {
            "valid": True,
            "message": "Face quality is good"
        }
