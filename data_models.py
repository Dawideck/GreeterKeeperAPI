from pydantic import BaseModel, Field
from datetime import datetime
from typing import List, Optional

class AttendancePayload(BaseModel):
        id: str
        class_code: str
        date: str
        subject: str



class Attendance(BaseModel):
        id: str
        date: datetime = Field(default_factory=datetime.now)
        subject: str



class Attendee(BaseModel):
        id: int
        name: str
        age: int
        is_active: bool
        date_joined: str
        attendance: Optional[List[Attendance]]



class AllAttendees(BaseModel):
        attendees: List[Attendee]



class Subject(BaseModel):
    id: int
    name: str