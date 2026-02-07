from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from datetime import date, datetime
import base64

from .. import models, schemas
from ..database import get_db
from ..dependencies import get_current_teacher, verify_class_ownership
from ..face_recognition import FaceEncoder, FaceMatcher

router = APIRouter(prefix="/attendance", tags=["attendance"])

@router.post("/class/{class_id}/mark", response_model=schemas.AttendanceMarkResponse)
def mark_attendance(
    class_id: int,
    request: schemas.AttendanceMarkRequest,
    current_teacher: models.Teacher = Depends(get_current_teacher),
    db: Session = Depends(get_db)
):
    """Mark attendance using face recognition from webcam frame"""
    verify_class_ownership(class_id, current_teacher, db)
    
    # Get all students with face embeddings
    students = db.query(models.Student).filter(
        models.Student.class_id == class_id,
        models.Student.face_embedding.isnot(None)
    ).all()
    
    if not students:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No students with registered faces in this class"
        )
    
    # Detect faces in the frame
    try:
        detected_encodings = FaceEncoder.generate_encodings_from_frame(request.frame_base64)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to process frame: {str(e)}"
        )
    
    # Prepare known embeddings
    known_embeddings = []
    for student in students:
        embedding = FaceEncoder.bytes_to_encoding(student.face_embedding)
        known_embeddings.append((student.id, embedding))
    
    # Match faces
    present_student_ids = FaceMatcher.match_faces(detected_encodings, known_embeddings)
    
    # Get today's date
    today = date.today()
    
    # Mark attendance
    present_students = []
    absent_students = []
    
    for student in students:
        is_present = student.id in present_student_ids
        
        # Check existing attendance
        existing_attendance = db.query(models.Attendance).filter(
            models.Attendance.student_id == student.id,
            models.Attendance.date == today
        ).first()
        
        if existing_attendance:
            existing_attendance.is_present = is_present
            existing_attendance.marked_at = datetime.utcnow()
        else:
            attendance = models.Attendance(
                student_id=student.id,
                class_id=class_id,
                date=today,
                is_present=is_present
            )
            db.add(attendance)
        
        # Prepare response
        photo_base64 = None
        if student.photo:
            photo_base64 = base64.b64encode(student.photo).decode()
        
        student_response = schemas.StudentResponse(
            id=student.id,
            name=student.name,
            roll_number=student.roll_number,
            class_id=student.class_id,
            photo=photo_base64,
            has_face_data=True,
            created_at=student.created_at
        )
        
        if is_present:
            present_students.append(student_response)
        else:
            absent_students.append(student_response)
    
    db.commit()
    
    return schemas.AttendanceMarkResponse(
        date=today,
        total_students=len(students),
        present_count=len(present_students),
        absent_count=len(absent_students),
        present_students=present_students,
        absent_students=absent_students
    )

@router.get("/class/{class_id}/history", response_model=List[schemas.AttendanceDateResponse])
def get_attendance_history(
    class_id: int,
    current_teacher: models.Teacher = Depends(get_current_teacher),
    db: Session = Depends(get_db)
):
    """Get attendance history for a class"""
    verify_class_ownership(class_id, current_teacher, db)
    
    attendance_dates = db.query(models.Attendance.date).filter(
        models.Attendance.class_id == class_id
    ).distinct().order_by(models.Attendance.date.desc()).all()
    
    response = []
    for (attendance_date,) in attendance_dates:
        attendances = db.query(models.Attendance).filter(
            models.Attendance.class_id == class_id,
            models.Attendance.date == attendance_date
        ).all()
        
        attendance_records = []
        present_count = 0
        
        for attendance in attendances:
            student = db.query(models.Student).filter(
                models.Student.id == attendance.student_id
            ).first()
            
            if attendance.is_present:
                present_count += 1
            
            attendance_records.append(schemas.AttendanceResponse(
                id=attendance.id,
                student_id=attendance.student_id,
                student_name=student.name if student else "Unknown",
                class_id=attendance.class_id,
                date=attendance.date,
                is_present=attendance.is_present,
                marked_at=attendance.marked_at
            ))
        
        response.append(schemas.AttendanceDateResponse(
            date=attendance_date,
            total_students=len(attendances),
            present_count=present_count,
            absent_count=len(attendances) - present_count,
            attendances=attendance_records
        ))
    
    return response

@router.put("/{attendance_id}", response_model=schemas.AttendanceResponse)
def update_attendance(
    attendance_id: int,
    update_data: schemas.AttendanceUpdate,
    current_teacher: models.Teacher = Depends(get_current_teacher),
    db: Session = Depends(get_db)
):
    """Update an attendance record"""
    attendance = db.query(models.Attendance).filter(
        models.Attendance.id == attendance_id
    ).first()
    
    if not attendance:
        raise HTTPException(status_code=404, detail="Attendance record not found")
    
    verify_class_ownership(attendance.class_id, current_teacher, db)
    
    attendance.is_present = update_data.is_present
    attendance.marked_at = datetime.utcnow()
    
    db.commit()
    db.refresh(attendance)
    
    student = db.query(models.Student).filter(
        models.Student.id == attendance.student_id
    ).first()
    
    return schemas.AttendanceResponse(
        id=attendance.id,
        student_id=attendance.student_id,
        student_name=student.name if student else "Unknown",
        class_id=attendance.class_id,
        date=attendance.date,
        is_present=attendance.is_present,
        marked_at=attendance.marked_at
    )

@router.delete("/{attendance_id}")
def delete_attendance(
    attendance_id: int,
    current_teacher: models.Teacher = Depends(get_current_teacher),
    db: Session = Depends(get_db)
):
    """Delete an attendance record"""
    attendance = db.query(models.Attendance).filter(
        models.Attendance.id == attendance_id
    ).first()
    
    if not attendance:
        raise HTTPException(status_code=404, detail="Attendance record not found")
    
    verify_class_ownership(attendance.class_id, current_teacher, db)
    
    db.delete(attendance)
    db.commit()
    
    return {"message": "Attendance record deleted successfully"}
