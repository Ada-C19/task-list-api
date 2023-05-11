from flask import Blueprint, jsonify, request
from app.models.task import Task
from .routes_helpers import validate_model
from app import db
from datetime import datetime
import os
import requests 

task_bp = Blueprint("tasks", __name__, url_prefix="/tasks")

@task_bp.route("", methods=["GET"])
def get_all_tasks():
    tasks_list = []

    sort_param = request.args.get("sort")

    if sort_param == "asc":
        tasks = Task.query.order_by(Task.title.asc())
    elif sort_param == "desc":
        tasks = Task.query.order_by(Task.title.desc())
    else:
        tasks = Task.query.all()
    
    for task in tasks:
        tasks_list.append(task.to_dict())
    
    return jsonify(tasks_list), 200

@task_bp.route("/<task_id>", methods=["GET"])
def get_one_task(task_id):
    task = validate_model(Task, task_id)
    output = {"task":task.to_dict()}

    return jsonify(output), 200

@task_bp.route("", methods=["POST"])
def create_task():
    if request.method == "POST":
        request_body = request.get_json()
        if "title" not in request_body or "description" not in request_body:
            return jsonify({"details": "Invalid data"}), 400
        
        new_task = Task.from_dict(request_body)

        db.session.add(new_task)
        db.session.commit()

        output = {"task":new_task.to_dict()}

        return jsonify(output), 201
    
@task_bp.route("/<task_id>", methods=["PUT"])
def update_task(task_id):
    task = validate_model(Task, task_id)

    request_body = request.get_json()

    task.title=request_body["title"]
    task.description=request_body["description"]
    task.completed_at=request_body.get("completed_at")

    db.session.commit()

    output = {"task":task.to_dict()}

    return jsonify(output), 200

@task_bp.route("/<task_id>/mark_complete", methods=["PATCH"])
def mark_complete(task_id):
    task = validate_model(Task, task_id)

    task.completed_at=datetime.utcnow()
    
    db.session.commit()

    path = "https://slack.com/api/chat.postMessage"

    ada_bot = {
        "token": os.environ.get("SLACK_API_TOKEN"),
        "channel": "task_notifications",
        "text": f"Someone just completed the task {task.title}"
    }

    requests.post(path, data=ada_bot)

    output = {"task":task.to_dict()}

    return jsonify(output), 200

@task_bp.route("/<task_id>/mark_incomplete", methods=["PATCH"])
def mark_incomplete(task_id):
    task = validate_model(Task, task_id)

    task.completed_at=None

    db.session.commit()

    output = {"task":task.to_dict()}

    return jsonify(output), 200


@task_bp.route("/<task_id>", methods=["DELETE"])
def delete_task(task_id):
    task = validate_model(Task, task_id)

    db.session.delete(task)
    db.session.commit()

    output = {"details": f'Task {task_id} \"{task.title}\" successfully deleted'}
    
    return jsonify(output), 200
