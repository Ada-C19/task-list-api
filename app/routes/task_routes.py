from flask import Blueprint, jsonify, abort, make_response, request
from app import db
from app.models.task import Task
from app.helper import filter_by_params, validate_model, slack_post_message
from datetime import datetime


tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")
@tasks_bp.route("", methods = ["POST"])
def create_tasks():
    request_body = request.get_json()
    try:
        new_task = Task.create_new_task(request_body)
        db.session.add(new_task)
        db.session.commit()

        message = new_task.__str__()

        return make_response(jsonify(message), 201)
    except KeyError as e:
        message = "Invalid data"
        return make_response({"details": message}, 400)

@tasks_bp.route("", methods = ["GET"])
def read_all_tasks():
    query_params = request.args.to_dict()
    tasks = filter_by_params(Task, query_params)
    tasks_response = [task.task_to_dict() for task in tasks]
    return jsonify(tasks_response)

@tasks_bp.route("/<task_id>", methods=["GET"])
def read_one_task(task_id):
    task = validate_model(Task, task_id)
    task = Task.query.get(task_id)
    task = task.__str__()
    return jsonify(task), 200

@tasks_bp.route("/<task_id>", methods=["PUT"])
def update_task(task_id):
    task = validate_model(Task, task_id)
    request_body = request.get_json()
    task.update(request_body)

    db.session.commit()
    message = task.__str__()
    return make_response(jsonify(message))

@tasks_bp.route("/<task_id>", methods=["DELETE"])
def delete_task(task_id):
    task = validate_model(Task, task_id)
    db.session.delete(task)
    db.session.commit()

    message = {
        "details": f'Task {task_id} "{task.title}" successfully deleted'
        }
    return make_response(jsonify(message), 200)

@tasks_bp.route("/<task_id>/mark_complete", methods=["PATCH"])
def mark_task_complete(task_id):
    task = validate_model(Task, task_id)
    task.is_complete = True
    task.completed_at = datetime.now().isoformat()
    db.session.commit()

    slack_post_message(task)
    message = task.__str__()
    return make_response(jsonify(message), 200)

@tasks_bp.route("/<task_id>/mark_incomplete", methods=["PATCH"])
def mark_task_incomplete(task_id):
    task = validate_model(Task, task_id)
    task.is_complete = False
    task.completed_at = None
    db.session.commit()
    message = task.__str__()
    return make_response(jsonify(message), 200)
