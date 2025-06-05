from fastapi import FastAPI
from app.services.business.todo_service import TodoService

app = FastAPI()

todo_service = TodoService()

@app.get("/todos")
async def get_todos():
    return todo_service.get_todos()

@app.post("/todos")
async def create_todo(todo: dict):
    return todo_service.create_todo(todo)

@app.get("/todos/{todo_id}")
async def get_todo(todo_id: int):
    return todo_service.get_todo(todo_id)

@app.put("/todos/{todo_id}")
async def update_todo(todo_id: int, todo: dict):
    return todo_service.update_todo(todo_id, todo)

@app.delete("/todos/{todo_id}")
async def delete_todo(todo_id: int):
    return todo_service.delete_todo(todo_id)