from flask import request, jsonify, current_app as app
from . import db
from .models import Task


@app.route('/api/task', methods=['POST'])
def add_task():
    data = request.get_json()
    id = data.get("id")
    title = data.get("title")
    description = data.get("description")
    status = data.get("status", "Pending")

    if status not in ['Pending', 'In-progress', 'Completed']:
        return jsonify({'message': 'Invalid status', 'status': status}), 400
    if not title:
        return jsonify({'message': 'Title is mandatory'}), 400

    new_task = Task(id=id, title=title, description=description, status=status)
    db.session.add(new_task)
    db.session.commit()
    return jsonify({'message': 'Task added successfully'}), 201

# Delete a task by id
@app.route('/api/task/<int:id>', methods=['DELETE'])
def delete_task(id):
    task = Task.query.get(id)
    if not task:
        return jsonify({'error': 'Task not found'}), 404
    db.session.delete(task)
    db.session.commit()
    return jsonify({'message': 'Task deleted successfully'}), 200

# Get all tasks or filter by status
@app.route('/api/task', methods=['GET'])
def get_tasks():
    status = request.args.get('status')
    if status:
        tasks = Task.query.filter_by(status=status).all()
    else:
        tasks = Task.query.all()
    result = [
        {
            'id': task.id,
            'title': task.title,
            'description': task.description,
            'status': task.status,
            'date_created': task.date_created.strftime('%d-%m-%Y %H:%M:%S')
        }
        for task in tasks
    ]
    return jsonify(result), 200

# Get a single task by id
@app.route('/api/task/<int:id>', methods=['GET'])
def get_task(id):
    task = Task.query.get(id)
    if not task:
        return jsonify({'error': 'Task not found'}), 404
    result = {
        'id': task.id,
        'title': task.title,
        'description': task.description,
        'status': task.status,
        'date_created': task.date_created.strftime('%d-%m-%Y %H:%M:%S')
    }
    return jsonify(result), 200

# Update a task by id
@app.route('/api/task/<int:id>', methods=['PUT'])
def update_task(id):
    task = Task.query.get(id)
    if not task:
        return jsonify({'error': 'Task not found'}), 404
    data = request.get_json()
    title = data.get('title')
    description = data.get('description')
    status = data.get('status')

    if title:
        task.title = title
    if description:
        task.description = description
    if status:
        if status not in ['Pending', 'In-progress', 'Completed']:
            return jsonify({'message': 'Invalid status', 'status': status}), 400
        task.status = status

    db.session.commit()
    return jsonify({'message': 'Task updated successfully'}), 200