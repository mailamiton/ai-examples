from app.models.todo import Todo
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

load_dotenv()
engine = create_engine(os.getenv("DB_URL"))
Session = sessionmaker(bind=engine)
Base = declarative_base()

class TodoRepository:
    def __init__(self):
        self.session = Session()

    def get_todos(self):
        return self.session.query(Todo).all()

    def create_todo(self, todo: Todo):
        todo = Todo(**todo)
        self.session.add(todo)
        self.session.commit()
        return todo

    def get_todo(self, todo_id: int):
        return self.session.query(Todo).get(todo_id)

    def update_todo(self, todo_id: int, todo: Todo):
        todo = Todo(**todo)
        self.session.query(Todo).filter(Todo.id == todo_id).update(todo)
        self.session.commit()
        return todo

    def delete_todo(self, todo_id: int):
        self.session.query(Todo).filter(Todo.id == todo_id).delete()
        self.session.commit()

    def init_db():
        Base.metadata.create_all(engine)