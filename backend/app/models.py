from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, LargeBinary, Date, UniqueConstraint, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .database import Base

class Teacher(Base):
    __tablename__ = "teachers"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    name = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)
    photo = Column(LargeBinary, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    classes = relationship("Class", back_populates="teacher", cascade="all, delete-orphan")

class Class(Base):
    __tablename__ = "classes"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    subject = Column(String, nullable=True)
    teacher_id = Column(Integer, ForeignKey("teachers.id", ondelete="CASCADE"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    teacher = relationship("Teacher", back_populates="classes")
    students = relationship("Student", back_populates="class_obj", cascade="all, delete-orphan")
    attendances = relationship("Attendance", back_populates="class_obj", cascade="all, delete-orphan")

class Student(Base):
    __tablename__ = "students"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    roll_number = Column(String, nullable=True)
    class_id = Column(Integer, ForeignKey("classes.id", ondelete="CASCADE"), nullable=False)
    face_embedding = Column(LargeBinary, nullable=True)
    photo = Column(LargeBinary, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    class_obj = relationship("Class", back_populates="students")
    attendances = relationship("Attendance", back_populates="student", cascade="all, delete-orphan")
    
    __table_args__ = (
        UniqueConstraint('roll_number', 'class_id', name='unique_roll_per_class'),
    )

class Attendance(Base):
    __tablename__ = "attendances"
    
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id", ondelete="CASCADE"), nullable=False)
    class_id = Column(Integer, ForeignKey("classes.id", ondelete="CASCADE"), nullable=False)
    date = Column(Date, nullable=False)
    is_present = Column(Boolean, default=False, nullable=False)
    marked_at = Column(DateTime(timezone=True), server_default=func.now())
    
    student = relationship("Student", back_populates="attendances")
    class_obj = relationship("Class", back_populates="attendances")
    
    __table_args__ = (
        UniqueConstraint('student_id', 'date', name='unique_attendance_per_day'),
    )
