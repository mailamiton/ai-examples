from pydantic import BaseModel
from datetime import datetime

class Todo(BaseModel):
    title: str
    description: str
    time: datetime
    status: bool