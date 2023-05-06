from app import db
from app.models.task import Task
from app.models.goal import Goal
from app.routes.helpers import create_item, get_all_items, get_item, \
  update_item, delete_item, mark_item_complete, mark_item_incomplete
from flask import Blueprint

tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")

@tasks_bp.route("", methods=["POST"])
def create_task():
    return create_item(Task)

@tasks_bp.route("", methods=["GET"])
def get_all_tasks():
    return get_all_items(Task)

@tasks_bp.route("/<task_id>", methods=["GET"])
def get_task(task_id):
    return get_item(Task, task_id)

@tasks_bp.route("/<task_id>", methods=["PUT"])
def update_task(task_id):
    return update_item(Task, task_id)

@tasks_bp.route("/<task_id>", methods=["DELETE"])
def delete_task(task_id):
    return delete_item(Task, task_id)

@tasks_bp.route("/<task_id>/mark_complete", methods=["PATCH"])
def mark__task_complete(task_id):
    return mark_item_complete(Task, task_id)

@tasks_bp.route("/<task_id>/mark_incomplete", methods=["PATCH"])
def mark__task_incomplete(task_id):
    return mark_item_incomplete(Task, task_id)