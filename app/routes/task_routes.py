import requests
import os
from datetime import datetime
from flask import Blueprint, jsonify, abort, make_response, request
from dotenv import load_dotenv
from app import db
from app.models.task import Task
from .routes_helpers import validate_model

load_dotenv()

task_bp = Blueprint("tasks", __name__, url_prefix="/tasks")


# CREATE ENDPOINT
@task_bp.route("", methods=["POST"])
def create_task():
    req_body = request.get_json()

    if "title" in req_body and "description" in req_body:
        new_task = Task.from_dict(req_body)
    else:
        abort(make_response({"details": "Invalid data"}, 400))

    db.session.add(new_task)
    db.session.commit()

    return make_response(jsonify({"task": new_task.to_dict()}), 201)


# GET ALL ENDPOINT
@task_bp.route("", methods=["GET"])
def handle_tasks():
    sort_param = request.args.get("sort")
    
    if sort_param == "asc":
        task_query = Task.query.order_by(Task.title.asc())
    elif sort_param == "desc":
        task_query = Task.query.order_by(Task.title.desc())
    else:
        task_query = Task.query.all()

    tasks_response = [task.to_dict() for task in task_query]

    return jsonify(tasks_response), 200


# GET ONE ENDPOINT
@task_bp.route("/<id>", methods=["GET"])
def handle_task(id):
    task = validate_model(Task, id)

    return jsonify({"task": task.to_dict()}), 200


# UPDATE ONE ENDPOINT
@task_bp.route("/<id>", methods=["PUT"])
def update_task(id):
    task = validate_model(Task, id)

    req_body = request.get_json()

    task.title = req_body["title"]
    task.description = req_body["description"]

    db.session.commit()

    return make_response(jsonify({"task": task.to_dict()}), 200)


# DELETE ONE ENDPOINT
@task_bp.route("/<id>", methods=["DELETE"])
def delete_task(id):
    task = validate_model(Task, id)

    db.session.delete(task)
    db.session.commit()

    return make_response({"details": f"Task {task.task_id} \"{task.title}\" successfully deleted"}, 200)


# MARK TASK AS COMPLETE
@task_bp.route("/<id>/mark_complete", methods=["PATCH"])
def mark_completed(id):
    task = validate_model(Task, id)
    prev_incomplete = True if not task.completed_at else False

    task.completed_at = datetime.now()
    db.session.commit()

    if prev_incomplete:
        url = "https://slack.com/api/chat.postMessage"
        json = {
            "channel": "task-notifications",
            "text": f"Someone just completed the task {task.title}"
        }
        authorization = os.environ.get("SLACKBOT_API_KEY")

        requests.post(
            url,
            json=json,
            headers={"Authorization": f"Bearer {authorization}"}
        )

    return make_response(jsonify({"task": task.to_dict()}), 200)


# MARK TASK AS INCOMPLETE
@task_bp.route("/<id>/mark_incomplete", methods=["PATCH"])
def mark_incomplete(id):
    task = validate_model(Task, id)

    task.completed_at = None
    db.session.commit()

    return make_response(jsonify({"task": task.to_dict()}), 200)
