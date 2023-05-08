from app import db
from app.models.task import Task
from flask import Blueprint, jsonify, make_response, request, abort
import copy

tasks_bp = Blueprint("task", __name__, url_prefix="/tasks")

def validate_task(task_id):
    """Validate that task exists in database before using route."""
    try:
        task_id = int(task_id)
    except:
        abort(make_response({"message": f"Task '{task_id}' invalid"}, 400))

    task = Task.query.get(task_id)
    if not task:
        abort(make_response({"message": f"Task '{task_id}' not found"}, 404))

    return task


@tasks_bp.route("", methods=["POST"])
def create_task():
    """Create and add task to database."""
    request_body = request.get_json()

    if "title" not in request_body or "description" not in request_body:
        return {"details": f"Invalid data"}, 400

    new_task = Task(
        title = request_body["title"],
        description = request_body["description"]
    )

    db.session.add(new_task)
    db.session.commit()

    return {"task": new_task.to_dict()}, 201


@tasks_bp.route("", methods=["GET"])
def get_all_tasks():
    """Get all tasks or a task by param."""
    sort_query = request.args.get("sort")

    # Retrieve all tasks, or a task specified by certain criteria
    all_tasks = Task.query.all()

    all_tasks_copy = copy.deepcopy(all_tasks)
    if sort_query == "asc":
        all_tasks = sorted(all_tasks_copy, key=lambda t: t.title)
    elif sort_query == "desc":
        all_tasks = sorted(all_tasks_copy, key=lambda t: t.title, reverse=True)

    response = [task.to_dict() for task in all_tasks]

    return jsonify(response), 200


@tasks_bp.route("/<task_id>", methods=["GET"])
def get_one_task(task_id):
    """Get one task by id."""
    return {"task": validate_task(task_id).to_dict()}, 200


@tasks_bp.route("/<task_id>", methods=["PUT"])
def update_task(task_id):
    """Updates task specifed by id."""
    task = validate_task(task_id)

    request_body = request.get_json()
    task.title = request_body["title"]
    task.description = request_body["description"]

    db.session.commit()

    return {"task": task.to_dict()}, 200


@tasks_bp.route("/<task_id>", methods=["DELETE"])
def delete_task(task_id):
    """Delete task specifed by id."""
    task = validate_task(task_id)

    db.session.delete(task)
    db.session.commit()

    return {"details": f'Task {task.task_id} "{task.title}" successfully deleted'}, 200