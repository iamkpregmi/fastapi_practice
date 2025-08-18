from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal, engine
from components.test_component import crud, schema
from models import models

models.Base.metadata.create_all(bind=engine)

router = APIRouter(
    prefix="/test",
    tags=["test"]
)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=schema.TestResponse)
def create_test(test: schema.TestCreate, db: Session = Depends(get_db)):
    return crud.create_test(db=db, test=test)

@router.get("/", response_model=list[schema.TestResponse])
def read_tests(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return crud.get_tests(db, skip=skip, limit=limit)

@router.get("/{test_id}", response_model=schema.TestResponse)
def read_test(test_id: int, db: Session = Depends(get_db)):
    db_test = crud.get_test(db, test_id=test_id)
    if db_test is None:
        raise HTTPException(status_code=404, detail="Test not found")
    return db_test


@router.delete("/delete/{test_id}")
def delete_test(test_id: int, db: Session = Depends(get_db)):
    return crud.delete_test(test_id, db)    

