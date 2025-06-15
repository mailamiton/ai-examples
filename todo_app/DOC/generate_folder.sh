#!/bin/bash

# Create the root directory
mkdir todo_app

# Create the app directory
mkdir todo_app/app

# Create the services directory
mkdir todo_app/app/services

# Create the business directory
mkdir todo_app/app/services/business

# Create the database directory
mkdir todo_app/app/services/database

# Create the utils directory
mkdir todo_app/app/services/utils

# Create the models directory
mkdir todo_app/app/models

# Create the schemas directory
mkdir todo_app/app/schemas

# Create the config directory
mkdir todo_app/config

# Create the tests directory
mkdir todo_app/tests

# Create the test_services directory
mkdir todo_app/tests/test_services

# Create the empty files
touch todo_app/app/__init__.py
touch todo_app/app/main.py
touch todo_app/app/services/__init__.py
touch todo_app/app/services/business/__init__.py
touch todo_app/app/services/business/todo_service.py
touch todo_app/app/services/database/__init__.py
touch todo_app/app/services/database/todo_repository.py
touch todo_app/app/services/utils/__init__.py
touch todo_app/app/services/utils/auth.py
touch todo_app/app/models/__init__.py
touch todo_app/app/models/todo.py
touch todo_app/app/schemas/__init__.py
touch todo_app/app/schemas/todo.py
touch todo_app/config/__init__.py
touch todo_app/config/settings.py
touch todo_app/config/logging.conf
touch todo_app/tests/__init__.py
touch todo_app/tests/test_main.py
touch todo_app/tests/test_services/__init__.py
touch todo_app/tests/test_services/test_todo_service.py
touch todo_app/tests/test_services/test_todo_repository.py
touch todo_app/.env
touch todo_app/.gitignore
touch todo_app/README.md
touch todo_app/run.sh