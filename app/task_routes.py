from flask import Blueprint
from app import db
from app.models.task import Task
from flask import Blueprint, jsonify, make_response, request, abort
from sqlalchemy import text
from datetime import datetime
import os, requests

tasks_bp = Blueprint("tasks", __name__, url_prefix = "/tasks")
def validate_task(task_id):
    try:
        task_id = int(task_id)
    except:
        abort(make_response({"message":f"Task {task_id} invalid"}, 400 ))

    task = Task.query.get(task_id)

    if not task:
        abort(make_response({"message":f"Task {task_id} not found"}, 404))

    return task

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
    task = validate_task(task_id)
    response_body = dict(task = task.to_dict())

    return jsonify(response_body), 200

@tasks_bp.route("/<task_id>", methods=["PUT"])
def update_task(task_id):
    task = validate_task(task_id)
    request_body = request.get_json()

    task.title = request_body["title"]
    task.description =request_body["description"]
    #task.completed_at = request_body[ "completed_at"]

    db.session.commit()

    response_body = dict(task = task.to_dict())

    return jsonify(response_body), 200
