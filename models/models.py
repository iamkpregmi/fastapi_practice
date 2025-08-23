from sqlalchemy import Column, Integer, String, ForeignKey, Date, Float, Enum
from sqlalchemy.orm import relationship, validates
from database import Base
import enum

# Gender Enum
class GenderEnum(enum.Enum):
    male = "Male"
    female = "Female"
    other = "Other"


class Test(Base):
    __tablename__ = "tests"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)



# ---------- SCHOOL MODEL ----------
class School(Base):
    __tablename__ = "schools"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    
    # Full address split
    address_line1 = Column(String, nullable=False)
    address_line2 = Column(String, nullable=True)
    city = Column(String, nullable=False)
    state = Column(String, nullable=False)
    zipcode = Column(String, nullable=False)
    country = Column(String, nullable=False)

    registration_date = Column(Date, nullable=False)

    # Relationships
    libraries = relationship("Library", back_populates="school")
    students = relationship("Student", back_populates="school")


# ---------- STUDENT MODEL ----------
class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    course = Column(String, nullable=False)
    email = Column(String, unique=True, index=True)
    phone_no = Column(String, nullable=False)
    admission_date = Column(Date, nullable=False)
    gender = Column(Enum(GenderEnum), nullable=False)
    fee = Column(Float, nullable=False)

    school_id = Column(Integer, ForeignKey("schools.id"))
    school = relationship("School", back_populates="students")
    marks = relationship("StudentMarks", back_populates="student", cascade="all, delete-orphan")


# ---------- StudentMarks MODEL ----------
class StudentMarks(Base):
    __tablename__ = "student_marks"

    id = Column(Integer, primary_key=True, index=True)

    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    subject = Column(String, nullable=False)
    marks_obtained = Column(Float, nullable=False)
    max_marks = Column(Float, nullable=False, default=100)

    student = relationship("Student", back_populates="marks")

    @validates('marks_obtained')
    def validate_marks(self, value):
        if value > self.max_marks:
            raise ValueError(f"Marks obtained ({value}) cannot be greater than max_marks ({self.max_marks})")
        return value



# ---------- LIBRARY MODEL ----------
class Library(Base):
    __tablename__ = "libraries"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    issue_date = Column(Date, nullable=False)
    submit_date = Column(Date, nullable=True)

    school_id = Column(Integer, ForeignKey("schools.id"))
    school = relationship("School", back_populates="libraries")



