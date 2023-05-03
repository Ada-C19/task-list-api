from flask import Blueprint, make_response, request, jsonify
from app import db
from app.models.task import Task

tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")

@tasks_bp.route("", methods=["POST"])
def add_task():
    request_body = request.get_json()
    new_task = Task(
        title = request_body["title"],
        description = request_body["description"],
        completed_at = request_body["completed_at"],
    )
    
    response = {}
    response["task"] = new_task

    db.session.add(new_task)
    db.session.commit()

    return {"task":{
        "title": new_task.title, 
        "description": new_task.description,
        "completed_at": new_task.completed_at
    }}, 201