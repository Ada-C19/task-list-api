from os import abort
from app import db
from app.models.task import Task
from flask import Blueprint, jsonify, abort, make_response, request

tasks_bp = Blueprint("task", __name__, url_prefix="/tasks")


@tasks_bp.route("", methods=["POST"])
def create_task():
    request_body = request.get_json()
    if "description" not in request_body:
        return make_response(jsonify({"details": "Invalid data"}), 400)
    
    if "title" not in request_body:
        return make_response(jsonify({"details": "Invalid data"}), 400)
    
    new_task = Task.from_dict(request_body)

    db.session.add(new_task)
    db.session.commit()

    return make_response(jsonify(new_task.to_dict()), 201)


@tasks_bp.route("", methods=["GET"])
def get_tasks():
    tasks = Task.query.all()
    task_list = [task.to_dict()["task"] for task in tasks]

    return make_response(jsonify(task_list), 200)


@tasks_bp.route("/<task_id>", methods=["GET"])
def read_one_task(task_id):
    task = Task.validate_task(task_id)
    return make_response(jsonify(task.to_dict()), 200)


@tasks_bp.route("/<task_id>", methods=["PUT"])
def update_task(task_id):
    task = Task.validate_task(task_id)
    
    request_body = request.get_json()
    task.title = request_body["title"]
    task.description = request_body["description"]
    task.completed_at = request_body.get("completed_at", None)
    db.session.commit()

    return make_response(jsonify(task.to_dict()), 200)


@tasks_bp.route("/<task_id>", methods=["DELETE"])
def delete_task(task_id):
    task = Task.validate_task(task_id)
    db.session.delete(task)
    db.session.commit()

    return make_response(jsonify({"details": 'Task 1 "Go on my daily walk 🏞" successfully deleted'}))

