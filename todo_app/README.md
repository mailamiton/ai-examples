# To-Do App

A simple To-Do App built using FastAPI with an enterprise-level folder structure.

## Requirements

* Python 3.9+
* FastAPI 0.65.0+
* Uvicorn 0.15.0+
* SQLAlchemy 1.4.26+
* Pydantic 1.8.2+

## Installation

1. Clone the repository: `git clone https://github.com/your-username/todo-app.git`
2. Create a virtual environment: `python -m venv venv`
3. Activate the virtual environment: `source venv/bin/activate` (on Linux/Mac) or `venv\Scripts\activate` (on Windows)
4. Install dependencies: `pip install -r requirements.txt`
5. Copy the `.env.example` file to `.env` and update the environment variables as needed

## Running the App

1. Run the app using Uvicorn: `uvicorn app.main:app --host 0.0.0.0 --port 8000`
2. Open a web browser and navigate to `http://localhost:8000/docs` to access the API documentation

## API Endpoints

* `GET /todos`: Retrieve a list of all To-Do items
* `POST /todos`: Create a new To-Do item
* `GET /todos/{todo_id}`: Retrieve a single To-Do item by ID
* `PUT /todos/{todo_id}`: Update a To-Do item
* `DELETE /todos/{todo_id}`: Delete a To-Do item

## Services

* `business.todo_service`: Handles business logic for To-Do items
* `database.todo_repository`: Handles database operations for To-Do items
* `utils.auth`: Handles authentication and authorization

## Models

* `models.todo`: Defines the To-Do item model

## Schemas

* `schemas.todo`: Defines the To-Do item schema for API requests and responses