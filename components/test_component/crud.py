from sqlalchemy.orm import Session
from models.models import Test
from components.test_component import schema

def create_test(db: Session, test: schema.TestCreate):
    db_test = Test(name=test.name)
    db.add(db_test)
    db.commit()
    db.refresh(db_test)
    return db_test

def get_tests(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Test).offset(skip).limit(limit).all()

def get_test(db: Session, test_id: int):
    return db.query(Test).filter(Test.id == test_id).first()


def delete_test(test_id, db):
    test_data = db.query(Test).filter(Test.id == test_id).first()

    if not test_data:
        return {'msg': 'Data not found'}
    
    db.delete(test_data)
    db.commit()

    return {'data': 'Data deleted Successfully'}

