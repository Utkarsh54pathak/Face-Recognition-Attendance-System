from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import date, datetime

# Teacher Schemas
class TeacherCreate(BaseModel):
    email: EmailStr
    name: str
    password: str

class TeacherLogin(BaseModel):
    email: EmailStr
    password: str

class TeacherResponse(BaseModel):
    id: int
    email: str
    name: str
    photo: Optional[str] = None
    
    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str
    teacher: TeacherResponse

# Class Schemas
class ClassCreate(BaseModel):
    name: str
    subject: Optional[str] = None

class ClassUpdate(BaseModel):
    name: Optional[str] = None
    subject: Optional[str] = None

class ClassResponse(BaseModel):
    id: int
    name: str
    subject: Optional[str]
    teacher_id: int
    created_at: datetime
    student_count: Optional[int] = 0
    
    class Config:
        from_attributes = True

# Student Schemas
class StudentCreate(BaseModel):
    name: str
    roll_number: Optional[str] = None
    photo_base64: str

class StudentUpdate(BaseModel):
    name: Optional[str] = None
    roll_number: Optional[str] = None
    photo_base64: Optional[str] = None

class StudentResponse(BaseModel):
    id: int
    name: str
    roll_number: Optional[str]
    class_id: int
    photo: Optional[str] = None
    has_face_data: bool = False
    created_at: datetime
    
    class Config:
        from_attributes = True

# Attendance Schemas
class AttendanceMarkRequest(BaseModel):
    frame_base64: str

class AttendanceMarkResponse(BaseModel):
    date: date
    total_students: int
    present_count: int
    absent_count: int
    present_students: List[StudentResponse]
    absent_students: List[StudentResponse]

class AttendanceResponse(BaseModel):
    id: int
    student_id: int
    student_name: str
    class_id: int
    date: date
    is_present: bool
    marked_at: datetime
    
    class Config:
        from_attributes = True

class AttendanceDateResponse(BaseModel):
    date: date
    total_students: int
    present_count: int
    absent_count: int
    attendances: List[AttendanceResponse]

class AttendanceUpdate(BaseModel):
    is_present: bool
