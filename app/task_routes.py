from app import db
from app.models.task import Task
from app.models.goal import Goal
from flask import Blueprint, jsonify, make_response, abort, request
import datetime
import requests
import os

tasks_bp = Blueprint("tasks", __name__, url_prefix = "/tasks")

###### Create Route ######
@tasks_bp.route("", methods=["POST"])
def create_task():
    request_body = request.get_json()

    if not request_body.get("title") or not request_body.get("description"):
        abort(make_response(
                {
                    "details": "Invalid data"
                }, 400
            ))

    task = Task.from_dict(request_body)

    db.session.add(task)
    db.session.commit()

    return jsonify({"task": task.to_dict()}), 201

###### Read Route ######

@tasks_bp.route("", methods=["GET"])
def read_tasks():
    
    title_query = request.args.get("sort")
    if title_query == "asc":
        tasks = Task.query.order_by(Task.title).all()
    elif title_query == "desc":
        tasks = Task.query.order_by(Task.title.desc()).all()
    else:
        tasks = Task.query.all()

    tasks_response = []
    for task in tasks:
        tasks_response.append(task.to_dict()), 200

    return jsonify(tasks_response)

@tasks_bp.route("/<task_id>", methods=["GET"])
def read_one_saved_task(task_id):
    task = validate_model(Task, task_id)

    return {"task": task.to_dict()}
    
###### Update Route ######
@tasks_bp.route("/<task_id>", methods=["PUT"])
def update_task(task_id):
    task = validate_model(Task, task_id)

    request_body = request.get_json()

    task.title = request_body["title"]
    task.description = request_body["description"]

    db.session.commit()

    return make_response({"task": task.to_dict()},200)

###### Patch Route ######
@tasks_bp.route("/<task_id>/mark_complete", methods=["PATCH"])
def mark_task_complete(task_id):
    task = validate_model(Task, task_id)

    request_body = request.get_json()

    task.completed_at = datetime.datetime.now()

    db.session.commit()

    slack_channel_id = "C0581Q2TDGQ"
    slack_url = "https://slack.com/api/chat.postMessage"

    slack_data = {
        "channel": slack_channel_id,
        "text": f"Someone completed the {task.title} task!"
    }

    headers= {
        "Authorization": f"Bearer {os.environ.get('SLACK_KEY')}"
    }
    
    slack_request = requests.post(slack_url, headers=headers, json=slack_data)
    print(slack_request.text)
    return make_response({"task": task.to_dict()}), 200

@tasks_bp.route("/<task_id>/mark_incomplete", methods=["PATCH"])
def mark_task_incomplete(task_id):
    task = validate_model(Task, task_id)

    request_body = request.get_json()

    task.completed_at = None

    db.session.commit()
                
    return make_response({"task": task.to_dict()}, 200)

###### Delete Route ######

@tasks_bp.route("/<task_id>", methods=["DELETE"])
def delete_task(task_id):
    task = validate_model(Task, task_id)

    db.session.delete(task)
    db.session.commit()

    return make_response(
        {
            "details": f"Task {task.task_id} \"{task.title}\" successfully deleted"
        }, 200
    )

def validate_model(cls, model_id):
    try:
        model_id = int(model_id)
    except:
        abort(make_response({"details":f"Invalid data"}, 400))

    model = cls.query.get(model_id)

    if not model:
        abort(make_response({"details":f"{cls.__name__} ID not found"}, 404))

    return model