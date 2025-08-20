from sqlalchemy.orm import Session
from models.models import School, Student, Library
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

