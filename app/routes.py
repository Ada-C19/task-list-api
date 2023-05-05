from flask import Blueprint, abort, jsonify, make_response, request
from app import db
from app.models.task import Task

tasks_bp = Blueprint('tasks', __name__, url_prefix='/tasks')

def validate_task_id(task_id):
    pass

def validate_task_entry(request):
    pass

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