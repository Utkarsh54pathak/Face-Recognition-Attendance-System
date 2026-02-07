import face_recognition
import numpy as np
from typing import List, Tuple
from ..config import settings

class FaceMatcher:
    """Handles face matching and recognition"""
    
    @staticmethod
    def match_faces(
        detected_encodings: List[np.ndarray],
        known_encodings: List[Tuple[int, np.ndarray]],
        tolerance: float = None
    ) -> List[int]:
        """
        Match detected face encodings against known encodings
        
        Args:
            detected_encodings: List of detected face encodings
            known_encodings: List of tuples (student_id, encoding)
            tolerance: Distance threshold (default from config)
        
        Returns:
            List of matched student IDs
        """
        if tolerance is None:
            tolerance = settings.FACE_MATCH_TOLERANCE
        
        matched_student_ids = []
        
        for detected_encoding in detected_encodings:
            for student_id, known_encoding in known_encodings:
                # Calculate face distance
                distance = face_recognition.face_distance(
                    [known_encoding], 
                    detected_encoding
                )[0]
                
                if distance <= tolerance:
                    if student_id not in matched_student_ids:
                        matched_student_ids.append(student_id)
                    break
        
        return matched_student_ids
    
    @staticmethod
    def compare_faces(
        known_encoding: np.ndarray,
        test_encoding: np.ndarray,
        tolerance: float = None
    ) -> bool:
        """
        Compare two face encodings
        
        Returns:
            True if faces match, False otherwise
        """
        if tolerance is None:
            tolerance = settings.FACE_MATCH_TOLERANCE
        
        distance = face_recognition.face_distance(
            [known_encoding], 
            test_encoding
        )[0]
        
        return distance <= tolerance
    
    @staticmethod
    def get_face_distance(
        encoding1: np.ndarray,
        encoding2: np.ndarray
    ) -> float:
        """
        Calculate distance between two face encodings
        
        Returns:
            Float distance (lower is better match)
        """
        return face_recognition.face_distance([encoding1], encoding2)[0]
