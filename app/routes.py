from flask import Blueprint, jsonify, request, make_response, abort
from app.models.task import Task
from .routes_helpers import validate_model
from sqlalchemy import asc, desc
from app import db
from datetime import datetime

tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")

# get all endpoint
@tasks_bp.route("", methods=["GET"])
def get_all_tasks():
    
    sort_param = request.args.get("sort")
    task_query = Task.query

    if sort_param == "asc":
        task_query = task_query.order_by(asc(Task.title))
    if sort_param == "desc":
        task_query = task_query.order_by(desc(Task.title))

    task_list = [task.to_dict() for task in task_query]

    return jsonify(task_list), 200

@tasks_bp.route("/<id>", methods=["GET"])
def get_one_task(id):
    task = validate_model(Task, id)

    response_body = task.to_dict()

    return jsonify({"task": response_body}), 200

@tasks_bp.route("", methods=["POST"])
def create_task():
    request_body = request.get_json()
    
    try:
        new_task = Task.from_dict(request_body)
    except KeyError:
        abort(make_response({"details": "Invalid data"}, 400))

    db.session.add(new_task)
    db.session.commit()

    return jsonify({f"task": new_task.to_dict()}), 201

@tasks_bp.route("/<id>", methods=["PUT"])
def update_task(id):
    task = validate_model(Task, id)

    request_body = request.get_json()

    task.title = request_body["title"]
    task.description = request_body["description"]

    db.session.commit()

    return jsonify({"task": task.to_dict()}), 200

@tasks_bp.route("/<id>", methods=["DELETE"])
def delete_task(id):
    task = validate_model(Task, id)

    db.session.delete(task)
    db.session.commit()

    return jsonify({"details": f'Task {task.id} "{task.title}" successfully deleted'}), 200

@tasks_bp.route("/<id>/mark_complete", methods=["PATCH"])
def complete_task(id):
    task = validate_model(Task, id)

    task.completed_at = datetime.utcnow()

    db.session.commit()

    return jsonify({"task": task.to_dict()}), 200

@tasks_bp.route("/<id>/mark_incomplete", methods=["PATCH"])
def incomplete_task(id):
    task = validate_model(Task, id)

    task.completed_at = None

    db.session.commit()

    return jsonify({"task": task.to_dict()}), 200

