from fastapi import FastAPI
import uvicorn
from app.services.business.todo_service import TodoService
from app.initdb.database import create_db_and_tables
from contextlib import asynccontextmanager


todo_service = TodoService()
# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     # Startup code
#     print("Application startup: Initializing resources")
#     yield
#     create_db_and_tables() # Call it here
#     # Shutdown code
#     print("Application shutdown: Cleaning up resources")

#app = FastAPI(lifespan=lifespan)

app = FastAPI()

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


def main():
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000)

if __name__ == "__main__":
    main()