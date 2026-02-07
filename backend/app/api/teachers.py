from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import base64

from .. import models
from ..database import get_db
from ..dependencies import get_current_teacher

router = APIRouter(prefix="/teachers", tags=["teachers"])

@router.put("/photo")
def update_teacher_photo(
    photo_base64: str,
    current_teacher: models.Teacher = Depends(get_current_teacher),
    db: Session = Depends(get_db)
):
    """Update teacher photo"""
    try:
        if "," in photo_base64:
            photo_base64 = photo_base64.split(",")[1]
        
        photo_bytes = base64.b64decode(photo_base64)
        current_teacher.photo = photo_bytes
        db.commit()
        
        return {"message": "Photo updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to update photo: {str(e)}")
