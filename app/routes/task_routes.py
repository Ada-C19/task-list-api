from app import db
import os
from app.models.task import Task
import requests
from flask import Blueprint, jsonify, abort, make_response, request
from datetime import datetime
from .routes_helper import validate_model

tasks_bp = Blueprint("tasks_bp", __name__, url_prefix="/tasks")

@tasks_bp.route("", methods=["POST"])
def create_task():
    request_body = request.get_json()
    response_body= {}
    if "title" not in request_body or "description" not in request_body:
       response_body = {"details": "Invalid data"}
       return make_response(jsonify(response_body), 400)
    else:
        new_task = Task(title=request_body["title"],
                    description=request_body["description"])
    
        db.session.add(new_task)
        db.session.commit()
    
        response_body["task"]= new_task.to_dict()

    return make_response(jsonify(response_body), 201)


@tasks_bp.route("/<task_id>", methods=["GET"])
def read_one_task(task_id):
    task= validate_model(Task, task_id)
    response_body = {}
    
    response_body["task"] = task.to_dict()

    return response_body

@tasks_bp.route("/<task_id>", methods=["PUT"])
def update_task(task_id):
    task= validate_model(Task, task_id)

    request_body = request.get_json()
    response_body = {}
    task.title = request_body["title"]
    task.description = request_body["description"]

    response_body["task"] = task.to_dict()

    db.session.commit()

    return jsonify(response_body)

@tasks_bp.route("/<task_id>", methods=["DELETE"])
def delete_task(task_id):
    task = validate_model(Task, task_id)

    db.session.delete(task)
    db.session.commit()

    return make_response({"details": f'Task {task.task_id} "{task.title}" successfully deleted'})
                         
#Wave 2 endpoint
@tasks_bp.route("", methods=["GET"])
def read_all_tasks():
    title_sort_param = request.args.get('sort', default='asc')
    tasks_response=[]
    task_query = Task.query
    #tasks= Task.query.all()
    if title_sort_param == 'asc':
        task_query = Task.query.order_by(Task.title.asc()).all()
    else:
        task_query = Task.query.order_by(Task.title.desc()).all()

    tasks_response= [task.to_dict() for task in task_query]

    return jsonify(tasks_response)

#Wave 3 & 4 endpoints
@tasks_bp.route("/<task_id>/mark_complete", methods=["PATCH"])
def mark_task_as_complete(task_id):
    task = validate_model(Task, task_id)
    path = "https://slack.com/api/chat.postMessage"
    SLACK_API_KEY = os.environ.get("SLACK_API_KEY")
    
    response_body = {}
    if task.completed_at is None:
        task.completed_at = datetime.now()
    
    response_body["task"] = task.to_dict()

    db.session.commit()

    #code to send a message to Slack when a task is completed
    channel = "task-notifications"
    text = f"Someone just completed the task {task.title}"
    message_slack={
        "token": SLACK_API_KEY,
        "channel": channel,
        "text": text
    }
    response_slack = requests.post(path, message_slack)

    return jsonify(response_body) 

@tasks_bp.route("/<task_id>/mark_incomplete", methods=["PATCH"])
def mark_task_as_incomplete(task_id):
    task = validate_model(Task, task_id)

    response_body = {}
    if task.completed_at != None:
        task.completed_at = None
    
    response_body["task"] = task.to_dict()

    db.session.commit()

    return jsonify(response_body)



