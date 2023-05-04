from app import db
from app.models.task import Task
from flask import Blueprint, jsonify, make_response, request, abort

tasks_bp = Blueprint("task", __name__, url_prefix="/tasks")


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

    return make_response(jsonify(f"Task '{new_task.title}' successfully created!"), 201)


@tasks_bp.route("", methods=["GET"])
def get_all_tasks():
    task_query = request.args.get("title")

    # all_tasks contains all tasks, or a task specified by title
    all_tasks = Task.query.all() if not task_query else Task.query.filter_by(title=task_query)

    # Add each task in all_tasks to response as a dictionary
    response = [task.to_dict() for task in all_tasks]

    return jsonify(response), 200