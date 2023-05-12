from flask import Blueprint, request, jsonify, make_response, abort
from app.models.task import Task
from app import db
from datetime import datetime
import requests, os
from app.helper_functions import validate_model, create_model, sort_by_title


tasks_bp = Blueprint("tasks_db", __name__, url_prefix="/tasks")

# Create
@tasks_bp.route("", methods=["POST"])
def create_task():
    request_body = request.get_json()
    new_task = create_model(Task, request_body)
    db.session.add(new_task)
    db.session.commit()
    return make_response({"task": new_task.to_dict()}, 201)


# Read
@tasks_bp.route("", methods=["GET"])
def list_all_tasks():
    sort_query = request.args.get("sort")
    tasks = sort_by_title(Task, sort_query)
    

    tasks_response = [task.to_dict() for task in tasks]
    return jsonify(tasks_response)


@tasks_bp.route("/<task_id>", methods=["GET"])
def list_specific_task(task_id):
    task = validate_model(Task, task_id)
    return make_response({"task": task.to_dict()})


# Update
@tasks_bp.route("<task_id>", methods=["PUT"])
def update_task_info(task_id):
    task = validate_model(Task, task_id)
    request_body = request.get_json()
    task.update_data(request_body)
    db.session.commit()
    return make_response({"task": task.to_dict()})


@tasks_bp.route("<task_id>/mark_complete", methods=["PATCH"])
def mark_task_complete(task_id):
    task = validate_model(Task, task_id)
    task.completed_at = datetime.utcnow()
    db.session.commit()
    response = send_slack_message(task)

    # response.ok is a boolean value that is True if the HTTP status code is between 
    # 200 and 299 (indicating a successful request), and False otherwise
    if response.ok:
        return make_response({"task": task.to_dict()})
    else:
        return make_response({"Error message":response.text})


@tasks_bp.route("<task_id>/mark_incomplete", methods=["PATCH"])
def mark_task_incomplete(task_id):
    task = validate_model(Task, task_id)
    task.completed_at = None
    db.session.commit()
    return make_response({"task": task.to_dict()})


# Delete
@tasks_bp.route("<task_id>", methods=["DELETE"])
def delete_task(task_id):
    task = validate_model(Task, task_id)
    db.session.delete(task)
    db.session.commit()
    return make_response({"details": f"Task {task_id} \"{task.title}\" successfully deleted"})


# Helper Functions
def send_slack_message(task):
    token = os.environ.get("SLACK_BOT_TOKEN")
    external_url = 'https://slack.com/api/chat.postMessage'
    headers = {"Authorization": f"Bearer {token}"}
    data = {"channel": "task-notifications", 
            "text": f"Someone just completed the task \"{task.title}\""}
    response = requests.post(external_url, headers=headers, json=data)
    return response