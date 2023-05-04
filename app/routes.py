from app import db
from app.models.task import Task
from app.models.goal import Goal
from flask import Blueprint, jsonify, abort, make_response, request

tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")

@tasks_bp.route("", methods=["POST"])
def create_task():
    request_body = request.get_json()
    new_task = Task(
        title = request_body["title"],
        description = request_body["description"],
        completed_at = request_body["completed_at"]
    )

    db.session.add(new_task)
    db.session.commit()

    return make_response(jsonify(f"Task {new_task.title} was successfully created"), 201)

@tasks_bp.route("", methods=["GET"])
def read_all_tasks():
    tasks = Task.query.all()
    tasks_response = []
    for task in tasks:
        tasks_response.append({
            "title": task.title,
            "description": task.description,
            "completed_at": task.completed_at
        })
    return jsonify(tasks_response)

@tasks_bp.route("/task_id", method=["GET"])
def read_one_task():
    pass