from fastapi import FastAPI, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from validators import is_id_correct, is_student_registered, is_student_already_logged
from data_models import AttendancePayload, Attendee, Subject, User
from icecream import ic
from functions import save_attendance, get_attendees, save_new_user, save_new_subject, get_subjects, save_attendance_temp
from typing import Annotated
from pydantic import BaseModel
from auth import *

greeter_keeper = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@greeter_keeper.get("/users/me", tags=["Users"])
async def read_users_me(current_user: Annotated[User, Depends(get_current_user)]):
    return current_user

@greeter_keeper.post("/token", tags=["Users"])
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user_dict = mock_db.get(form_data.username)
    print(f"{user_dict=}")
    if not user_dict:
        raise HTTPException(status_code=400, detail="Incorrect username or password!")
    user = UserInDB(**user_dict)    
    password = mock_hash_password(form_data.password)
    if not password == user.password:
        raise HTTPException(status_code=400, detail="Incorrect username or password!")

        return {"access_token": user.username, "token_type": "bearer"}
    
    
@greeter_keeper.get("/", tags=["TestRoot"])
def read_root(token: Annotated[str, Depends(oauth2_scheme)]):
    return {"message": "Welcome to the GreeterKeeper server!"}


@greeter_keeper.get("/students/", tags=["Students"])
async def get_students(token: Annotated[str, Depends(oauth2_scheme)], student_id:int=None):
    return get_attendees(student_id)


@greeter_keeper.get("/subjects/", tags=["Subjects"])
async def get_topics(token: Annotated[str, Depends(oauth2_scheme)], id:int=None, name:str=None):
    return get_subjects(id, name)


@greeter_keeper.put("/students/", tags=["Students"])
async def check_in_student(token: Annotated[str, Depends(oauth2_scheme)], data: AttendancePayload):
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


@greeter_keeper.post("/students/", tags=["Students"])
async def add_new_student(token: Annotated[str, Depends(oauth2_scheme)], data: Attendee):
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
    
    
@greeter_keeper.put("/attendance/save_attendance", tags=["Attendance"])
async def transfer_attendance_from_today(token: Annotated[str, Depends(oauth2_scheme)]):
    if save_attendance():
        return {"message": "Attendance saved successfully!"}
    else:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error while transferring the attendance from temp! Please review tha data!")


@greeter_keeper.post("/subjects/", tags=["Subjects"])
async def add_new_subject(token: Annotated[str, Depends(oauth2_scheme)], data: Subject):

    # validation succeeded, proceed with saving the data
    print("save to file will run")
    if save_new_subject(data):
        return {"message": "New subject added successfully!"}
    else:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error saving data!")