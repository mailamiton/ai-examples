from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class Todo(Base):
    __tablename__ = "todos"

    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String)
    title = Column(String)
    description = Column(String)
    schedule_dt = Column(DateTime, default=datetime.now)
    created_dt = Column(DateTime, default=datetime.now)
    status = Column(Boolean, default=True)
