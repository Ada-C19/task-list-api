from flask import Blueprint, abort, jsonify, make_response, request
from app import db
from app.models.task import Task

tasks_bp = Blueprint('tasks', __name__, url_prefix='/tasks')

def validate_model_id(model, id):
    if not id.isnumeric():
        abort(make_response(f'Error: {id} is invalid', 400))
    
    entity = model.query.get(id)
    if not entity:
        abort(make_response(f'Not found: No {model.__name__} with id#{id} is found', 404))
    return model

def validate_model_entry(model, request_body):
    for atr in model.get_attributes():
        if atr not in request_body:
            abort(make_response(f'Invalid Request. {model.__name__} {atr} missing', 400))
    return request_body

@tasks_bp.route('', methods=['POST'])
def create_task():
    request_body = request.get_json()
    # valid_request = validate_model_entry(Task, request_body)
    new_task = Task.from_dict(request_body)
    # new_task = Task.from_dict(valid_request)
    
    db.session.add(new_task)
    db.session.commit()
    task = new_task.to_dict()
    if not task['is_complete']:
        task = new_task.to_dict()
        task['is_complete'] = False
        del task['completed_at']
        return {'task': task}, 201
    return {'task': new_task.to_dict()}, 201
    # return {'task': valid_request}, 201

@tasks_bp.route('', methods=['GET'])
def get_tasks():
    pass

@tasks_bp.route('/<task_id>', methods=['GET'])
def get_task_by_id(task_id):
    pass

@tasks_bp.route('/<task_id>', methods=['PUT'])
def replace_task(task_id):
    pass

@tasks_bp.route('/<task_id>', methods=['PATCH'])
def update_task(task_id):
    pass

@tasks_bp.route('/<task_id>', methods=['DELETE'])
def delete_task(task_id):
    pass