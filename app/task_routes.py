from flask import Blueprint, jsonify, abort, make_response, request
from app import db
from app.models.task import Task
from .route_helpers import validate_model
from datetime import datetime
from sqlalchemy import exc
import requests
from dotenv import load_dotenv
import os

bp = Blueprint("tasks", __name__, url_prefix="/tasks")

@bp.route("", methods=["GET"])
def get_tasks():
    sort_param = request.args.get("sort")
    order_param = request.args.get("order")

    tasks = Task.query.all()
    
    if sort_param == "title":
        column = Task.title
    elif sort_param == "id":
        column = Task.id
    else:
        return abort(make_response(jsonify(f"Tasks cannot be sorted by {sort_param}"), 400))
    
    if order_param == "asc":
        tasks = Task.query.order_by(column.asc())
    elif order_param == "desc":
        tasks = Task.query.order_by(column.desc())
    else:
        return abort(make_response(jsonify(f"Tasks cannot be ordered by {order_param}"), 400))
    
    tasks_response = [task.to_dict() for task in tasks]
    
    return make_response(jsonify(tasks_response), 200)


@bp.route("", methods=["POST"])
def create_task():
    request_body = request.get_json()

    try:
        new_task = Task.from_dict(request_body)
    except KeyError:
        abort(make_response(jsonify({"details": "Invalid data"}), 400))
    
    db.session.add(new_task)
    
    try:
        db.session.commit()
    except exc.DataError: # Catches invalid datetime data submitted to "completed_at"
        abort(make_response(jsonify({"details": "Invalid datetime data"}), 400))

    return make_response(jsonify({f"task": new_task.to_dict()}), 201) 


@bp.route("/<id>", methods=["GET"])
def get_one_task(id):
    task = validate_model(Task, id)

    return make_response(jsonify({"task": task.to_dict()}), 200)


@bp.route("/<id>", methods=["PUT"])
def update_one_task(id):
    request_body = request.get_json()
    task = validate_model(Task, id)

    task.title = request_body["title"]
    task.description = request_body["description"]
    task.completed_at = None if not request_body.get("completed_at") else request_body["completed_at"]

    try:
        db.session.commit()
    except exc.DataError: # Catches invalid datetime values for completed_at
        abort(make_response(jsonify({"details": "Invalid datetime data"}), 400))

    return make_response(jsonify({"task": task.to_dict()}), 200)
        

@bp.route("/<id>", methods=["DELETE"])
def delete_one_task(id):
    task = validate_model(Task, id)
    
    db.session.delete(task)
    db.session.commit()

    return make_response(jsonify({"details": f'Task {task.id} "{task.title}" successfully deleted'}), 200)


@bp.route("/<id>/<mark>", methods=["PATCH"])
def mark_one_task(id, mark):
    load_dotenv()
    task = validate_model(Task, id)
    if mark == "mark_complete":
        task.completed_at = datetime.now()
        path = "https://slack.com/api/chat.postMessage"
        SLACK_TOKEN = os.environ.get("SLACK_TOKEN")
        headers = {"Authorization": f"Bearer {SLACK_TOKEN}"}
        params = {"channel": "task-notifications",
                        "text": f"Someone just completed the task {task.title}"
        }
        requests.post(path, params=params, headers=headers)    
    elif mark == "mark_incomplete":
        task.completed_at = None

    db.session.commit()

    return make_response(jsonify({"task": task.to_dict()}), 200)
    



