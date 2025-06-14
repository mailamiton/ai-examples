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

# app = FastAPI(lifespan=lifespan)

app = FastAPI()

@app.get("/todos")
async def get_todos() -> list[dict]: # Return type will be list of dicts after model_dump
    # todo_service.get_todos() returns list[TodoSchema]
    pydantic_models = todo_service.get_todos()
    # Convert Pydantic models to dicts for JSON serialization
    results = [model.model_dump(mode="json") for model in pydantic_models]
    return results

@app.post("/todos")
async def create_todo(todo: dict):
    return todo_service.create_todo(todo)

@app.post("/todobyid")
async def get_todo_by_id(todo_id: dict[str, int]) -> dict:
        # todo_service.get_todos() returns list[TodoSchema]
    pydantic_model = todo_service.get_todo_by_id(todo_id=todo_id.get("id"))
    # Convert Pydantic models to dicts for JSON serialization
    result = pydantic_model.model_dump(mode="json")
    print("result ::",result)
    return result



@app.post("/todobyemail")
async def get_todo_by_email(todo_id: dict[str, str]) -> list[dict]:
    # todo_service.get_todos() returns list[TodoSchema]
    pydantic_models = todo_service.get_todo_by_email(email=todo_id.get("email"))
    # Convert Pydantic models to dicts for JSON serialization
    results = [model.model_dump(mode="json") for model in pydantic_models]
    return results

@app.put("/todos/{todo_id}") 
async def update_todo(todo_id: int, todo: dict):
    return todo_service.update_todo(todo_id, todo)

@app.delete("/todos/{todo_id}")
async def delete_todo(todo_id: int):
    return todo_service.delete_todo(todo_id)


def main():
    uvicorn.run("app.main:app", host="0.0.0.0", port=5000)

if __name__ == "__main__":
    main()