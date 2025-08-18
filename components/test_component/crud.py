from sqlalchemy.orm import Session
from models import models
from components.test_component import schema

def create_test(db: Session, test: schema.TestCreate):
    db_test = models.Test(name=test.name)
    db.add(db_test)
    db.commit()
    db.refresh(db_test)
    return db_test

def get_tests(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Test).offset(skip).limit(limit).all()

def get_test(db: Session, test_id: int):
    return db.query(models.Test).filter(models.Test.id == test_id).first()
