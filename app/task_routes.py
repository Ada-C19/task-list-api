from flask import Blueprint, request, jsonify, abort, make_response
from app import db
from app.models.task import Task
from app.routes_helper import validate_item_by_id
from datetime import datetime
import os
import requests

# Define all routes with tasks_bp start with url_prefix (/tasks)
tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")


@tasks_bp.route("", methods=["POST"])
def create_a_task():
    
    request_body = request.get_json()
    
    try:
        new_task = Task(title=request_body["title"], description=request_body["description"])
        
    except:
        return {
            "details": "Invalid data"
        }, 400
    db.session.add(new_task)
    db.session.commit()
    
    return {
        "task": new_task.to_dict()
    }, 201


@tasks_bp.route("", methods=["GET"])
def get_saved_tasks():
    tasks = Task.query.all()
    sort_request = request.args.get("sort")
    task_response = []

    if sort_request:
        if sort_request == "asc":
            tasks = Task.query.order_by(Task.title.asc())
        if sort_request == "desc":
            tasks = Task.query.order_by(Task.title.desc())
    for task in tasks:
        task_response.append(task.to_dict())
    return jsonify(task_response), 200
    
@tasks_bp.route("/<task_id>", methods=["GET"])
def get_one_task(task_id):
    task = validate_item_by_id(Task, task_id)
    return {
        "task": task.to_dict()
    }, 200

@tasks_bp.route("/<task_id>", methods=["PUT"])
def update_one_task(task_id):
    request_body = request.get_json()
    task = validate_item_by_id(Task, task_id)
    if "title" in request_body:
        task.title = request_body["title"]
    if "description" in request_body:
        task.description = request_body["description"]
    db.session.commit()
    return {"task": task.to_dict()}, 200


@tasks_bp.route("/<task_id>", methods=["DELETE"])
def delete_one_task(task_id):
    task_to_delete = validate_item_by_id(Task, task_id)
    
    db.session.delete(task_to_delete)
    db.session.commit()
    
    return {
        "details": f'Task {task_to_delete.task_id} "{task_to_delete.title}" successfully deleted'
    }, 200
    
    
@tasks_bp.route("/<task_id>/mark_complete", methods=["PATCH"])
def mark_complete(task_id):
    slack_api = os.environ.get("SLACK_BOT_TOKEN")
    task = validate_item_by_id(Task, task_id)
    task.completed_at = datetime.now()
    db.session.commit()
    data = {
        "channel": "task-list-api",
        "token": slack_api,
        "text": f"Someone just completed the task {task.title}"
    }
    # Interact with Slack Bot API
    requests.post(url='https://slack.com/api/chat.postMessage', data=data)

    return {"task": task.to_dict()},200


@tasks_bp.route("/<task_id>/mark_incomplete", methods=["PATCH"])
def mark_incomplete(task_id):
    task = validate_item_by_id(Task, task_id)
    task.completed_at = None
    db.session.commit()
    return {"task": task.to_dict()},200

