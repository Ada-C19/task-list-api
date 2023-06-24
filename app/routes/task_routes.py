from flask import Blueprint, request, jsonify
from app.models.task import Task
from app import db
from app.routes.helper import validate_model, send_slack_massage
from sqlalchemy import asc, desc
from datetime import datetime


tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")


@tasks_bp.route("", methods=["POST"])
def create_task():
    response = request.get_json()

    try:
        new_task = Task.from_dict(response)

    except KeyError:
        message = {"details": "Invalid data"}
        return jsonify(message), 400

    db.session.add(new_task)
    db.session.commit()

    result = {"task": new_task.to_dict()}
    return jsonify(result), 201


@tasks_bp.route("", methods=["GET"])
def get_all_tasks():
    model_query = Task.query.order_by(desc(Task.completed_at))
    sort_query = request.args.get("sort")
    title_query = request.args.get("title")

    if title_query:
        model_query = model_query.filter(
            Task.title == request.args.get("title"))

    if sort_query == "asc":
        model_query = model_query.order_by(asc(Task.title))
    elif sort_query == "desc":
        model_query = model_query.order_by(desc(Task.title))

    all_tasks = model_query.all()

    tasks_response = [task.to_dict() for task in all_tasks]
    return jsonify(tasks_response), 200


@tasks_bp.route("/<task_id>", methods=["GET"])
def get_one_task(task_id):
    task = validate_model(Task, task_id)

    result = {"task": task.to_dict()}
    return jsonify(result), 200


@tasks_bp.route("/<task_id>", methods=["PUT"])
def update_task(task_id):
    response = request.get_json()
    task_to_update = validate_model(Task, task_id)

    try:
        task_to_update.title = response["title"]
        task_to_update.description = response["description"]

    except KeyError:
        message = {"details": "Invalid data"}
        return jsonify(message), 400

    db.session.commit()
    result = {"task": task_to_update.to_dict()}
    return jsonify(result), 200


@tasks_bp.route("/<task_id>", methods=["DELETE"])
def delete_task(task_id):
    task_to_delete = validate_model(Task, task_id)
    db.session.delete(task_to_delete)
    db.session.commit()

    message = {
        "details": f'Task {task_to_delete.task_id} "{task_to_delete.title}" successfully deleted'}
    return jsonify(message), 200


@tasks_bp.route("/<task_id>/mark_complete", methods=["PATCH"])
def mark_complete(task_id):
    task = validate_model(Task, task_id)

    task.completed_at = datetime.now()
    db.session.commit()

    send_slack_massage(task)

    result = {"task": task.to_dict()}
    return jsonify(result), 200


@tasks_bp.route("/<task_id>/mark_incomplete", methods=["PATCH"])
def mark_incomplete(task_id):
    task = validate_model(Task, task_id)

    task.completed_at = None
    db.session.commit()

    result = {"task": task.to_dict()}
    return jsonify(result), 200
