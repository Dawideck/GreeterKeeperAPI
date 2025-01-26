from fastapi import FastAPI, HTTPException, status, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from validators import is_id_correct, is_student_registered, is_student_already_logged
from data_models import AttendancePayload, Attendee, Subject, StudentEditPayload
from icecream import ic
from functions import save_attendance, get_attendees, save_new_user, save_new_subject, get_subjects, save_attendance_temp, deactivate_student, edit_student_details


greeter_keeper = FastAPI()
    
@greeter_keeper.get("/", tags=["TestRoot"], summary="Test endpoint")
def read_root():
    return {"message": "Welcome to the GreeterKeeper server!"}

# TODO This is returning a 200 even for an empty list, 404????
# TODO extend with search "joined before/after date"
@greeter_keeper.get("/students/", tags=["Students"])
async def get_students(student_id:str=None, 
                       student_name:str=None, 
                       student_surname:str=None,
                       student_active:bool=None):
    return get_attendees(student_id, student_name, student_surname, student_active)


@greeter_keeper.post("/students/", tags=["Students"])
async def add_new_student(data: Attendee):
    new_student = data
    if not is_id_correct(new_student.id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid Student ID!")

    if is_student_registered(new_student.id, get_attendees()):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Id already exists, use different card!")
    
    # validation succeeded, proceed with saving the data
    result = save_new_user(new_student)
    if result.get("status"):
        return result.get("message")
    else:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=result.get("message"))


@greeter_keeper.put("/students/", tags=["Students"])
async def edit_student_data(id:str, data: StudentEditPayload):
    
    if not is_student_registered(id, get_attendees()):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Student with id {id} does not exist!")
    # check if payload proper
    edit_student_details(id, data)
    # deactivate student
    deactivation_result = deactivate_student(id)
    if not deactivation_result.get("status"):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=deactivation_result.get("message"))
    
    return {"message": f"Student with id {id} edited successfully!"}


@greeter_keeper.put("/attendance/", tags=["Attendance"])
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
    save_attendance_temp(student_check_in)
    return {"message": "Student checked in successfully!"}
    
    
@greeter_keeper.post("/attendance/save", tags=["Attendance"])
async def transfer_attendance_from_today():
    if save_attendance():
        return {"message": "Attendance saved successfully!"}
    else:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error while transferring the attendance from temp! Please review tha data!")


@greeter_keeper.post("/subjects/", tags=["Subjects"])
async def add_new_subject(data: Subject):

    # validation succeeded, proceed with saving the data
    print("save to file will run")
    if save_new_subject(data):
        return {"message": "New subject added successfully!"}
    else:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error saving data!")


@greeter_keeper.get("/subjects/", tags=["Subjects"])
async def get_topics(id:int=None, name:str=None):
    return get_subjects(id, name)
    