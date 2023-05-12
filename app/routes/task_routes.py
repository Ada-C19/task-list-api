from app import db
from app.models.task import Task
from flask import Blueprint, jsonify, abort, make_response, request
from datetime import datetime
from app.helpers import validate_model
import os
import requests

tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")

@tasks_bp.route("", methods=["GET"])
def get_all_tasks():

    sort_direction = request.args.get("sort")

    if sort_direction == "asc":
        tasks = Task.query.order_by(Task.title)
    elif sort_direction == "desc":
        tasks = Task.query.order_by(Task.title.desc())
    else:
        tasks = Task.query.all()
    
    results = [task.to_dict() for task in tasks]

    return jsonify(results)

@tasks_bp.route("/<task_id>", methods=["GET"])
def get_one_task(task_id):
    task = validate_model(Task, task_id)
    response = {"task": task.to_dict()}

    return jsonify(response)

@tasks_bp.route("", methods=["POST"])
def create_task():
    request_body = request.get_json()
    
    new_task_is_valid = "title" in request_body and "description" in request_body
    if not new_task_is_valid:
        abort(make_response(jsonify({"details":"Invalid data"}), 400))

    new_task = Task.from_dict(request_body)
    db.session.add(new_task)
    db.session.commit()
    
    response = {"task": new_task.to_dict()}

    return make_response((jsonify(response)), 201)

@tasks_bp.route("/<task_id>", methods=["PUT"])
def update_one_task(task_id):    
    task = validate_model(Task, task_id)
    updated_data = request.get_json()

    task.title = updated_data["title"]
    task.description = updated_data["description"]

    db.session.commit()

    response = {"task": task.to_dict()}

    return make_response(response, 200)

@tasks_bp.route("<task_id>", methods=["DELETE"])
def delete_one_task(task_id):
    task_to_delete = validate_model(Task, task_id)
    
    db.session.delete(task_to_delete)
    db.session.commit()

    message = {"details":f"Task {task_id} \"{task_to_delete.title}\" successfully deleted"}
    return make_response(message, 200)

@tasks_bp.route("/<task_id>/mark_complete", methods=["PATCH"])
def complete_one_task(task_id):    
    task = validate_model(Task, task_id)

    if not task.completed_at:
        task.completed_at = datetime.now()

    db.session.commit()
    
    url = "https://slack.com/api/chat.postMessage"
    SLACK_API_TOKEN = os.environ.get("SLACK_API_TOKEN")
    headers = {"Authorization": f"Bearer {SLACK_API_TOKEN}"}
    message = f"Someone just completed the task {task.title}"
    data = {"channel": "random", "text": message}

    requests.post(url, headers=headers, data=data)

    response = {"task": task.to_dict()}
    return make_response(response, 200)

@tasks_bp.route("/<task_id>/mark_incomplete", methods=["PATCH"])
def incomplete_one_task(task_id):    
    task = validate_model(Task, task_id)

    if task.completed_at:
        task.completed_at = None

    db.session.commit()
    response = {"task": task.to_dict()}
    return make_response(response, 200)