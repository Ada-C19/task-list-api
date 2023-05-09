
import os
import requests
from flask import Blueprint, jsonify, request, make_response
from app.models.task import Task
from app.models.goal import Goal
from app.routes_helpers import validate_model
from app import db
from datetime import datetime


tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")
goals_bp = Blueprint("goals", __name__, url_prefix="/goals")


SLACK_API_URL = "https://slack.com/api/chat/postMessage"
SLACKBOT_TOKEN = os.environ["SLACKBOT_TOKEN"]


@tasks_bp.route("", methods=["GET"])
def read_all_tasks():
    tasks = Task.query.all()
    tasks_response = [task.to_dict() for task in tasks]
    return jsonify(tasks_response)

@tasks_bp.route("", methods=["POST"])
def create_task():
    request_body = request.get_json()
    if not request_body or "title" not in request_body or "description" not in request_body:
        return make_response(jsonify({"details": "Invalid data"}), 400)
    new_task = Task(
        title=request_body["title"],
        description=request_body["description"],
        completed_at=request_body.get("completed_at")
    )
    db.session.add(new_task)
    db.session.commit()
    return make_response(jsonify({"task": new_task.to_dict()}), 201)


@tasks_bp.route("/<task_id>", methods=["GET"])
def read_one_task(task_id):
    task = validate_model(Task, task_id)
    return jsonify({"task": task.to_dict()})

@tasks_bp.route("/<task_id>", methods=["PUT"])
def update_task(task_id):
    task = validate_model(Task, task_id)
    request_body = request.get_json()
    if not request_body or "title" not in request_body or "description" not in request_body:
        return make_response(jsonify({"details": "Invalid data"}), 400)
    task.title = request_body["title"]
    task.description = request_body["description"]
    task.completed_at = request_body.get("completed_at")
    db.session.commit()
    return jsonify({"task": task.to_dict()})

@tasks_bp.route("/<task_id>", methods=["DELETE"])
def delete_task(task_id):
    task = validate_model(Task, task_id)
    db.session.delete(task)
    db.session.commit()
    return make_response(jsonify({"details": f"Task {task_id} \"{task.title}\" successfully deleted"}))



