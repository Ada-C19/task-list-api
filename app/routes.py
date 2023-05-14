from flask import Blueprint, jsonify, request
from app.models.task import Task
from app import db

tasks_bp = Blueprint('tasks', __name__, url_prefix='/tasks')

@tasks_bp.route('', methods=['POST'])
def create_task():
    data = request.json
    title = data.get('title')
    description = data.get('description')
    completed_at = data.get('completed_at')

    if not title or not description:
        return jsonify({'details': 'Invalid data'}), 400

    task = Task(title=title, description=description, completed_at=completed_at)
    db.session.add(task)
    db.session.commit()

    return jsonify({'task': {
        'id': task.task_id,
        'title': task.title,
        'description': task.description,
        'is_complete': False
    }}), 201
