# Flask-Task-Manager-API
A RESTful API built using Flask and SQLAlchemy that allows users to create, manage, and track personal tasks.

## Features

- Add, update, delete, and fetch tasks
- Filter tasks by status 
- Uses MySQL database via SQLAlchemy ORM

## Tech Stack

- Python
- Flask
- SQLAlchemy
- MySQL

## **🚀 API Usage (via curl)**

➕ Create a Task

curl --location --globoff '{{base_url}}/api/task' \
--header 'Content-Type: application/json' \
--data '{
    "id": 1,
    "title": "Sample Task",
    "description": "This is a test task",
    "status": "Pending"
}'


📃 Get All Tasks

curl --location --globoff '{{base_url}}/api/task'


📃 Get All Tasks by Status

curl --location --globoff '{{base_url}}/api/task?status=Completed'


🔍 Get Task by ID

curl --location --globoff '{{base_url}}/api/task/{{id}}'


✏️ Update Task

curl --location --globoff --request PUT '{{base_url}}/api/task/{{id}}' \
--header 'Content-Type: application/json' \
--data '{
    "id": 1,
    "title": "Sample Task",
    "description": "This is a test task",
    "status": "Pending"
}'


❌ Delete Task

curl --location --globoff --request DELETE '{{base_url}}/api/task/{{id}}'
