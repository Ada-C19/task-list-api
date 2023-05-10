from app import db
from app.models.task import Task
from flask import Blueprint, jsonify, make_response, abort, request

tasks_bp = Blueprint("tasks", __name__, url_prefix = "/tasks")

@tasks_bp.route("", methods=["GET"])
def read_task():
    tasks_response = []
    tasks = Task.query.all()

    for task in tasks:
        tasks_response.append(
            {
                "id": task.task_id,
                "title": task.title,
                "description": task.description,
                "is_complete": False
            }
        ), 200

    return jsonify(tasks_response)
