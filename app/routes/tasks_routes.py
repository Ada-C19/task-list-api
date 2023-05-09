from flask import Blueprint, jsonify, make_response, request
from app.models.task import Task
from app import db

# All routes for tasks start with "/tasks" URL prefix
tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")

@tasks_bp.route("", methods=["GET"])
def handle_get_tasks_request():
    tasks = Task.query.all()
    task_response = []
    for task in tasks:
        task_response.append(task.to_dict())
    return jsonify(task_response), 200

@tasks_bp.route("", methods=['POST'])
def create_task():
    # Get the data from the request body
    request_body = request.get_json()

    # Use it to make an Task
    new_task = Task.from_dict(request_body)

    # Persist (save, commit) it in the database
    db.session.add(new_task)
    db.session.commit()

    # Check whether task "is_complete"
    is_complete = False
    if new_task.to_dict()["completed_at"]:
        is_complete = True

    # Give back our response
    return {
        "task": {
            "id": new_task.task_id,
            "title": new_task.title,
            "description": new_task.description,
            "is_complete": is_complete
        }
    }, 201