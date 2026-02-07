from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from .. import models, schemas
from ..database import get_db
from ..dependencies import get_current_teacher

router = APIRouter(prefix="/classes", tags=["classes"])

@router.post("", response_model=schemas.ClassResponse)
def create_class(
    class_data: schemas.ClassCreate,
    current_teacher: models.Teacher = Depends(get_current_teacher),
    db: Session = Depends(get_db)
):
    """Create a new class"""
    db_class = models.Class(
        name=class_data.name,
        subject=class_data.subject,
        teacher_id=current_teacher.id
    )
    
    db.add(db_class)
    db.commit()
    db.refresh(db_class)
    
    return schemas.ClassResponse(
        id=db_class.id,
        name=db_class.name,
        subject=db_class.subject,
        teacher_id=db_class.teacher_id,
        created_at=db_class.created_at,
        student_count=0
    )

@router.get("", response_model=List[schemas.ClassResponse])
def get_classes(
    search: str = "",
    current_teacher: models.Teacher = Depends(get_current_teacher),
    db: Session = Depends(get_db)
):
    """Get all classes for current teacher"""
    query = db.query(models.Class).filter(
        models.Class.teacher_id == current_teacher.id
    )
    
    if search:
        query = query.filter(
            models.Class.name.ilike(f"%{search}%") |
            models.Class.subject.ilike(f"%{search}%")
        )
    
    classes = query.all()
    
    response = []
    for class_obj in classes:
        student_count = db.query(models.Student).filter(
            models.Student.class_id == class_obj.id
        ).count()
        
        response.append(schemas.ClassResponse(
            id=class_obj.id,
            name=class_obj.name,
            subject=class_obj.subject,
            teacher_id=class_obj.teacher_id,
            created_at=class_obj.created_at,
            student_count=student_count
        ))
    
    return response

@router.get("/{class_id}", response_model=schemas.ClassResponse)
def get_class(
    class_id: int,
    current_teacher: models.Teacher = Depends(get_current_teacher),
    db: Session = Depends(get_db)
):
    """Get a specific class"""
    class_obj = db.query(models.Class).filter(
        models.Class.id == class_id,
        models.Class.teacher_id == current_teacher.id
    ).first()
    
    if not class_obj:
        raise HTTPException(status_code=404, detail="Class not found")
    
    student_count = db.query(models.Student).filter(
        models.Student.class_id == class_obj.id
    ).count()
    
    return schemas.ClassResponse(
        id=class_obj.id,
        name=class_obj.name,
        subject=class_obj.subject,
        teacher_id=class_obj.teacher_id,
        created_at=class_obj.created_at,
        student_count=student_count
    )

@router.put("/{class_id}", response_model=schemas.ClassResponse)
def update_class(
    class_id: int,
    class_data: schemas.ClassUpdate,
    current_teacher: models.Teacher = Depends(get_current_teacher),
    db: Session = Depends(get_db)
):
    """Update a class"""
    class_obj = db.query(models.Class).filter(
        models.Class.id == class_id,
        models.Class.teacher_id == current_teacher.id
    ).first()
    
    if not class_obj:
        raise HTTPException(status_code=404, detail="Class not found")
    
    if class_data.name is not None:
        class_obj.name = class_data.name
    if class_data.subject is not None:
        class_obj.subject = class_data.subject
    
    db.commit()
    db.refresh(class_obj)
    
    student_count = db.query(models.Student).filter(
        models.Student.class_id == class_obj.id
    ).count()
    
    return schemas.ClassResponse(
        id=class_obj.id,
        name=class_obj.name,
        subject=class_obj.subject,
        teacher_id=class_obj.teacher_id,
        created_at=class_obj.created_at,
        student_count=student_count
    )

@router.delete("/{class_id}")
def delete_class(
    class_id: int,
    current_teacher: models.Teacher = Depends(get_current_teacher),
    db: Session = Depends(get_db)
):
    """Delete a class"""
    class_obj = db.query(models.Class).filter(
        models.Class.id == class_id,
        models.Class.teacher_id == current_teacher.id
    ).first()
    
    if not class_obj:
        raise HTTPException(status_code=404, detail="Class not found")
    
    db.delete(class_obj)
    db.commit()
    
    return {"message": "Class deleted successfully"}
