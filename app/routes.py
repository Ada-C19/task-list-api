from flask import Blueprint, request, jsonify
from app import db
from app.models.task import Task

task_bp = Blueprint("task", __name__, url_prefix="/tasks")

#CREATE
@task_bp.route("", methods=["POST"])
def create_task():
    request_body = request.get_json()

    if "title" not in request_body or "description" not in request_body:
        return jsonify({"details": "Invalid data"}), 400

    #create a new instance of Task
    new_task = Task(
        title = request_body["title"],
        description = request_body["description"],
        completed_at = request_body.get("completed_at", None)
    )
    db.session.add(new_task)
    db.session.commit()

    return jsonify({"task":{
        "id": new_task.task_id,
        "title": new_task.title,
        "description": new_task.description,
        "is_complete": new_task.completed_at is not None
        
    }}), 201
