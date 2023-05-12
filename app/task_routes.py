from os import abort
from app import db
from app.models.task import Task
from flask import Blueprint, jsonify, abort, make_response, request
from datetime import datetime
import requests  
import os

tasks_bp = Blueprint("task", __name__, url_prefix="/tasks")


@tasks_bp.route("", methods=["POST"])
def create_task():
    request_body = request.get_json()
    if "description" not in request_body:
        return make_response(jsonify({"details": "Invalid data"}), 400)
    if "title" not in request_body:
        return make_response(jsonify({"details": "Invalid data"}), 400)
    new_task = Task.from_dict(request_body)
    db.session.add(new_task)
    db.session.commit()
    return make_response(jsonify(new_task.to_dict()), 201)


@tasks_bp.route("", methods=["GET"])
def get_tasks():
    sort_order = request.args.get("sort", "asc")
    sort_key = lambda task: task.title
    tasks = Task.query.all()
    if len(tasks) > 1:
        tasks = sorted(tasks, key=sort_key)
        if sort_order == "desc":
            tasks = reversed(tasks)
    task_list = [task.to_dict()["task"]for task in tasks]
    return make_response(jsonify(task_list), 200)


@tasks_bp.route("/<task_id>", methods=["GET"])
def read_one_task(task_id):
    task = Task.validate_task(task_id)
    return make_response(jsonify(task.to_dict()), 200)


@tasks_bp.route("/<task_id>", methods=["PUT"])
def update_task(task_id):
    task = Task.validate_task(task_id)
    request_body = request.get_json()
    task.title = request_body["title"]
    task.description = request_body["description"]
    task.completed_at = request_body.get("completed_at", None)
    db.session.commit()
    return make_response(jsonify(task.to_dict()), 200)


@tasks_bp.route("/<task_id>", methods=["DELETE"])
def delete_task(task_id):
    task = Task.validate_task(task_id)
    db.session.delete(task)
    db.session.commit()
    return make_response(jsonify({"details": f'Task {task_id} "{task.title}" successfully deleted'}))


@tasks_bp.route("/<task_id>/mark_complete", methods=["PATCH"])
def mark_complete(task_id):
    task = Task.validate_task(task_id)
    
    if task.completed_at is None:
        task.completed_at = datetime.now()
        db.session.commit()

    slack_token = os.environ.get("SLACK_TOKEN")
    if slack_token:
        channel = "#task-notifications"
        message = f'Someone just completed the task "{task.title}."'
        url = "https://slack.com/api/chat.postMessage"
        headers = {
            "Authorization": f"Bearer {slack_token}",
            "Content-Type": "application/json"
        }
        payload = {
            "channel":channel,
            "text": message
            }
        custom_headers = request.headers.get("Custom-Headers")
        if custom_headers is not None:
            headers.update(custom_headers)
        try:
            response = requests.post(url, json=payload)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            abort(make_response(jsonify({"message": "Fail to send Slack message"}), 500))

        response = requests.post(url, json=payload, headers=headers)
        print(response.status_code)  # Check the status code
        print(response.json())  # Print the response content
    return make_response(jsonify(task.to_dict()), 200)


@tasks_bp.route("/<task_id>/mark_incomplete", methods=["PATCH"])
def mark_incomplete(task_id):
    task = Task.validate_task(task_id)
    if not task:
        abort(make_response(jsonify({"message": f"Task {task_id} not found"}), 404))
    if task.completed_at is not None:
        task.completed_at = None
        db.session.commit()
    return make_response(jsonify(task.to_dict()), 200)




