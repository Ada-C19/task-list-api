from flask import Blueprint, abort, jsonify, make_response, request
from app import db
from app.models.task import Task


task_bp = Blueprint("tasks", __name__, url_prefix="/planet")

def validate_task(task_id):
    try:
        task_id = int(task_id)
    except ValueError:
        abort(make_response({"msg": f"Task {task_id} invalid"}, 400))
    
    task = Task.query.get(task_id)

    if not task:
        abort(make_response({"msg": f"Task {task_id} not found"}, 404))

    return task

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

    return make_response({"msg": f"Task {new_task.title} successfully created"}), 201

