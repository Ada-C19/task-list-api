from flask import Blueprint, request, jsonify, abort, make_response
from app.models.task import Task
from app import db
from datetime import datetime
import os
import requests

# Define all routes with tasks_bp start with url_prefix (/tasks)
tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")

# @blueprint_name.route("/endpoint/path/here", methods=["GET"])
# def endpoint_name():
#     my_beautiful_response_body = "Hello, World!"
#     return my_beautiful_response_body
def validate_task(task_id):
    try:
        task_id = int(task_id)
    except:
        abort(make_response({"msg": f"Invalid id '{task_id}'"}, 400))
    task = Task.query.get(task_id)
    return task if task else abort(make_response({"msg": f"Na task with task id '{task_id}'"}, 404))
        
@tasks_bp.route("", methods=["POST"])
def create_a_task():
    
    request_body = request.get_json()
    
    try:
        new_task = Task(title=request_body["title"], description=request_body["description"])
    except KeyError:
        return {
            "details": "Invalid data"
        }, 400
    db.session.add(new_task)
    db.session.commit()
    
    return {
        "task": new_task.to_dict()
    }, 201

# @tasks_bp.route("", methods=["GET"])
# def get_tasks_asc_sort():
#     sort_asc = request.args.get("sort=asc")
#     sort_desc = request.args.get("sort=desc")
#     if sort_asc:
#         tasks = Task.query.order_by(Task.title.asc())
#     if sort_desc:
#         tasks = Task.query.order_by(Task.title.desc())
#     return tasks

@tasks_bp.route("", methods=["GET"])
def get_saved_tasks():
    tasks = Task.query.all()
    sort_request = request.args.get("sort")
    task_response = []
    if tasks:
        if sort_request:
            if sort_request == "asc":
                tasks = Task.query.order_by(Task.title.asc())
            elif sort_request == "desc":
                tasks = Task.query.order_by(Task.title.desc())
        for task in tasks:
            task_response.append(task.to_dict())
    return jsonify(task_response), 200
    
@tasks_bp.route("/<task_id>", methods=["GET"])
def get_one_task(task_id):
    task = validate_task(task_id)
    return {
        "task": task.to_dict()
    }, 200

@tasks_bp.route("/<task_id>", methods=["PUT"])
def update_one_task(task_id):
    request_body = request.get_json()
    task = validate_task(task_id)
    if "title" in request_body:
        task.title = request_body["title"]
    if "description" in request_body:
        task.description = request_body["description"]
    db.session.commit()
    return {"task": task.to_dict()}, 200

@tasks_bp.route("/<task_id>", methods=["DELETE"])
def delete_one_task(task_id):
    task_to_delete = validate_task(task_id)
    
    db.session.delete(task_to_delete)
    db.session.commit()
    
    return {
        "details": f'Task {task_to_delete.task_id} "{task_to_delete.title}" successfully deleted'
    }, 200
    
@tasks_bp.route("/<task_id>/mark_complete", methods=["PATCH"])
def mark_complete(task_id):
    slack_api = os.environ.get("SLACK_BOT_TOKEN")
    task = validate_task(task_id)
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
    task = validate_task(task_id)
    task.completed_at = None
    db.session.commit()
    return {"task": task.to_dict()},200