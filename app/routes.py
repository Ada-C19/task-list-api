from flask import Blueprint, request, jsonify, make_response
from app import db
from app.models.task import Task

task_bp = Blueprint("tasks", __name__, url_prefix="/tasks")

@task_bp.route("", methods=["POST"])
def add_task():
    request_body = request.get_json()
    new_task = Task(
        title = request_body["title"],
        description = request_body["description"],
        completed_at = request_body["completed_at"]
    )

    db.session.add(new_task)
    db.session.commit()

    is_complete = True
    if not new_task.completed_at:
        is_complete = False
    

    return jsonify({"id": new_task.task_id,
            "title": new_task.title,
            "description": new_task.description,
            "is_complete": is_complete
            }), 201

@task_bp.route("", methods=["GET"])
def get_tasks():
    response = []
    all_tasks = Task.query.all()

    for task in all_tasks:
        response.append(
            {
                "id": task.task_id,
                "title": task.title,
                "description": new_task.description,
                "is_complete": is_complete
            }
        )
    
    return jsonify(response), 200