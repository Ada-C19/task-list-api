from flask import Blueprint
from app.models.task import Task
from app.routes.helpers import create_item, get_all_items, get_one_item, update_item, delete_item, mark_item_complete, mark_item_incomplete


tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")


@tasks_bp.route("", methods=["POST"])
def create_task():
    return create_item(Task)


@tasks_bp.route("", methods=["GET"])
def get_all_tasks():
    return get_all_items(Task)


@tasks_bp.route("/<task_id>", methods=["GET"])
def get_one_task(task_id):
    return get_one_item(Task, task_id)


@tasks_bp.route("<task_id>", methods=["PUT"])
def update_task(task_id):
    return update_item(Task, task_id)


@tasks_bp.route("<task_id>", methods=["DELETE"])
def delete_task(task_id):
    return delete_item(Task, task_id)


@tasks_bp.route("<task_id>/mark_complete", methods=["PATCH"])
def mark_task_complete(task_id):
    return mark_item_complete(Task, task_id)


@tasks_bp.route("<task_id>/mark_incomplete", methods=["PATCH"])
def mark_task_incomplete(task_id):
    return mark_item_incomplete(Task, task_id)