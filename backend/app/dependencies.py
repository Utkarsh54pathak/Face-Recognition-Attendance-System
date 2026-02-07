from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from . import models
from .database import get_db
from .security import decode_access_token

security = HTTPBearer()

def get_current_teacher(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> models.Teacher:
    """Get the current authenticated teacher"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    token = credentials.credentials
    payload = decode_access_token(token)
    
    if payload is None:
        raise credentials_exception
    
    teacher_id: int = payload.get("sub")
    if teacher_id is None:
        raise credentials_exception
    
    teacher = db.query(models.Teacher).filter(models.Teacher.id == teacher_id).first()
    if teacher is None:
        raise credentials_exception
    
    return teacher

def verify_class_ownership(class_id: int, teacher: models.Teacher, db: Session):
    """Verify that the teacher owns the class"""
    class_obj = db.query(models.Class).filter(models.Class.id == class_id).first()
    if not class_obj:
        raise HTTPException(status_code=404, detail="Class not found")
    if class_obj.teacher_id != teacher.id:
        raise HTTPException(status_code=403, detail="Not authorized to access this class")
    return class_obj
