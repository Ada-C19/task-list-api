from flask import Blueprint, request, make_response, request, abort, jsonify
from app import db
from app.models.task import Task

tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")

@tasks_bp.route("", methods=["POST"])
def add_task():
    request_body = request.get_json()
    new_task = Task(
            title= request_body["title"],
            description= request_body['description'],
            completed_at= request_body['completed_at']
        )
    
    db.session.add(new_task)
    db.session.commit()

    is_complete = True
    if not new_task.completed_at:
        is_complete = False

    return jsonify({
        "task": {
            "id": new_task.task_id,
            "title": new_task.title,
            "description": new_task.description,
            "is_complete": is_complete
        }
    }), 201