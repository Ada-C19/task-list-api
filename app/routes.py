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
    for atr in model.self_attributes():
        if atr not in request_body:
            abort(make_response(f'Invalid Request. {model.__name__} {atr} missing', 400))

@tasks_bp.route('', methods=['POST'])
def create_task():
    pass

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