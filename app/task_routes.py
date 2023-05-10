from flask import Blueprint
from app import db
from app.models.task import Task
from flask import Blueprint, jsonify, make_response, request, abort
from sqlalchemy import text
from datetime import datetime
import os, requests
from .routes_helper import validate_model

tasks_bp = Blueprint("tasks", __name__, url_prefix = "/tasks")

@tasks_bp.route("", methods=["POST"])
def create_task():
    request_body = request.get_json()
    if "title" not in request_body or "description" not in request_body:
        return make_response(jsonify({"details": "Invalid data"}), 400)
    # Create a new task in the database
    new_task = Task(
        title=request_body["title"],
        description=request_body["description"],
        completed_at = None
    )

    db.session.add(new_task)
    db.session.commit()

    response_body = dict(task = new_task.to_dict())

    return jsonify(response_body), 201

@tasks_bp.route("", methods=["GET"])
def get_all_tasks():

    #WAVE 2: Sorting Tasks: By Title, Ascending
    if request.args.get("sort") == "asc":
        tasks = Task.query.order_by(text("title asc"))
    elif request.args.get("sort") == "desc":
        tasks = Task.query.order_by(text("title desc"))
    else:
        tasks = Task.query.all()

    tasks_list = [task.to_dict() for task in tasks]

    return jsonify(tasks_list), 200

@tasks_bp.route("/<task_id>", methods=["GET"])
def get_one_task(task_id):
    task =validate_model(Task, task_id)
    response_body = dict(task = task.to_dict())

    return jsonify(response_body), 200

@tasks_bp.route("/<task_id>", methods=["PUT"])
def update_task(task_id):
    task =validate_model(Task, task_id)
    request_body = request.get_json()

    task.title = request_body["title"]
    task.description =request_body["description"]

    db.session.commit()

    response_body = dict(task = task.to_dict())

    return jsonify(response_body), 200

@tasks_bp.route("/<task_id>", methods=["DELETE"])
def delete_task(task_id):
    task =validate_model(Task, task_id)

    db.session.delete(task)
    db.session.commit()

    return make_response({"details": f"Task {task.task_id} \"{task.title}\" successfully deleted"}, '200 OK')

@tasks_bp.route("/<task_id>/mark_complete", methods=["PATCH"])
def mark_complete(task_id):
    task =validate_model(Task, task_id)
    if task.completed_at == None:
        task.completed_at = datetime.utcnow()

    db.session.commit()

    URL = "https://slack.com/api/chat.postMessage"
    query_param = {"channel": "api-test-channel", "text": f"Someone just completed the task {task.title}"}
    headers = {"Authorization": os.environ.get("SLACK_BOT_TOKEN")}
    response_bot = requests.post(URL,params=query_param, headers=headers)

    response_body = dict(task = task.to_dict())
    return jsonify(response_body), 200

@tasks_bp.route("/<task_id>/mark_incomplete", methods=["PATCH"])
def mark_incomplete(task_id):
    task =validate_model(Task, task_id)
    if task.completed_at != None:
        task.completed_at = None

        db.session.commit()

    response_body = dict(task = task.to_dict())

    return jsonify(response_body), 200