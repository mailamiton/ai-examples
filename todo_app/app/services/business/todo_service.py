from app.models.todo import Todo
from app.services.database.todo_repository import TodoRepository

class TodoService:
    def __init__(self):
        self.todo_repository = TodoRepository()

    def get_todos(self):
        return self.todo_repository.get_todos()

    def create_todo(self, todo: Todo):
        return self.todo_repository.create_todo(todo)

    def get_todo(self, todo_id: int):
        return self.todo_repository.get_todo(todo_id)

    def update_todo(self, todo_id: int, todo: Todo):
        return self.todo_repository.update_todo(todo_id, todo)

    def delete_todo(self, todo_id: int):
        return self.todo_repository.delete_todo(todo_id)