from app import db
from flask import Blueprint, request, make_response, jsonify
from app.models.task import Task


tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")

@tasks_bp.route("", methods=["POST"])
def create_tasks():
    request_body = request.get_json()
    new_task = Task.from_dict(request_body)

    db.session.add(new_task)
    db.session.commit()

    return make_response(jsonify(f"'task':{new_task.to_dict()}"), 201)

@tasks_bp.route("/<task_id>", methods=["GET"])
def handle_task(task_id):
    task = Task.validate_model(Task, task_id)
    return Task.to_dict(task)

@tasks_bp.route("", methods=["GET"])
def handle_tasks():
    tasks = Task.query.all()
    tasks_response = [Task.to_dict(task) for task in tasks]

    return make_response(jsonify(tasks_response),200)