from icecream import ic
from data_models import AllAttendees

teacher_ids = [1337]
forbidden_ids = [420, 2137, 69]

def is_id_correct(id) -> bool:
    ic(id)
    if id in teacher_ids or id in forbidden_ids:
        return False
    return True

def is_student_registered(student_id: int, students_list: AllAttendees) -> bool:
    ic(students_list["attendees"])
    ic(student_id)
    for student in students_list["attendees"]:
        if student["id"] == student_id:
            return True
    return False

def is_student_already_logged(student_id: int, date:str, students_list) -> bool: # refactor to attendance_today or sth like that
    for student in students_list["attendance_today"]:
        if student["id"] == student_id:
            return True