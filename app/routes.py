from flask import Blueprint, request, jsonify
from app.models.task import Task
from app import db

tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")

@tasks_bp.route('', methods=['GET'])
def get_tasks():
    tasks = Task.query.all()
    tasks_response = [task.to_dict() for task in tasks]
    return jsonify(tasks_response), 200

@tasks_bp.route('/<int:task_id>', methods=['GET'])
def get_task(task_id):
    task = Task.query.get(task_id)
    if task:
        return jsonify(task=task.to_dict()), 200
    else:
        return jsonify(details="Task not found"), 404

@tasks_bp.route('', methods=['POST'])
def create_task():
    request_data = request.get_json()

    if "title" not in request_data or "description" not in request_data:
        return jsonify(details="Invalid data"), 400

    new_task = Task(title=request_data['title'], description=request_data['description'])
    db.session.add(new_task)
    db.session.commit()
    return jsonify(task=new_task.to_dict()), 201

@tasks_bp.route('/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    task = Task.query.get(task_id)
    if task:
        request_data = request.get_json()
        task.title = request_data.get('title', task.title)
        task.description = request_data.get('description', task.description)
        db.session.commit()
        return jsonify(task=task.to_dict()), 200
    else:
        return jsonify(details="Task not found"), 404

@tasks_bp.route('/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    task = Task.query.get(task_id)
    if task:
        db.session.delete(task)
        db.session.commit()
        return jsonify(details=f'Task {task_id} "{task.title}" successfully deleted'), 200
    else:
        return jsonify(details="Task not found"), 404
