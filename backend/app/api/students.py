from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
import base64

from .. import models, schemas
from ..database import get_db
from ..dependencies import get_current_teacher, verify_class_ownership
from ..face_recognition import FaceDetector, FaceEncoder

router = APIRouter(prefix="/students", tags=["students"])

@router.post("/class/{class_id}", response_model=schemas.StudentResponse)
def create_student(
    class_id: int,
    student_data: schemas.StudentCreate,
    current_teacher: models.Teacher = Depends(get_current_teacher),
    db: Session = Depends(get_db)
):
    """Enroll a new student with face recognition"""
    verify_class_ownership(class_id, current_teacher, db)
    
    # Verify face quality
    quality_check = FaceDetector.verify_face_quality(student_data.photo_base64)
    if not quality_check["valid"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=quality_check["message"]
        )
    
    # Generate face embedding
    try:
        embedding, face_image = FaceEncoder.generate_encoding(student_data.photo_base64)
        embedding_bytes = FaceEncoder.encoding_to_bytes(embedding)
        face_image_bytes = face_image.tobytes()
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    
    # Create student
    db_student = models.Student(
        name=student_data.name,
        roll_number=student_data.roll_number,
        class_id=class_id,
        face_embedding=embedding_bytes,
        photo=face_image_bytes
    )
    
    try:
        db.add(db_student)
        db.commit()
        db.refresh(db_student)
    except Exception as e:
        db.rollback()
        if "unique_roll_per_class" in str(e):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Roll number already exists in this class"
            )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create student"
        )
    
    photo_base64 = None
    if db_student.photo:
        photo_base64 = FaceDetector.image_to_base64(face_image)
    
    return schemas.StudentResponse(
        id=db_student.id,
        name=db_student.name,
        roll_number=db_student.roll_number,
        class_id=db_student.class_id,
        photo=photo_base64,
        has_face_data=db_student.face_embedding is not None,
        created_at=db_student.created_at
    )

@router.get("/class/{class_id}", response_model=List[schemas.StudentResponse])
def get_students(
    class_id: int,
    current_teacher: models.Teacher = Depends(get_current_teacher),
    db: Session = Depends(get_db)
):
    """Get all students in a class"""
    verify_class_ownership(class_id, current_teacher, db)
    
    students = db.query(models.Student).filter(
        models.Student.class_id == class_id
    ).all()
    
    response = []
    for student in students:
        photo_base64 = None
        if student.photo:
            try:
                photo_base64 = base64.b64encode(student.photo).decode()
            except:
                pass
        
        response.append(schemas.StudentResponse(
            id=student.id,
            name=student.name,
            roll_number=student.roll_number,
            class_id=student.class_id,
            photo=photo_base64,
            has_face_data=student.face_embedding is not None,
            created_at=student.created_at
        ))
    
    return response

@router.put("/{student_id}", response_model=schemas.StudentResponse)
def update_student(
    student_id: int,
    student_data: schemas.StudentUpdate,
    current_teacher: models.Teacher = Depends(get_current_teacher),
    db: Session = Depends(get_db)
):
    """Update a student"""
    student = db.query(models.Student).filter(
        models.Student.id == student_id
    ).first()
    
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    
    verify_class_ownership(student.class_id, current_teacher, db)
    
    if student_data.name is not None:
        student.name = student_data.name
    if student_data.roll_number is not None:
        student.roll_number = student_data.roll_number
    
    if student_data.photo_base64:
        quality_check = FaceDetector.verify_face_quality(student_data.photo_base64)
        if not quality_check["valid"]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=quality_check["message"]
            )
        
        try:
            embedding, face_image = FaceEncoder.generate_encoding(student_data.photo_base64)
            student.face_embedding = FaceEncoder.encoding_to_bytes(embedding)
            student.photo = face_image.tobytes()
        except ValueError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )
    
    db.commit()
    db.refresh(student)
    
    photo_base64 = None
    if student.photo:
        photo_base64 = base64.b64encode(student.photo).decode()
    
    return schemas.StudentResponse(
        id=student.id,
        name=student.name,
        roll_number=student.roll_number,
        class_id=student.class_id,
        photo=photo_base64,
        has_face_data=student.face_embedding is not None,
        created_at=student.created_at
    )

@router.delete("/{student_id}")
def delete_student(
    student_id: int,
    current_teacher: models.Teacher = Depends(get_current_teacher),
    db: Session = Depends(get_db)
):
    """Delete a student"""
    student = db.query(models.Student).filter(
        models.Student.id == student_id
    ).first()
    
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    
    verify_class_ownership(student.class_id, current_teacher, db)
    
    db.delete(student)
    db.commit()
    
    return {"message": "Student deleted successfully"}
