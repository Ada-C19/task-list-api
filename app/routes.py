from flask import Blueprint, jsonify, make_response, request
from app import db
from app.models.task import Task

task_bp = Blueprint("tasks", __name__, url_prefix="/tasks")

@task_bp.route("", methods = ["GET"])
def get_tasks():
    response = []
    all_tasks = Task.query.all()
    for task in all_tasks:
        response.append(task.to_dict())
    return jsonify(response), 200

@task_bp.route("", methods = ["POST"])
def create_new_task():
    request_body = request.get_json()
    new_task = Task(
        title = request_body["title"],
        description = request_body["description"],
        completed_at = request_body["completed_at"]
    )
    db.session.add(new_task)
    db.session.commit()

    result = new_task.to_dict()
    return jsonify(result), 201



