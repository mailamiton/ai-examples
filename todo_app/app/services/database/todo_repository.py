from app.models.todo import Todo
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine("sqlite:///todos.db")
Session = sessionmaker(bind=engine)

class TodoRepository:
    def __init__(self):
        self.session = Session()

    def get_todos(self):
        return self.session.query(Todo).all()

    def create_todo(self, todo: Todo):
        self.session.add(todo)
        self.session.commit()
        return todo

    def get_todo(self, todo_id: int):
        return self.session.query(Todo).get(todo_id)

    def update_todo(self, todo_id: int, todo: Todo):
        self.session.query(Todo).filter(Todo.id == todo_id).update(todo)
        self.session.commit()
        return todo

    def delete_todo(self, todo_id: int):
        self.session.query(Todo).filter(Todo.id == todo_id).delete()
        self.session.commit()
