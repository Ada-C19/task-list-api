from flask import Blueprint, jsonify, make_response, request
from app.models.task import Task
from app import db

# All routes for tasks start with "/tasks" URL prefix
tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")

@tasks_bp.route("", methods=["GET"])
def handle_get_animals_request():
    tasks = Task.query.all()
    task_response = []
    for task in tasks:
        task_response.append(task.to_dict())
    return jsonify(task_response), 200