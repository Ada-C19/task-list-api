from flask import Blueprint, jsonify, request, make_response
from app.models.task import Task
from .routes_helpers import validate_model
from app import db

tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")

# get all endpoint
@tasks_bp.route("", methods=["GET"])
def get_all_tasks():
    
    tasks = Task.query.all()

    task_list = [task.to_dict() for task in tasks]

    return jsonify(task_list), 200

@tasks_bp.route("/<id>", methods=["GET"])
def get_one_task(id):
    task = validate_model(Task, id)

    response_body = task.to_dict()

    return jsonify({"task": response_body}), 200

@tasks_bp.route("", methods=["POST"])
def create_task():

    request_body = request.get_json()
    new_task = Task.from_dict(request_body)

    db.session.add(new_task)
    db.session.commit()

    return jsonify({f"task": new_task.to_dict()}), 201


