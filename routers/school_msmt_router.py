from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal, engine
from components.school_mgmt import crud, schema
from models import models

models.Base.metadata.create_all(bind=engine)

router = APIRouter(
    prefix="/school_mgmt",
    tags=["School Mamangement"]
)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/get-student-by-school-id/{school_id}")
def get_student_details(school_id, db: Session = Depends(get_db)):
    return crud.get_student_details(school_id, db)


@router.post("/get-school-list")
def get_school_list(request: schema.SchoolDetails, db: Session = Depends(get_db)):
    return crud.get_school_list(request, db)



@router.post("/get-school-list-by-id")
def get_school_list_by_id(request: schema.SchoolDetailsId, db: Session = Depends(get_db)):
    return crud.get_school_list_by_id(request, db)


@router.post("/school-dashboard")
def school_dashboard(db: Session = Depends(get_db)):
    return crud.school_dashboard(db)


@router.post("/student-result-by-id")
def student_result_by_id(request: schema.StudentResultSchema ,db: Session = Depends(get_db)):
    return crud.student_result_by_id(request, db)


@router.post("/student-result")
def student_result(db: Session = Depends(get_db)):
    return crud.student_result(db)

@router.post("/vehicle-details")
def vehicle_details(db: Session = Depends(get_db)):
    return crud.vehicle_details(db)