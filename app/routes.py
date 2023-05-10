from flask import Blueprint, abort, jsonify, make_response, request
from app import db
from app.models.task import Task

tasks_bp = Blueprint('tasks', __name__, url_prefix='/tasks')

def validate_id(model, id):
    if not id.isnumeric():
        abort(make_response({'Error': f'{id} is invalid'}, 400))
    
    entity = model.query.get(id)
    if not entity:
        abort(make_response({'Not found': f'No {model.__name__} with id#{id} is found'}, 404))
    return entity

def validate_entry(model, request_body):
    for atr in model.get_attributes():
        if atr not in request_body:
            abort(make_response({'details': 'Invalid data'}, 400))
            # abort(make_response({'Invalid Request': f'Missing {model.__name__} {atr}'}, 400))
    return request_body

@tasks_bp.route('', methods=['POST'])
def create_task():
    request_body = request.get_json()
    valid_request = validate_entry(Task, request_body)

    new_task = Task.from_dict(valid_request)
    
    db.session.add(new_task)
    db.session.commit()
    
    return {'task': new_task.to_dict()}, 201

@tasks_bp.route('', methods=['GET'])
def get_tasks():
    title_query = request.args.get('title')
    sort_query = request.args.get('sort')

    # if sort_query == 'asc':
    #     tasks = Task.query.order_by(Task.title.asc())
    # elif sort_query == 'desc':
    #     tasks = Task.query.order_by(Task.title.desc())

    # if title_query:
    #     tasks = Task.query.filter(Task.title.ilike(title_query.strip()+'%'))
    # else:
    #     tasks = Task.query.all()
    
    if title_query:
        tasks = Task.query.filter(Task.title.ilike(title_query.strip()+'%'))
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
    task = validate_id(Task, task_id)
    
    return {'task': task.to_dict()}, 200

@tasks_bp.route('/<task_id>', methods=['PUT'])
def replace_task(task_id):
    task = validate_id(Task, task_id)
    
    request_body = request.get_json()
    valid_request = validate_entry(Task, request_body)
    
    task.title = valid_request['title']
    task.description = valid_request['description']
    if 'completed_at' in valid_request:
        task.completed_at = valid_request['completed_at']
        task.is_complete = True
    
    db.session.commit()
    
    return {'task': task.to_dict()}, 200

@tasks_bp.route('/<task_id>', methods=['PATCH'])
def update_task(task_id):
    task = validate_id(Task, task_id)
    
    request_body = request.get_json()

    task.title = request_body.get('title', task.title)
    task.description = request_body.get('description', task.description)
    if 'completed_at' in request_body:
        task.completed_at = request_body['completed_at']
        task.is_complete = True
    
    db.session.commit()
    
    return {'task': task.to_dict()}, 200

@tasks_bp.route('/<task_id>', methods=['DELETE'])
def delete_task(task_id):
    task = validate_id(Task, task_id)
    
    task_title = task.title
    
    db.session.delete(task)
    db.session.commit()
    
    return {'details': f'Task {task_id} "{task_title}" successfully deleted'}, 200