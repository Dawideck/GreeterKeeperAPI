from icecream import ic
import os
import json

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
    
    
def save_attendance_temp(data) -> bool:
    try:
        with open(attendees_filepath, "r+") as file:
            attendee_check_in = data.__dict__

            attendees = json.loads(file.read())
            attendees["attendance_today"].append(attendee_check_in)
            
            file.seek(0)
            file.write(json.dumps(attendees, indent=4))
            file.truncate()
            return True
    except Exception:
        return False
            

def save_new_user(data) -> bool: # bug - decide on if either saving id as string or will int suffice, and same for checking in!
    try:
        with open(attendees_filepath, "r+") as file:
            new_student = data.__dict__
            attendees = json.loads(file.read())
            attendees["attendees"].append(new_student)

            file.seek(0)
            file.write(json.dumps(attendees, indent=4))
            file.truncate()
            return True
    except Exception:
        return False


def save_new_subject(subject) -> bool:
    try:
        with open(subjects_filepath, "r+") as file:
            new_subject = subject.__dict__
            subjects = json.loads(file.read())
            ic(subjects)
            subjects["subjects"].append(new_subject)

            file.seek(0)
            file.write(json.dumps(subjects, indent=4))
            file.truncate()
            return True
    except Exception:
        return False


def get_attendees(student_id:int=None) -> dict:
    try:
        with open(attendees_filepath, "r") as file:
            attendees = json.load(file)
            ic(attendees)
            ic(student_id)
            if student_id:
                for student in attendees["attendees"]:
                    ic(student["id"])
                    if student["id"] == int(student_id):
                        return student
        return attendees
    except FileNotFoundError:
        return {"error": "File not found!"}
    except json.JSONDecodeError:
        return {"error": "Error decoding JSON!"}
    except:
        return {"error": "Unknown error!"}


def get_subjects(id:int=None, name:str=None) -> dict:
    try:
        with open(subjects_filepath, "r") as file:
            subjects = json.load(file)
            ic(subjects)
            ic(id)
            ic(name)
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
    