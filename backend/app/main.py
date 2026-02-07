from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .config import settings
from .database import init_db
from .middleware import log_requests, error_handler
from .api import auth, teachers, classes, students, attendance

app = FastAPI(
    title="Face Recognition Attendance System",
    description="A complete attendance system using face recognition",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Custom middleware
app.middleware("http")(log_requests)
app.middleware("http")(error_handler)

# Include routers
app.include_router(auth.router)
app.include_router(teachers.router)
app.include_router(classes.router)
app.include_router(students.router)
app.include_router(attendance.router)

@app.on_event("startup")
def startup_event():
    """Initialize database on startup"""
    init_db()

@app.get("/")
def read_root():
    return {
        "message": "Face Recognition Attendance System API",
        "version": "1.0.0",
        "docs": "/docs"
    }

@app.get("/health")
def health_check():
    return {"status": "healthy"}
