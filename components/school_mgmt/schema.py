from pydantic import BaseModel
from datetime import date
from typing import List

class SchoolDetails(BaseModel):
    from_date: date
    to_date: date


class SchoolDetailsId(BaseModel):
    school_id: List[int]


class StudentResultSchema(BaseModel):
    student_id: int
    

