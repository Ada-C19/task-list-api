from flask import Blueprint, jsonify, abort, make_response, request
from app.models.task import Task
from app import db
from sqlalchemy import asc, desc
from .helper_functions import get_task_instance, validate_task_id, get_task_by_id, update_task_from_request
from datetime import timezone, datetime

tasks_bp = Blueprint('tasks', __name__, url_prefix='/tasks')

@tasks_bp.route("", methods=['POST'])
def create_task():
    new_task = get_task_instance(request)

    db.session.add(new_task)
    db.session.commit()

    task = new_task.to_json()

    return make_response(jsonify(task=task)), 201

@tasks_bp.route("", methods=['GET'])
def get_tasks():
    sort_order = request.args.get("sort", None)

    tasks = Task.query

    title_query = request.args.get("title")
    if title_query:
        tasks = tasks.filter_by(title=title_query)

    if sort_order == "asc":
        tasks = tasks.order_by(asc(Task.title))
    elif sort_order == "desc":
        tasks = tasks.order_by(desc(Task.title))

    tasks = tasks.all()

    task_list = [task.to_json() for task in tasks]

    return jsonify(task_list), 200

@tasks_bp.route("/<task_id>", methods=['GET'])
def get_one_task(task_id):
    task = get_task_by_id(task_id)
    return make_response(jsonify({"task": task.to_json()})), 200

@tasks_bp.route("/<task_id>", methods=['PUT'])
def update_task(task_id):
    task = get_task_by_id(task_id)
    updated_task = update_task_from_request(task, request)

    db.session.commit()

    task = updated_task.to_json()

    return make_response(jsonify(task=task)), 200

@tasks_bp.route("/<task_id>", methods=['DELETE'])
def delete_task(task_id):
    task = get_task_by_id(task_id)

    db.session.delete(task)
    db.session.commit()

    message = f'Task {task_id} "{task.title}" successfully deleted'

    return make_response({"details" : message}), 200

@tasks_bp.route("/<task_id>/mark_complete", methods=['PATCH'])
def mark_task_completed(task_id):
    task = get_task_by_id(task_id)

    task.completed_at = datetime.now(timezone.utc)

    db.session.commit()

    task = task.to_json()
    task["is_complete"] = True

    return make_response(jsonify(task=task)), 200

@tasks_bp.route("/<task_id>/mark_incomplete", methods=['PATCH'])
def mark_task_incomplete(task_id):
    task = get_task_by_id(task_id)

    task.completed_at = None

    db.session.commit()

    task = task.to_json()
    task["is_complete"] = False

    return make_response(jsonify(task=task)), 200
