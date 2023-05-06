from flask import Blueprint, jsonify, abort, make_response, request
from app import db
from app.models.task import Task
from datetime import datetime
import requests
from dotenv import load_dotenv
import os

bp = Blueprint("tasks", __name__, url_prefix="/tasks")

@bp.route("", methods=["GET"])
def get_tasks():
    sort_param = request.args.get("sort")

    tasks = Task.query.all()
    tasks_response = [task.to_dict() for task in tasks]
    if sort_param == "asc":
        tasks_response.sort(key=lambda task: task["title"])
    elif sort_param == "desc":
        tasks_response.sort(reverse=True, key=lambda task: task["title"])

    return make_response(jsonify(tasks_response), 200)


@bp.route("", methods=["POST"])
def create_task():
    request_body = request.get_json()
    try:
        new_task = Task.from_dict(request_body)
    except KeyError:
        abort(make_response(jsonify({"details": "Invalid data"}), 400))
    db.session.add(new_task)
    db.session.commit()

    #Check test, is this the right format to return?
    return make_response(jsonify({"task": new_task.to_dict()}), 201) 


@bp.route("/<id>", methods=["GET"])
def get_one_task(id):
    task = validate_task(id)

    return make_response(jsonify({"task": task.to_dict()}), 200)


@bp.route("/<id>", methods=["PUT"])
def update_one_task(id):
    request_body = request.get_json()
    task = validate_task(id)

    task.title = request_body["title"]
    task.description = request_body["description"]
    task.completed_at = None if not request_body.get("completed_at") else request_body["completed_at"]

    db.session.commit()

    return make_response(jsonify({"task": task.to_dict()}), 200)
        

@bp.route("/<id>", methods=["DELETE"])
def delete_one_task(id):
    task = validate_task(id)
    db.session.delete(task)
    db.session.commit()

    return make_response(jsonify({"details": f'Task {task.task_id} "{task.title}" successfully deleted'}), 200)

@bp.route("/<id>/<mark>", methods=["PATCH"])
def mark_one_task(id, mark):
    load_dotenv()
    task = validate_task(id)
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
    

def validate_task(task_id):
    try:
        task_id = int(task_id)
    except:
        abort(make_response(jsonify(f"Task {task_id} is invalid"), 400))
    task = Task.query.get(task_id)
    if not task:
        abort(make_response(jsonify(f"Task {task_id} not found"), 404))
    return task

