from flask import Blueprint, request, make_response, jsonify, abort
from app.models.task import Task
from app import db
from .routes_helpers import validate_model, delete_message
from datetime import date
import requests
import os
from dotenv import load_dotenv

load_dotenv()

tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")

# CREATE TASK ENDPOINT
@tasks_bp.route("", methods=["POST"])
def create_task():
    request_body = request.get_json()

    if not request_body.get("title") or not request_body.get("description"):
        abort(make_response({"details": "Invalid data"}, 400))

    new_task = Task.from_dict(request_body)
    
    db.session.add(new_task)
    db.session.commit()

    return make_response({"task": new_task.to_dict()}, 201)

# GET TASKS ENDPOINT
@tasks_bp.route("", methods=["GET"])
def read_tasks():
    sort_query = request.args.get("sort")

    if not sort_query:
        tasks = Task.query.all()
    elif sort_query.lower() == "asc":
        tasks = Task.query.order_by(Task.title).all()
    elif sort_query.lower() == "desc":
        tasks = Task.query.order_by(Task.title.desc()).all()

    try:
        tasks_response = [task.to_dict() for task in tasks]
    except:
        abort(make_response({"message": f"{sort_query} query invalid"}, 400))

    return jsonify(tasks_response)

# GET ONE TASK ENDPOINT
@tasks_bp.route("/<task_id>", methods=["GET"])
def read_one_task(task_id):
    task = validate_model(Task, task_id)

    return {"task": task.to_dict()}

# UPDATE TASK ENDPOINT
@tasks_bp.route("/<task_id>", methods=["PUT"])
def update_task(task_id):
    request_body = request.get_json()

    task = validate_model(Task, task_id)

    task.title = request_body["title"]
    task.description = request_body["description"]

    db.session.commit()

    return {"task": task.to_dict()}

@tasks_bp.route("/<task_id>/mark_complete", methods=["PATCH"])
def mark_complete(task_id):
    task = validate_model(Task, task_id)
    
    path = "https://slack.com/api/chat.postMessage"

    SLACK_API_TOKEN = os.environ.get("SLACK_API_TOKEN")

    args = {
        "token": SLACK_API_TOKEN,
        "channel": "C0561UUDX4K",
        "text": f"Someone just completed the task {task.title}"
    }

    task.completed_at = date.today()

    db.session.commit()

    requests.post(path, data=args)

    return {"task": task.to_dict()}

@tasks_bp.route("/<task_id>/mark_incomplete", methods=["PATCH"])
def mark_incomplete(task_id):
    task = validate_model(Task, task_id)

    task.completed_at = None
    
    db.session.commit()

    return {"task": task.to_dict()}

# DELETE TASK ENDPOINT
@tasks_bp.route("/<task_id>", methods=["DELETE"])
def delete_task(task_id):
    task = validate_model(Task, task_id)

    db.session.delete(task)
    db.session.commit()

    return delete_message(Task, task)