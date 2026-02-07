from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import base64

from .. import models, schemas
from ..database import get_db
from ..security import get_password_hash, verify_password, create_access_token
from ..dependencies import get_current_teacher

router = APIRouter(prefix="/auth", tags=["authentication"])


@router.post("/register", response_model=schemas.Token)
def register_teacher(teacher: schemas.TeacherCreate, db: Session = Depends(get_db)):
    """Register a new teacher"""
    existing_teacher = db.query(models.Teacher).filter(
        models.Teacher.email == teacher.email
    ).first()

    if existing_teacher:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    hashed_password = get_password_hash(teacher.password)

    db_teacher = models.Teacher(
        email=teacher.email,
        name=teacher.name,
        hashed_password=hashed_password
    )

    db.add(db_teacher)
    db.commit()
    db.refresh(db_teacher)

    # FIX: store sub as string
    access_token = create_access_token(data={"sub": str(db_teacher.id)})

    teacher_response = schemas.TeacherResponse(
        id=db_teacher.id,
        email=db_teacher.email,
        name=db_teacher.name,
        photo=None
    )

    return schemas.Token(
        access_token=access_token,
        token_type="bearer",
        teacher=teacher_response
    )


@router.post("/login", response_model=schemas.Token)
def login_teacher(credentials: schemas.TeacherLogin, db: Session = Depends(get_db)):
    """Login teacher"""
    teacher = db.query(models.Teacher).filter(
        models.Teacher.email == credentials.email
    ).first()

    if not teacher or not verify_password(credentials.password, teacher.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )

    # FIX: store sub as string
    access_token = create_access_token(data={"sub": str(teacher.id)})

    photo_base64 = None
    if teacher.photo:
        photo_base64 = base64.b64encode(teacher.photo).decode()

    teacher_response = schemas.TeacherResponse(
        id=teacher.id,
        email=teacher.email,
        name=teacher.name,
        photo=photo_base64
    )

    return schemas.Token(
        access_token=access_token,
        token_type="bearer",
        teacher=teacher_response
    )


@router.get("/me", response_model=schemas.TeacherResponse)
def get_current_teacher_info(
    current_teacher: models.Teacher = Depends(get_current_teacher)
):
    """Get current teacher information"""
    photo_base64 = None
    if current_teacher.photo:
        photo_base64 = base64.b64encode(current_teacher.photo).decode()

    return schemas.TeacherResponse(
        id=current_teacher.id,
        email=current_teacher.email,
        name=current_teacher.name,
        photo=photo_base64
    )
