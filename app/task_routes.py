from app import db
from app.models.task import Task
from flask import Blueprint, jsonify, make_response, request, abort
import datetime
from sqlalchemy.orm.exc import NoResultFound
import os
import requests
from app.helper_functions import validate_model, create_model


task_bp = Blueprint("task_bp", __name__, url_prefix="/tasks")

@task_bp.route("", methods=["POST"])
def creat_task():
    request_body = request.get_json()
    new_task =  create_model(request_body, Task)

    if "title" not in request_body or "description" not in request_body or request_body["description"] is None:
        abort(make_response(jsonify({"details": "Invalid data"}), 400))

    return make_response(jsonify({
        "task": {
            "id": new_task.task_id,
            "title": new_task.title,
            "description": new_task.description,
            "is_complete": False
        }
    }), 201)


@task_bp.route("", methods=["GET"])
def read_all_tasks():
    task_query = Task.query
    title_query = request.args.get("sort")

    if title_query == "asc":
        task_query = Task.query.order_by(Task.title.asc())
    if title_query == "desc":
        task_query = Task.query.order_by(Task.title.desc())

    tasks = task_query.all()
    task_response = []
    for task in tasks:
        task_response.append(task.to_dict())

    return jsonify(task_response)


@task_bp.route("/<task_id>", methods=["GET"])
def read_one_task(task_id):
    task = validate_model(Task, task_id)
    return jsonify({"task": task.to_dict()}), 200


@task_bp.route("/<task_id>", methods=["PUT"])
def update_task(task_id):
    task = validate_model(Task, task_id)
    request_body = request.get_json()

    if "title" not in request_body or "description" not in request_body or request_body["description"] is None:
        abort(make_response(jsonify({"details": "Invalid data"}), 400))

    task.title = request_body["title"],
    task.description = request_body["description"],
    task.is_complete = False

    db.session.commit()

    return make_response(jsonify({
        "task": {
            "id": task.task_id,
            "title": task.title,
            "description": task.description,
            "is_complete": False
        }
    }), 200)


@task_bp.route("/<task_id>", methods=["DELETE"])
def delete_task(task_id):
    task = validate_model(Task, task_id)

    db.session.delete(task)
    db.session.commit()

    return make_response(jsonify({"details": f"Task 1 \"{task.title}\" successfully deleted"})), 200

@task_bp.route("<task_id>/mark_complete", methods=["PATCH"])
def mark_complete(task_id):
    slack_channel = "#tasks-notifications"
    slack_token = os.environ.get("SLACK_TOLKEN")

    task = validate_model(Task, task_id)
    
    if task.completed_at is None:
        task.completed_at = datetime.datetime.now()
        db.session.commit()

    requests.post("https://slack.com/api/chat.postMessage", data={
        "token": slack_token,
        "channel": slack_channel,
        "text": f"Someone just completed the task {task.title}"
    })
    
    task_data = task.to_dict()
    if task.completed_at:
        task_data["completed_at"] = task.completed_at.strftime('%m-%d-%Y')

    task_data.pop("completed_at", None)
    
    return make_response(jsonify({
        "task": task_data
    }), 200)


@task_bp.route("<task_id>/mark_incomplete", methods=["PATCH"])
def mark_incomplete(task_id):
    task = validate_model(Task, task_id)

    if task.completed_at is not None:
        task.completed_at = None
        db.session.commit()
    
    task_data = task.to_dict()

    task_data.pop("completed_at", None)
    
    return make_response(jsonify({
        "task": task_data
    }), 200)