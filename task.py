from datetime import datetime
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

# Flask app initialization
app = Flask(_name_)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:root%40123@localhost/task_manager'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Task model definition
class Task(db.Model):
    _tablename_ = 'Tasks'
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(300), nullable=False)
    description = db.Column(db.String(500), nullable=False)
    status = db.Column(db.String(50), nullable=False, default='Pending')
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

# Add a new task
@app.route('/api/task', methods=['POST'])
def add_task():
    data = request.get_json()
    sno = data.get("sno")
    title = data.get("title")
    description = data.get("description")
    status = data.get("status", "Pending")

    if status not in ['Pending', 'In-progress', 'Completed']:
        return jsonify({'message': 'Invalid status', 'status': status}), 400
    if not title:
        return jsonify({'message': 'Title is mandatory'}), 400

    new_task = Task(sno=sno, title=title, description=description, status=status)
    db.session.add(new_task)
    db.session.commit()
    return jsonify({'message': 'Task added successfully'}), 201

# Delete a task by serial number
@app.route('/api/task/<int:serialno>', methods=['DELETE'])
def delete_task(serialno):
    task = Task.query.get(serialno)
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
            'sno': task.sno,
            'title': task.title,
            'description': task.description,
            'status': task.status,
            'date_created': task.date_created.strftime('%d-%m-%Y %H:%M:%S')
        }
        for task in tasks
    ]
    return jsonify(result), 200

# Get a single task by serial number
@app.route('/api/task/<int:sno>', methods=['GET'])
def get_task(sno):
    task = Task.query.get(sno)
    if not task:
        return jsonify({'error': 'Task not found'}), 404
    result = {
        'sno': task.sno,
        'title': task.title,
        'description': task.description,
        'status': task.status,
        'date_created': task.date_created.strftime('%d-%m-%Y %H:%M:%S')
    }
    return jsonify(result), 200

# Update a task by serial number
@app.route('/api/task/<int:serialno>', methods=['PUT'])
def update_task(serialno):
    task = Task.query.get(serialno)
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

# Run the Flask app
if _name_ == '_main_':
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=5000)