from app import db
from app.models.task import Task
from flask import Blueprint, jsonify, make_response, request, abort

tasks_bp = Blueprint("task", __name__, url_prefix="/tasks")


@tasks_bp.route("", methods=["POST"])
def create_task():
    request_body = request.get_json()

    if "title" not in request_body or "description" not in request_body:
        return {"details": f"Invalid data"}, 400

    new_task = Task(
        title=request_body["title"],
        description=request_body["description"]
    )

    db.session.add(new_task)
    db.session.commit()

    return {"task": new_task.to_dict()}, 201


@tasks_bp.route("", methods=["GET"])
def get_all_tasks():
    task_query = request.args.get("title")

    # Store all tasks, or a task specified by title
    all_tasks = Task.query.all() if not task_query else Task.query.filter_by(title=task_query)

    # Add each task in all_tasks to response as a dictionary
    response = [task.to_dict() for task in all_tasks]

    return jsonify(response), 200


def validate_task(task_id):
    try:
        task_id = int(task_id)
    except:
        abort(make_response({"message": f"Task '{task_id}' invalid"}, 400))

    task = Task.query.get(task_id)
    if not task:
        abort(make_response({"message": f"Task '{task_id}' not found"}, 404))

    return task


@tasks_bp.route("/<task_id>", methods=["GET"])
def get_one_task(task_id):
    task = validate_task(task_id)

    return {"task": task.to_dict()}, 200
