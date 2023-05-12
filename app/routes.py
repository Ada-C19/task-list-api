from app import db
from app.models.task import Task
from sqlalchemy import asc, desc
from flask import Blueprint, jsonify, make_response, abort, request
import requests
from datetime import date
import os
from dotenv import load_dotenv

load_dotenv()

tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")

def validate_task(task_id):
    try:
        task_id = int(task_id)
    except:
        message = f"task {task_id} not found"
        abort(make_response({"message": message}, 400))

    task = Task.query.get(task_id)

    if not task:
        abort(make_response({"message":f"task {task_id} not found"}, 404))
    return task

@tasks_bp.route("", methods =["POST"])
def create_task():
    request_body = request.get_json()

    if "description" not in request_body or "title" not in request_body:
        abort(make_response({"details": "Invalid data"}, 400))

    new_task = Task.from_dict(request_body)
    
    db.session.add(new_task)
    db.session.commit()
    
    return make_response({"task": new_task.make_dict()}, 201)
    
@tasks_bp.route("", methods =["GET"])
def get_tasks_data():
    sort_query = request.args.get("sort")

    if sort_query == "asc":
        tasks = Task.query.order_by(asc(Task.title))
    elif sort_query == "desc":
        tasks = Task.query.order_by(desc(Task.title))
    else:
        tasks = Task.query.all()

    tasks_response = []
    for task in tasks:
        tasks_response.append(task.make_dict())
    return jsonify(tasks_response), 200


@tasks_bp.route("/<task_id>", methods =["GET"])
def get_task_data(task_id):
    task = validate_task(task_id)
    return make_response({"task": task.make_dict()}, 200)

@tasks_bp.route("/<task_id>", methods =["PUT"])
def update_task(task_id):
    task = validate_task(task_id)
    request_body = request.get_json()
    
    task.title = request_body["title"]
    task.description = request_body["description"]

    db.session.commit()

    return make_response({"task": task.make_dict()}, 200)

@tasks_bp.route("/<task_id>", methods =["DELETE"])
def delete_task(task_id):
    task = validate_task(task_id)

    db.session.delete(task)
    db.session.commit()

    message = {f"details": 'Task 1 "Go on my daily walk 🏞" successfully deleted'}
    return make_response(jsonify(message)), 200

@tasks_bp.route("/<task_id>/mark_complete", methods =["PATCH"])
def mark_complete(task_id):
    task = validate_task(task_id)
    task.completed_at = date.today()
    
    db.session.commit()
    notify_slack(task)
    
    return make_response({"task": task.make_dict()}, 200)

def notify_slack(task):
    url = "https://slack.com/api/chat.postMessage"
    body = {
    "channel": "task-notification", 
    "text": f"Someone just completed the task {task.title}"
    }
    header = {"Authorization": os.environ.get('SLACK_TOKEN'),
            "Content-Type": "application/json"}

    requests.post(url, json=body, headers=header)

@tasks_bp.route("/<task_id>/mark_incomplete", methods =["PATCH"])
def mark_incomplete(task_id):
    
    task = validate_task(task_id)

    task.completed_at = None
    
    db.session.commit()
    
    return make_response({"task": task.make_dict()}, 200)