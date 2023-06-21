from flask import Blueprint, jsonify, abort, make_response, request
from app.models.task import Task
from app import db
import datetime
from app.routes.helper_routes import validate_object
import os
import requests




tasks_bp = Blueprint("tasks_bp", __name__, url_prefix="/tasks")
   
@tasks_bp.route("", methods=["GET"])
def get_all_tasks():
    
    sort_query = request.args.get("sort")

    if sort_query == "asc":
        tasks = Task.query.order_by(Task.title.asc())
    
    elif sort_query == "desc":
        tasks = Task.query.order_by(Task.title.desc())
    else:
        tasks = Task.query.all()
        
    task_dict = [task.to_dict() for task in tasks]
    return jsonify(task_dict), 200

@tasks_bp.route("/<task_id>", methods=["GET"])
def single_task(task_id):
    task = validate_object(Task,task_id)
    return jsonify({"task": task.to_dict()}), 200

@tasks_bp.route("/<task_id>", methods=["PUT"])
def update_task(task_id):
    task = validate_object(Task, task_id)

    request_body = request.get_json()

    task.title = request_body["title"]
    task.description = request_body["description"]

    db.session.commit()
    
    return jsonify({"task":task.to_dict()}), 200

@tasks_bp.route("/<task_id>", methods=["DELETE"])
def delete_single_task(task_id):
    task = validate_object(Task, task_id)

    db.session.delete(task)    
    db.session.commit()

    success_message = f"Task {task.task_id} \"{task.title}\" successfully deleted"
    return jsonify({"details": success_message}), 200


@tasks_bp.route("", methods=["POST"])
def create_task():
    request_body = request.get_json()
    try:
        new_task = Task.from_dict(request_body)
        new_task.completed_at = None
    except:
        abort(make_response({"details": "Invalid data"}, 400))
    db.session.add(new_task)
    db.session.commit()
    return {"task":new_task.to_dict()}, 201

@tasks_bp.route("/<task_id>/mark_complete", methods=["PATCH"])
def mark_task_complete(task_id):
    """Mark task specifed by id as completed and send bot message on Slack."""
    task = validate_object(Task, task_id)

    task.completed_at = datetime.datetime.now()

    db.session.commit()

    bot_data = {
        "token": os.environ.get("SLACK_TOKEN"),
        "channel": "task-notifications",
        "text": f"'{task.title}' has just been completed! 🥳"
    }

    requests.post(url="https://slack.com/api/chat.postMessage", data=bot_data)

    return {"task": task.to_dict()}, 200


@tasks_bp.route("/<task_id>/mark_incomplete", methods=["PATCH"])
def mark_task_incomplete(task_id):
    task = validate_object(Task, task_id)
    if task.completed_at is None:
        # The task is already incomplete
        return {"task": task.to_dict()}, 200
    task.completed_at = None
    db.session.commit()
    return {"task": task.to_dict()}, 200

