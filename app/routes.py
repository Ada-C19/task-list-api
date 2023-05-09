from flask import Blueprint
from os import abort, environ
import os
from app import db
from app.models.task import Task
from flask import Blueprint, jsonify, abort, make_response, request
from datetime import datetime
import requests

tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")

def validate_task(task_id):
    try:
        task_id = int(task_id)
    except:
        abort(make_response({"message":f"task {task_id} invalid"}, 400))

    task = Task.query.get(task_id)
    if not task:
        abort(make_response({"message":f"task {task_id} not found"}, 404))

    return task
# query.get(task_id)

@tasks_bp.route("", methods=["POST"])
def create_task():
    request_body = request.get_json()

    if not "title" in request_body or not "description" in request_body:
        abort (make_response({"details": "Invalid data"}, 400))

    new_task = Task(title=request_body["title"],
                    description=request_body["description"])
                    # completed_at=request_body["completed_at"])

    db.session.add(new_task)
    db.session.commit()

    return {"task" : new_task.to_result()}, 201

@tasks_bp.route("<task_id>/mark_complete", methods=['PATCH'])
def mark_task(task_id):
    task = validate_task(task_id)
    request_body = request.get_json()

    task.completed_at = datetime.now()
    
    db.session.commit()

    slack_api = "https://slack.com/api/chat.postMessage"

    bot_info = {
        "token": os.environ.get("SLACK_PERSONAL_TOKEN"),
        "channel": "task-list",
        "text": f"Someone just completed the task{task.title}."
    }
    requests.post(slack_api, data=bot_info)

    return {"task": task.to_result()}, 200 

@tasks_bp.route("<task_id>/mark_incomplete", methods=['PATCH'])
def mark_incomp_task(task_id):
    task = validate_task(task_id)
    request_body = request.get_json()

    task.completed_at = None
    
    db.session.commit()

    return {"task": task.to_result()}, 200 

@tasks_bp.route("", methods=["GET"])
def read_all_tasks():
    tasks_response = []
    sort_query = request.args.get("sort")
    if sort_query == "asc":
        tasks = Task.query.order_by(Task.title.asc()).all()
    elif sort_query == "desc":
        tasks = Task.query.order_by(Task.title.desc()).all()
    else:
        tasks = Task.query.all()
    for task in tasks:
        tasks_response.append(task.to_result())
    return jsonify(tasks_response), 200

@tasks_bp.route("/<task_id>", methods=["GET"])
def read_one_task(task_id):
    task = validate_task(task_id)
    return {"task": task.to_result()}, 200 

@tasks_bp.route("/<task_id>", methods=["PUT"])
def update_task(task_id):
    task = validate_task(task_id)
    request_body = request.get_json()

    task.title = request_body["title"]
    task.description = request_body["description"]
    
    db.session.commit()

    return {"task": task.to_result()}, 200 

@tasks_bp.route("/<task_id>", methods=["DELETE"])
def delete_task(task_id):
    task_to_delete = validate_task(task_id)

    db.session.delete(task_to_delete)
    db.session.commit()

    # return {"details": task.to_result()}, 200 

    return make_response({"details":f'Task {task_id} "{task_to_delete.title}" successfully deleted'})


