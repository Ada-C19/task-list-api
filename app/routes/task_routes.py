from .helper_functions import create_instance, get_all_instances, get_one_instance, update_instance, delete_instance, make_instance_complete, make_instance_incomplete
from app.models.task import Task
from flask import Blueprint


tasks_bp = Blueprint('tasks', __name__, url_prefix='/tasks')


@tasks_bp.route("", methods=['POST'])
def create_task():
    return create_instance(Task)


@tasks_bp.route("", methods=['GET'])
def get_tasks():
    return get_all_instances(Task)


@tasks_bp.route("/<task_id>", methods=['GET'])
def get_one_task(task_id):
    return get_one_instance(Task, task_id)


@tasks_bp.route("/<task_id>", methods=['PUT'])
def update_task(task_id):
    return update_instance(Task, task_id)


@tasks_bp.route("/<task_id>", methods=['DELETE'])
def delete_task(task_id):
    return delete_instance(Task, task_id)


@tasks_bp.route("/<task_id>/mark_complete", methods=['PATCH'])
def mark_task_completed(task_id):
    return make_instance_complete(Task, task_id)


@tasks_bp.route("/<task_id>/mark_incomplete", methods=['PATCH'])
def mark_task_incomplete(task_id):
    return make_instance_incomplete(Task, task_id)

