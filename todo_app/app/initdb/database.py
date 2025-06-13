# app/db/database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models.todo import Base # Assuming your models are here
import os

# It's good practice to get the DB URL from an environment variable
DATABASE_URL = os.getenv("DB_URL", "sqlite:///./todos.db")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def create_db_and_tables():
    # This will create all tables defined in your models that inherit from Base
    Base.metadata.create_all(bind=engine)
    print("Database and tables created successfully.")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
