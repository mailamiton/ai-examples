from pydantic import BaseModel, EmailStr, ConfigDict
from datetime import datetime

class Todo(BaseModel):
    model_config = ConfigDict(from_attributes=True) # Pydantic V2 way to enable ORM mode

    title: str
    description: str
    email : EmailStr
    schedule_dt: datetime
    status: bool