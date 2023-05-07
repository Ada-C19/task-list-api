from app import db
from app.models.task import Task
from flask import Blueprint, jsonify, request

tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")

# POST request to create new task
@tasks_bp.route("", methods=['POST'])
def create_task():
    request_body = request.get_json()
    
    new_task = Task(title=request_body["title"], description=request_body["description"], completed_at=request_body["completed_at"])

    db.session.add(new_task)
    db.session.commit()

    return {
        "task": {
        "id": new_task.task_id,
        "title": new_task.title,
        "description": new_task.description,
        "is_complete": False
        }
    }, 201


@tasks_bp.route("", methods=["GET"])
def get_all_tasks():
    tasks = Task.query.all()
    tasks_response = []

    for task in tasks:
        tasks_response.append({
            "id": task.task_id,
            "title": task.title,
            "description": task.description,
            "is_complete": False

        })
    return jsonify(tasks_response), 200