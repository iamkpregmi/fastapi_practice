from sqlalchemy import Column, Integer, String, ForeignKey, Date, Float, Enum, JSON, Boolean, DateTime
from sqlalchemy.orm import relationship, validates
from database import Base
import enum
from datetime import datetime

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



#--------------------------------------------------------------
class Company(Base):
    __tablename__ = 'companies'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    industry = Column(String)
    city = Column(String)
    state = Column(String)
    country = Column(String)
    established = Column(Date)

    employees = relationship("Employee", back_populates="company")



class Employee(Base):
    __tablename__ = 'employees'

    id = Column(Integer, primary_key=True, index=True)

    # Personal Info
    first_name = Column(String, nullable=False)
    last_name = Column(String)
    gender = Column(String)
    date_of_birth = Column(Date)
    marital_status = Column(String)

    # Contact Info
    email = Column(String, unique=True)
    phone_number = Column(String)
    alternate_phone = Column(String)
    address = Column(String)
    city = Column(String)
    state = Column(String)
    country = Column(String)
    zipcode = Column(String)

    # Job Info
    designation = Column(String)
    department = Column(String)
    employee_code = Column(String, unique=True)
    date_of_joining = Column(Date)
    employment_date = Column(Date)  # same as joining, but separate if needed
    date_of_exit = Column(Date, nullable=True)
    is_active = Column(Boolean, default=True)
    employment_type = Column(String)  # e.g., Full-Time, Part-Time, Intern, Contract

    # Education & Skills
    highest_qualification = Column(String)
    university = Column(String)
    passing_year = Column(Integer)
    skills = Column(String)  # comma-separated string or separate table (future)

    # Salary & Docs
    salary = Column(Float)
    pan_number = Column(String)
    aadhaar_number = Column(String)
    passport_number = Column(String)
    resume_url = Column(String)
    profile_picture_url = Column(String)

    # Emergency Contact
    emergency_contact_name = Column(String)
    emergency_contact_relation = Column(String)
    emergency_contact_number = Column(String)

    # Misc
    blood_group = Column(String)
    nationality = Column(String)
    remarks = Column(String)
    misc_data = Column(JSON)  # <-- dynamic field as requested

    # Foreign Key
    company_id = Column(Integer, ForeignKey("companies.id"))
    company = relationship("Company", back_populates="employees")




class VehicleEntry(Base):
    __tablename__ = 'vehicle_entries'

    id = Column(Integer, primary_key=True, index=True)
    
    company_name = Column(String, nullable=False)
    vehicle_id = Column(String, nullable=False)

    empty_weight = Column(Float, nullable=False)
    loaded_weight = Column(Float, nullable=False)

    entry_time = Column(DateTime, default=datetime.utcnow)
    exit_time = Column(DateTime, nullable=True)

    driver_name = Column(String, nullable=False)
    toll_fee = Column(Float, nullable=False)