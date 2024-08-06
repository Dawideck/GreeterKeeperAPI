from fastapi import FastAPI, HTTPException, status
from validators import is_id_correct, is_student_registered, is_student_already_logged
from data_models import AttendancePayload, Attendee, Subject
from icecream import ic
from functions import save_attendance, get_attendees, save_new_user, save_new_subject, get_subjects

greeter_keeper = FastAPI()

@greeter_keeper.get("/")
def read_root():
    return {"message": "Welcome to the GreeterKeeper server!"}


@greeter_keeper.get("/students/")
async def get_students(student_id:int=None):
    return get_attendees(student_id)


@greeter_keeper.get("/subjects/")
async def get_topics(id:int=None, name:str=None):
    return get_subjects(id, name)


@greeter_keeper.put("/students/")
async def check_in_student(data: AttendancePayload):
    student_check_in = data
    if not is_id_correct(student_check_in.id):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid Student ID!")

    if not is_student_registered(student_check_in.id, get_attendees()):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Student not registered, please register!")

    if is_student_already_logged(student_check_in.id, student_check_in.date, get_attendees()):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Student already checked in today!")

    # validation succeeded, proceed with saving the data
    print("save to file will run")
    save_attendance(student_check_in)
    return {"message": "Student checked in successfully!"}


@greeter_keeper.post("/students/")
async def add_new_student(data: Attendee):
    new_student = data
    if not is_id_correct(new_student.id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid Student ID!")

    if is_student_registered(new_student.id, get_attendees()):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Id already exists, choose another!")

    # validation succeeded, proceed with saving the data
    print("save to file will run")
    if save_new_user(new_student):
        return {"message": "New student added successfully!"}
    else:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error saving data!")


@greeter_keeper.post("/subjects/")
async def add_new_subject(data: Subject):

    # validation succeeded, proceed with saving the data
    print("save to file will run")
    if save_new_subject(data):
        return {"message": "New subject added successfully!"}
    else:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error saving data!")