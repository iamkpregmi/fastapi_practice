from sqlalchemy.orm import Session
from models.models import School, Student, Library, StudentMarks, VehicleEntry
from components.test_component import schema
from sqlalchemy import func, desc


def get_student_details(school_id, db):
    students = db.query(
        School.name, 
        School.city,
        Student.name
        ).join(
            Student,
            School.id == Student.school_id
        ).filter(
            School.id==school_id
        ).all()

    if not students:
        return {'data': 'Data not found'}
    
    # data_dict = dict(students._mapping) #convert data into object
    data_list = [dict(student._mapping) for student in students]

    return {
        'data': data_list
    }



def get_school_list(request, db):
    school_list = db.query(
        School
    ).filter(
        School.registration_date >= request.from_date,  
        School.registration_date <= request.to_date
    ).order_by(
        School.registration_date.desc()
    ).all()

    data_list = [
        {
            "id": school.id,
            "name": school.name,
            "city": school.city,
            "registration_date": school.registration_date
        }
        for school in school_list
    ]

    return {'data': data_list}



def get_school_list_by_id(request, db):
    school_list = db.query(
        School
    ).filter(
        School.id.in_(request.school_id)
    ).order_by(
        School.registration_date.desc()
    ).all()

    data_list = [
        {
            "id": school.id,
            "name": school.name,
            "city": school.city,
            "registration_date": school.registration_date
        }
        for school in school_list
    ]

    return {'data': data_list}


#Dashboard and Calculation part
def school_dashboard(db):
    #---------------------------------------------
    #Group by course and gender
    studet_data = db.query(
        Student.course,
        Student.gender,
        func.sum(Student.fee).label('total_fee'),
        func.avg(Student.fee).label('avg_fee')
    ).group_by(
        Student.gender,
        Student.course
    ).order_by(
        Student.course
    ).all()

    data_list = [
        {
        "course": stu.course,
        "gender": stu.gender,
        "total_fee": stu.total_fee,
        "avg_fee": stu.avg_fee
    } for stu in studet_data]


    #------------------------------------------
    #City by total fee using join
    fee_data = db.query(
        School.city,
        func.sum(Student.fee).label('total_fee')
    ).join(
        Student,
        School.id == Student.school_id
    ).group_by(
        School.city
    ).order_by(
        desc(func.sum(Student.fee))
    ).all()

    fee_data = [
        {
            'city': fee.city,
            'total_fee': fee.total_fee
        }
        for fee in fee_data]
    
    context = {
        'studet_data': data_list,
        'fee_data': fee_data
    }

    return {'data': context}



#--------------------------Student management----------------------------------
def student_result_by_id(request, db):
    # Get marks for the requested student
    student_info = db.query(
        Student.id,
        Student.name,
        StudentMarks.subject,
        StudentMarks.marks_obtained,
        StudentMarks.max_marks,
    ).join(
        StudentMarks,
        Student.id == StudentMarks.student_id
    ).filter(
        Student.id == request.student_id
    ).all()

    if not student_info:
        return {'data': 'Data not found'}

    student_id = student_info[0].id
    student_name = student_info[0].name

    total_marks_obtained = 0
    total_max_marks = 0
    subjects = []

    for record in student_info:
        total_marks_obtained += record.marks_obtained
        total_max_marks += record.max_marks
        subjects.append({
            "subject": record.subject,
            "marks_obtained": record.marks_obtained,
            "max_marks": record.max_marks
        })

    total_percentage = round((total_marks_obtained / total_max_marks) * 100)

    # Get total marks of all students
    all_students_data = db.query(
        Student.id,
        Student.name,
        func.sum(StudentMarks.marks_obtained).label('total_obtained'),
        func.sum(StudentMarks.max_marks).label('total_max')
    ).join(
        StudentMarks,
        Student.id == StudentMarks.student_id
    ).group_by(
        Student.id
    ).all()

    # Calculate percentage and sort
    student_percentages = []
    for s in all_students_data:
        percentage = (s.total_obtained / s.total_max) * 100
        student_percentages.append((s.id, round(percentage)))

    # Sort by percentage descending
    student_percentages.sort(key=lambda x: x[1], reverse=True)

    # Find rank
    rank = next((i + 1 for i, s in enumerate(student_percentages) if s[0] == student_id), None)
    total_students = len(student_percentages)

    context = {
        "student_id": student_id,
        "student_name": student_name,
        "total_marks_obtained": total_marks_obtained,
        "total_max_marks": total_max_marks,
        "total_percentage": total_percentage,
        "rank": rank,
        "total_students": total_students,
        "rank_out_of": f"{rank} out of {total_students}",
        "subjects": subjects
    }

    return {'data': context}


#all studetn result
def student_result(db):

    show_students = 10 #how many student you want to show
    student_info = db.query(
        StudentMarks.student_id,
        func.sum(StudentMarks.marks_obtained).label("total_obtained"),
        func.sum(StudentMarks.max_marks).label("total_max")
    ).group_by(
        StudentMarks.student_id
    ).all()

    if not student_info:
        return {'data': 'Data not found'}
    
    # Calculate percentage and prepare result
    result = []
    for stu in student_info:
        percentage = round((stu.total_obtained / stu.total_max) * 100, 2)
        result.append({
            "student_id": stu.student_id,
            "marks_obtained": stu.total_obtained,
            "max_marks": stu.total_max,
            "percentage": percentage
        })

    result = sorted(result, key=lambda x: x["percentage"], reverse=True)[:show_students]


    return {'Top 10 Students': result}



def vehicle_details(db):
    return {'data': 'hello world'}
