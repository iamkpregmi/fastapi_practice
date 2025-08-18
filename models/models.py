from sqlalchemy import Column, Integer, String, ForeignKey, Date
from sqlalchemy.orm import relationship
from database import Base


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


# ---------- LIBRARY MODEL ----------
class Library(Base):
    __tablename__ = "libraries"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    issue_date = Column(Date, nullable=False)
    submit_date = Column(Date, nullable=True)

    school_id = Column(Integer, ForeignKey("schools.id"))
    school = relationship("School", back_populates="libraries")


# ---------- STUDENT MODEL ----------
class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    course = Column(String, nullable=False)
    email = Column(String, unique=True, index=True)
    phone_no = Column(String, nullable=False)
    admission_date = Column(Date, nullable=False)

    school_id = Column(Integer, ForeignKey("schools.id"))
    school = relationship("School", back_populates="students")

