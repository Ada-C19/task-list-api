from flask import Blueprint, make_response, jsonify, request, abort
from app.models.task import Task
from app import db
from datetime import datetime
import requests
from .route_helpers import validate_model
import os
from dotenv import load_dotenv

load_dotenv()

bp = Blueprint("tasks", __name__, url_prefix="/tasks")


@bp.route("", methods=["GET"])
def get_all_tasks():
    sorted_query = request.args.get("sort")
    if sorted_query == "asc":
        tasks = Task.query.order_by("title")
    elif sorted_query == "desc":
        tasks = Task.query.order_by(Task.title.desc())
    else:
        tasks = Task.query.all()

    tasks_list = [task.to_dict() for task in tasks]

    return jsonify(tasks_list), 200


@bp.route("", methods=["POST"])
def create_task():
    request_body = request.get_json()
    if "title" not in request_body or not request_body["title"] or "description" not in request_body or not request_body["description"]:
        abort(make_response({"details": "Invalid data"}, 400))

    new_task = Task(
        title=request_body["title"],
        description=request_body["description"]
    )

    db.session.add(new_task)
    db.session.commit()

    return {"task": new_task.to_dict()}, 201


@bp.route("/<id>", methods=["GET"])
def get_one_task(id):
    task = validate_model(Task, id)
    if task.goal_id:
        return {"task": task.to_dict_with_goal()}, 200
    return {"task": task.to_dict()}, 200


@bp.route("/<id>", methods=["PUT"])
def update_task(id):
    task = validate_model(Task, id)
    request_body = request.get_json()
    is_complete = request_body.get("is_complete", False)

    task.title = request_body["title"]
    task.description = request_body["description"]
    task.is_complete = is_complete

    db.session.commit()

    return {"task": task.to_dict()}, 200


@bp.route("/<id>", methods=["DELETE"])
def delete_task(id):
    task = validate_model(Task, id)

    db.session.delete(task)
    db.session.commit()

    return {"details": f'Task {id} "{task.title}" successfully deleted'}, 200


@bp.route("/<id>/mark_complete", methods=["PATCH"])
def complete_task(id):
    task = validate_model(Task, id)
    if not task.completed_at:
        task.completed_at = datetime.now()
    task.is_complete = True

    PATH = "https://slack.com/api/chat.postMessage"
    Authorization = os.environ.get(
        "Authorization")
    text = f"Someone just completed the task {task.title}"

    headers = {
        "Authorization": Authorization,
        "format": "json"
    }

    body = {
        "channel": "task-notifications",
        "text": text,
    }
    requests.post(PATH, headers=headers, json=body)

    db.session.commit()

    return {"task": task.to_dict()}, 200


@bp.route("/<id>/mark_incomplete", methods=["PATCH"])
def incomplete_task(id):
    task = validate_model(Task, id)

    if task.completed_at:
        task.completed_at = None
    task.is_complete = False

    db.session.commit()

    return {"task": task.to_dict()}, 200
