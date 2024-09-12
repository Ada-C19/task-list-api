from app import db
from app.models.task import Task
from flask import Blueprint, jsonify, make_response, abort, request
from app.helper_functions import validate_model, create_slack_message
from datetime import datetime


tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")


@tasks_bp.route("", methods=["POST"])
def create_task():
    request_body = request.get_json()
    try:
        task = Task.from_dict(request_body)
        db.session.add(task)
        db.session.commit()

        return make_response({"task": task.to_dict()}, 201)

    except KeyError:
        abort(make_response({"details": "Invalid data"}, 400))


@tasks_bp.route("", methods=["GET"])
def get_all_tasks():
    title_query = request.args.get("sort")
    if title_query == "asc":
        tasks = Task.query.order_by(Task.title.asc())
    elif title_query == "desc":
        tasks = Task.query.order_by(Task.title.desc())
    elif title_query == "id_asc":
        tasks = Task.query.order_by(Task.task_id.asc())
    elif title_query == "id_desc":
        tasks = Task.query.order_by(Task.task_id.desc())
    else:
        tasks = Task.query.order_by(Task.task_id.asc())

    tasks_response = [task.to_dict() for task in tasks]
    return jsonify(tasks_response)


@tasks_bp.route("/<task_id>", methods=["GET"])
def get_one_task(task_id):
    task = validate_model(Task, task_id)
    return {"task": task.to_dict()}


@tasks_bp.route("/<task_id>", methods=["PUT"])
def update_task(task_id):
    task = validate_model(Task, task_id)
    request_body = request.get_json()
    try:
        task.title = request_body["title"]
        task.description = request_body["description"]
        task.completed_at = request_body.get("completed_at")

        db.session.commit()

        return make_response({"task": task.to_dict()}, 200)

    except KeyError:
        abort(make_response({"details": "Invalid data"}, 400))


@tasks_bp.route("/<task_id>/mark_complete", methods=["PATCH"])
def mark_task_complete(task_id):
    task = validate_model(Task, task_id)
    if not task.completed_at:
        task.completed_at = datetime.now().isoformat()

    db.session.commit()
    create_slack_message(task)

    return make_response({"task": task.to_dict()}, 200)


@tasks_bp.route("/<task_id>/mark_incomplete", methods=["PATCH"])
def mark_task_incomplete(task_id):
    task = validate_model(Task, task_id)
    if task.completed_at:
        task.completed_at = None

    db.session.commit()

    return make_response({"task": task.to_dict()}, 200)


@tasks_bp.route("/<task_id>", methods=["DELETE"])
def delete_task(task_id):
    task = validate_model(Task, task_id)

    db.session.delete(task)
    db.session.commit()

    return make_response({"details": task.task_id})
