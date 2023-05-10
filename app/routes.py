from datetime import date
from flask import Blueprint, make_response, request, jsonify, abort
from app import db
from app.models.task import Task
import requests, os

tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")

#Add a task
@tasks_bp.route("", methods=["POST"])
def add_task():
    request_body = request.get_json()
    try:
        new_task = Task.from_dict(request_body)
    except KeyError:
        abort(make_response(jsonify({"details": "Invalid data"}), 400))

    db.session.add(new_task)
    db.session.commit()

    return make_response(jsonify({"task": new_task.to_dict()}), 201)

#Read all tasks
@tasks_bp.route("", methods=["GET"])
def read_all_tasks():
    sort_param = request.args.get("sort")
    tasks = Task.query

    if sort_param == "asc":
        tasks = tasks.order_by(Task.title.asc())
    if sort_param == "desc":
        tasks = tasks.order_by(Task.title.desc())

    task_list = [task.to_dict() for task in tasks]

    return make_response(jsonify(task_list), 200)

#Read one task by ID
@tasks_bp.route("/<task_id>", methods=["GET"])
def read_one_task(task_id):
    task = Task.validate_model(task_id)
    return make_response(jsonify({"task": task.to_dict()}), 200)

#Update an existing task
@tasks_bp.route("/<task_id>", methods=["PUT"])
def update_task(task_id):
    task = Task.validate_model(task_id)
    request_body = request.get_json()
    task.title = request_body["title"]
    task.description = request_body["description"]
    task.is_complete = request_body.get("is_complete", False)

    db.session.commit()

    return make_response(jsonify({"task": task.to_dict()}), 200)

#Delete a task
@tasks_bp.route("/<task_id>", methods=["DELETE"])
def delete_task(task_id):
    task = Task.validate_model(task_id)

    db.session.delete(task)
    db.session.commit()

    return make_response(jsonify({"details": f"Task {task.task_id} \"{task.title}\" successfully deleted"}))

#Mark a task as complete
@tasks_bp.route("/<task_id>/mark_complete", methods=["PATCH"])
def mark_task_complete(task_id):
    task = Task.validate_model(task_id)
    task.completed_at = date.today()

    db.session.commit()

    #Send HTTP request to Slack
    TOKEN = os.environ.get("BOT_TOKEN")
    SLACK_URL = "https://slack.com/api/chat.postMessage"
    header = {"Authorization": f"Bearer {TOKEN}"}
    message_body = {
        "channel": "task-notifications",
        "text": f"Someone just completed the task {task.title}"
    }
    requests.post(SLACK_URL, headers=header, json=message_body)

    return make_response(jsonify({"task": task.to_dict()}), 200)

#Mark a task as incomplete
@tasks_bp.route("/<task_id>/mark_incomplete", methods=["PATCH"])
def mark_task_incomplete(task_id):
    task = Task.validate_model(task_id)
    task.completed_at = None

    db.session.commit()

    return make_response(jsonify({"task": task.to_dict()}), 200)
