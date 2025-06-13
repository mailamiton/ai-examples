from pydantic import BaseModel, EmailStr
from datetime import datetime

class Todo(BaseModel):
    title: str
    description: str
    email : EmailStr
    schedule_dt: datetime
    status: bool