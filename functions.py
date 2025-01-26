from icecream import ic
import os
import json
from datetime import datetime

current_directory = os.path.dirname(os.path.abspath(__file__))
list_directory = os.path.join(current_directory, "student_lists")
attendees_filepath = "data/attendees.json"
subjects_filepath = "data/subjects.json"

def save_attendance() -> bool:
    try:
        with open(attendees_filepath, "r+") as file:

            attendance_lists = json.loads(file.read())
            if len(attendance_lists["attendance_today"]) == 0:
                return True
            items_to_remove = []
            for attendance in attendance_lists["attendance_today"]: # think about changing the data to a dict
                for student in attendance_lists["attendees"]:
                    if attendance["id"] == student["id"]:
                        attendance_without_id = attendance.copy()
                        attendance_without_id.pop("id")
                        student["attendance"].append(attendance_without_id)
                        items_to_remove.append(attendance)
                        
            for item in items_to_remove:
                attendance_lists["attendance_today"].remove(item)
            
            if len(attendance_lists["attendance_today"]) > 0:
                return False
            
            file.seek(0)
            file.write(json.dumps(attendance_lists, indent=4))
            file.truncate()
            return True
    except Exception:
        return False
    
    
def save_attendance_temp(data) -> dict[bool, str]:
    try:
        with open(attendees_filepath, "r+") as file:
            attendee_check_in = data.__dict__

            attendees = json.loads(file.read())
            attendees["attendance_today"].append(attendee_check_in)
            
            file.seek(0)
            file.write(json.dumps(attendees, indent=4))
            file.truncate()
            return {"status": True, "message": "Saved successfully!"}
    except Exception as e:
        return {"status": False, "message": e}
            
# extend with surname!!!
def save_new_user(data) -> dict[bool, str]: # bug - decide on if either saving id as string or will int suffice, and same for checking in!
    try:
        with open(attendees_filepath, "r+") as file:
            new_student = data.__dict__
            attendees = json.loads(file.read())
            attendees.append(new_student)

            file.seek(0)
            file.write(json.dumps(attendees, indent=4))
            file.truncate()
            return {"status": True, "message": "Successfully added new User!"}
    except Exception as e:
        return {"status": False, "message": e}


def save_new_subject(subject) -> bool:
    try:
        with open(subjects_filepath, "r+") as file:
            new_subject = subject.__dict__
            subjects = json.loads(file.read())
            subjects["subjects"].append(new_subject)

            file.seek(0)
            file.write(json.dumps(subjects, indent=4))
            file.truncate()
            return True
    except Exception:
        return False


def get_attendees(student_id:str=None, 
                  student_name:str=None, 
                  student_surname:str=None,
                  student_active:bool=None) -> dict:
    try:
        with open(attendees_filepath, "r") as file:
            attendees = json.load(file)
            filtered_students = attendees
            
            if student_id is not None:
                filtered_students = [student for student in filtered_students if student.get("id") == student_id]
            if student_name is not None:
                filtered_students = [student for student in filtered_students if student.get("name").lower() == student_name.lower()]
            if student_surname is not None:
                filtered_students = [student for student in filtered_students if student.get("surname").lower() == student_surname.lower()]                
            if student_active is not None:
                filtered_students = [student for student in filtered_students if student.get("is_active") == student_active]
                
            return filtered_students
    except FileNotFoundError:
        return {"error": "File not found!"}
    except json.JSONDecodeError:
        return {"error": "Error decoding JSON!"}
    except Exception as e:
        return {"error": e}
                

def get_subjects(id:int=None, name:str=None) -> dict:
    try:
        with open(subjects_filepath, "r") as file:
            subjects = json.load(file)
            if id and name:
                for subject in subjects["subjects"]:
                    if subject["id"] == id and subject["name"] == name:
                        return subject
                return None
            elif id:
                for subject in subjects["subjects"]:
                    if subject["id"] == id:
                        return subject
                return None
            elif name:
                for subject in subjects["subjects"]:
                    if subject["name"] == name:
                        return subject
                return None
            return subjects
    except FileNotFoundError:
        return {"error": "File not found!"}
    except json.JSONDecodeError:
        return {"error": "Error decoding JSON!"}
    except:
        print("test-last-probably-for-sure?")
        return {"error": "Unknown error!"}
    

def edit_student_details(id:str, data):
    try:
        with open(attendees_filepath, "r+") as file:
            student_to_edit = data.__dict__
            attendees = json.loads(file.read())
            for student in attendees:
                if student.get("id") == id:
                    if student_to_edit.get("name"):
                        student.update({"name":student_to_edit.get("name")})
                    if student_to_edit.get("surname"):
                        student.update({"surname":student_to_edit.get("surname")})
                        
                    if student_to_edit.get("is_active") is not None: 
                        ic(student_to_edit.get("is_active"))
                        ic(student.get("is_active"))
                        if not student_to_edit.get("is_active") and student.get("is_active"):
                            student.update({"date_left": datetime.now().strftime("%Y-%m-%d")})
                        student.update({"is_active":student_to_edit.get("is_active")})
                        
                        ic(student)
            file.seek(0)
            file.write(json.dumps(attendees, indent=4))
            file.truncate()
            return {f"status": True, "message": "Successfully edited User with id {id}!"}
    except Exception as e:
        return {"status": False, "message": e}
    

def deactivate_student(id: str) -> dict[bool, str]:
    # do something
    return {"status": True, "message": f"Deactivation of student with id {id} successful!"}

    
# TODO let's figure out how to keep student age up-to-date
def student_automatically_change_age():
    pass

    
# TODO how about some kind of wrapper function that opens JSON files and handles errors? 