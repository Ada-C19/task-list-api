from flask import Blueprint, request, make_response, jsonify, abort
from app import db
from app.models.task import Task
from app.routes_helpers import validate_model
from datetime import datetime
import requests
import os


tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")

@tasks_bp.route("", methods=["POST"])
def create_task():
    request_body = request.get_json()

    if (not request_body.get("title")):
        abort(make_response({"details": "Invalid data"}, 400))

    task_data = {
        "title": request_body.get("title"),
        "description": request_body.get("description")
    }

    task = Task.from_dict(task_data)

    db.session.add(task)
    db.session.commit()

    return make_response(task.to_dict(), 201)


@tasks_bp.route("", methods=["GET"])
def read_all_tasks():
    sort_query = request.args.get("sort")

    if sort_query == "asc":
        tasks = Task.query.order_by(Task.title.asc()).all()
    elif sort_query == "desc":
        tasks = Task.query.order_by(Task.title.desc()).all()
    else:
        tasks = Task.query.all()
   
    tasks_response = [task.to_dict()["task"] for task in tasks]
   
    return jsonify(tasks_response), 200


@tasks_bp.route("/<task_id>", methods=["GET"])
def get_one_task(task_id):
    task = validate_model(Task, task_id)

    return task.to_dict(), 200
 

@tasks_bp.route("/<task_id>", methods=["PUT"])
def update_one_task(task_id):
    task = validate_model(Task, task_id)
 
    request_body = request.get_json()

    for attr, val in request_body.items():
        setattr(task, attr, val)

    db.session.add(task)
    db.session.commit()

    return make_response(task.to_dict(), 200)


@tasks_bp.route("/<task_id>", methods=["DELETE"])
def delete_one_task(task_id):
    task = validate_model(Task, task_id)

    db.session.delete(task)
    db.session.commit()

    return make_response({'details': f'Task {task_id} "{task.title}"'
                         ' successfully deleted'}, 200)


@tasks_bp.route("/<task_id>/mark_complete", methods=["PATCH"])
def mark_complete(task_id):
    task = validate_model(Task, task_id)
  
    url = "https://slack.com/api/chat.postMessage"
    payload = {
        "channel": "api-test-channel",
        "text": f"Someone just completed the task {task.title}"
    }
    headers = {"Authorization": f"Bearer {os.environ.get('SLACK_BOT_TOKEN')}"}

    if not task.completed_at:
        task.completed_at = datetime.utcnow()
        response = requests.post(url, json=payload, headers=headers)

    db.session.add(task)
    db.session.commit()

    return make_response(task.to_dict(), 200)


@tasks_bp.route("/<task_id>/mark_incomplete", methods=["PATCH"])
def mark_incomplete(task_id):
    task = validate_model(Task, task_id)

    if task.completed_at:
        task.completed_at = None

    db.session.add(task)
    db.session.commit()

    return make_response(task.to_dict(), 200)

