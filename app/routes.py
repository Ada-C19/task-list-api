from app import db
from app.models.task import task
from flask import Blueprint, jsonify, make_response, request

task_bp = Blueprint("tasks", __name__, url_prefix="/tasks")

@task_bp.route("", methods=["POST"])
def handle_tasks():
    request_body = request.get_json()
    new_task = task(title=request_body["title"],
                    description=request_body["description"]
                    completed_at=request_body["completed_at"])

    db.session.add(new_task)
    db.session.commit()

    return make_response(f"Book {new_task.title} successfully created", 201)
