from app import db
from app.models.task import Task
from app.models.goal import Goal
from flask import Blueprint, request, make_response, jsonify, abort
from datetime import datetime
import os
import requests
from dotenv import load_dotenv
load_dotenv()

tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")
goals_bp = Blueprint("goals", __name__, url_prefix="/goals")
SLACK_TOKEN = os.environ.get("SLACK_TOKEN")

def validate_model(cls, model_id):
    try:
        model_id = int(model_id)
    except:
        message = f"{cls.__name__} {model_id} invalid"
        abort(make_response({"error": message}, 400))

    model = cls.query.get(model_id)

    if not model:
        message = f"{cls.__name__} #{model_id} not found"
        abort(make_response({"error": message}, 404))

    return model

def send_slack_message(task_title):
    slack_url = "https://slack.com/api/chat.postMessage"
    headers = {
        "Authorization": f"Bearer {SLACK_TOKEN}"
    }
    data = {
        "channel": "task-notifications",
        "text": f"Someone just completed the task {task_title}"
    }

    response = requests.post(slack_url, headers=headers, data=data)
    return response

def create_item(cls):
    request_body = request.get_json()

    try: 
        new_item = cls.from_dict(request_body)
        db.session.add(new_item)
        db.session.commit()
        return make_response({cls.__name__.lower(): new_item.to_dict()}, 201)
    except:
        return make_response({"details": "Invalid data"}, 400)
    
def get_all_items(cls):
    sort_query = request.args.get("sort")

    if sort_query == "asc":
        items = cls.query.order_by(cls.title.asc())
    elif sort_query == "desc":
        items = cls.query.order_by(cls.title.desc())
    else: 
        items = cls.query.all()

    items_response = [item.to_dict() for item in items]
    return jsonify(items_response), 200

def get_item(cls, item_id):
    item = validate_model(cls, item_id)
    return make_response({cls.__name__.lower(): item.to_dict()}, 200)

def update_item(cls, item_id):
    item = validate_model(cls, item_id)
    item_data = request.get_json()

    for key, value in item_data.items():
        setattr(item, key, value)

    db.session.commit()
    
    return make_response({cls.__name__.lower(): item.to_dict()}, 200)

@tasks_bp.route("", methods=["POST"])
def create_task():
    return create_item(Task)

@tasks_bp.route("", methods=["GET"])
def get_all_tasks():
    return get_all_items(Task)

@tasks_bp.route("/<task_id>", methods=["GET"])
def get_task(task_id):
    return get_item(Task, task_id)

@tasks_bp.route("/<task_id>", methods=["PUT"])
def update_task(task_id):
    return update_item(Task, task_id)

@tasks_bp.route("/<task_id>", methods=["DELETE"])
def delete_task(task_id):
    task = validate_model(Task, task_id)

    db.session.delete(task)
    db.session.commit()

    details = f"Task {task.task_id} \"{task.title}\" successfully deleted"
    return make_response({"details": details}, 200)

@tasks_bp.route("/<task_id>/mark_complete", methods=["PATCH"])
def mark_complete(task_id):
    task = validate_model(Task, task_id)

    task.completed_at = datetime.now()
    db.session.commit()

    send_slack_message(task.title)

    return make_response({"task": task.to_dict()}, 200)

@tasks_bp.route("/<task_id>/mark_incomplete", methods=["PATCH"])
def mark_incomplete(task_id):
    task = validate_model(Task, task_id)

    task.completed_at = None
    db.session.commit()

    return make_response({"task": task.to_dict()}, 200)

@goals_bp.route("", methods=["POST"])
def create_goal():
    return create_item(Goal)

@goals_bp.route("", methods=["GET"])
def get_all_goals():
    return get_all_items(Goal)

@goals_bp.route("/<goal_id>", methods=["GET"])
def get_goal(goal_id):
    return get_item(Goal, goal_id)

@goals_bp.route("/<goal_id>", methods=["PUT"])
def update_goal(goal_id):
    return update_item(Goal, goal_id)