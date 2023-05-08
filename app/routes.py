from app import db
from app.models.task import Task
from flask import Blueprint, jsonify, make_response, request, abort


tasks_bp = Blueprint("tasks_bp", __name__, url_prefix="/tasks")

@tasks_bp.route("", methods=["POST"])
def create_task():
    request_body = request.get_json()

    if "title" not in request_body or "description" not in request_body or "completed_at" not in request_body:
        return make_response({"details": "Invalid data"}, 400)

    new_task = Task(
        title = request_body["title"],
        description = request_body["description"],
        is_complete = request_body["is_complete"]
    )

    db.session.add(new_task)
    db.session.commit()

    return make_response(f"Task {new_task.title} has been successfully created. Hurray!", 201)