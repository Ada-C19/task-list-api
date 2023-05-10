from flask import Blueprint, jsonify, request
from sqlalchemy.sql import func
from app import db
from app import valid
from app.models.task import Task


tasks_bp = Blueprint('tasks', __name__, url_prefix='/tasks')


@tasks_bp.route('', methods=['POST'])
def create_task():
    request_body = request.get_json()
    valid_request = valid.validate_entry(Task, request_body)

    new_task = Task.from_dict(valid_request)
    
    db.session.add(new_task)
    db.session.commit()
    return {'task': new_task.to_dict()}, 201


@tasks_bp.route('', methods=['GET'])
def get_tasks():
    title_query = request.args.get('title')
    sort_query = request.args.get('sort')
    
    if title_query:
        tasks = Task.query.filter(Task.title.ilike('%'+title_query.strip()+'%'))
    elif sort_query == 'asc':
        tasks = Task.query.order_by(Task.title.asc())
    elif sort_query == 'desc':
        tasks = Task.query.order_by(Task.title.desc())
    else:
        tasks = Task.query.all()
    
    task_response = [task.to_dict() for task in tasks]
    return jsonify(task_response), 200


@tasks_bp.route('/<task_id>', methods=['GET'])
def get_task_by_id(task_id):
    task = valid.validate_id(Task, task_id)
    
    return {'task': task.to_dict()}, 200


@tasks_bp.route('/<task_id>', methods=['PUT'])
def replace_task(task_id):
    task = valid.validate_id(Task, task_id)
    
    request_body = request.get_json()
    valid_request = valid.validate_entry(Task, request_body)
    
    task.title = valid_request['title']
    task.description = valid_request['description']
    
    db.session.commit()
    return {'task': task.to_dict()}, 200


@tasks_bp.route('/<task_id>', methods=['PATCH'])
def update_task(task_id):
    task = valid.validate_id(Task, task_id)
    
    request_body = request.get_json()

    task.title = request_body.get('title', task.title)
    task.description = request_body.get('description', task.description)
    
    db.session.commit()
    return {'task': task.to_dict()}, 200


@tasks_bp.route('/<task_id>/mark_complete', methods=['PATCH'])
def mark_complete(task_id):
    task = valid.validate_id(Task, task_id)
    
    task.completed_at, task.is_complete = func.now(), True
    
    db.session.commit()
    return {'task': task.to_dict()}, 200
    
    
@tasks_bp.route('/<task_id>/mark_incomplete', methods=['PATCH'])
def mark_incomplete(task_id):
    task = valid.validate_id(Task, task_id)
    
    task.completed_at, task.is_complete = None, False
    
    db.session.commit()
    return {'task': task.to_dict()}, 200


@tasks_bp.route('/<task_id>', methods=['DELETE'])
def delete_task(task_id):
    task = valid.validate_id(Task, task_id)
    
    task_title = task.title
    
    db.session.delete(task)
    db.session.commit()
    return {'details': f'Task {task_id} "{task_title}" successfully deleted'}, 200