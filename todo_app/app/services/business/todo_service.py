from app.models.todo import Todo
from app.schemas.todo import Todo as To
from app.services.database.todo_repository import TodoRepository
from datetime import datetime
from dateutil import parser

class TodoService:
    def __init__(self):
        self.todo_repository = TodoRepository()

    def get_todos(self) -> list[To]:
         # Fetches ORM model instances from the repository.
        todo_instances = self.todo_repository.get_todos()
        # Converts these ORM instances to Pydantic 'To' schema instances.
        todo_schemas = [To.model_validate(todo) for todo in todo_instances]
        return todo_schemas

    def create_todo(self, todo: Todo):
         # Parse schedule_dt input from user
        schedule_dt_input = todo['schedule_dt']
        try:
            schedule_dt = parser.parse(schedule_dt_input)
        except ValueError:
            # Handle invalid date format error
            raise ValueError("Invalid date format for schedule_dt")

        # Create a new Todo object with the parsed schedule_dt
        parsed_todo = Todo(
            title=todo['title'],
            description=todo['description'],
            email=todo['email'],
            schedule_dt=schedule_dt,
            status=True
        )
        return self.todo_repository.create_todo(todo=parsed_todo)

    def get_todo_by_id(self, todo_id: int) -> dict : 
        print("todo_id service", todo_id)
        todo_instance = self.todo_repository.get_todo_by_id(todo_id)
        # Converts these ORM instances to Pydantic 'To' schema instances.
        todo_schemas = To.model_validate(todo_instance)
        print("todo_schemas ::", todo_schemas)
        return todo_schemas
    
    def get_todo_by_email(self, email: str)  -> list[To] : 
        print("email :: ", email)
        todo_instances = self.todo_repository.get_todo_by_email(email=email)
       # Converts these ORM instances to Pydantic 'To' schema instances.
        todo_schemas = [To.model_validate(todo) for todo in todo_instances]
        print("todo_schemas ::", todo_schemas)
        return todo_schemas

    def update_todo(self, todo_id: int, todo: Todo):
        return self.todo_repository.update_todo(todo_id, todo)

    def delete_todo(self, todo_id: int):
        return self.todo_repository.delete_todo(todo_id)
    
    def init_db(self):
        return self.todo_repository.init_db()