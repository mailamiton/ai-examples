from app.services.database.todo_repository import engine

# Create the tables in the database
from app.models.todo import Todo
Todo.metadata.create_all(engine)