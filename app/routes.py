from app import db
from app.models.task import Task
from app.models.goal import Goal
from flask import Blueprint
from flask import Blueprint, jsonify, abort, make_response, request
from sqlalchemy import desc, asc
from datetime import datetime
import requests
import pytz
import os
from dotenv import load_dotenv

SLACK_API_KEY = os.environ.get('SLACK_API_KEY')
tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")
goals_bp = Blueprint("goals", __name__, url_prefix="/goals")

def validate_model(cls, model_id):
    try:
        model_id = int(model_id)
    except:
        abort(make_response({"message":f"{cls.__name__.lower()} {model_id} invalid"}, 400))
    
    item = cls.query.get(model_id)
    
    if not item:
        abort(make_response({"message":f"{cls.__name__.lower()} {model_id} not found"}, 404))
    
    return item

@tasks_bp.route("", methods=["GET"])
def read_all_tasks():
    sort_query = request.args.get("sort")
    if sort_query == 'asc':
        tasks = Task.query.order_by(Task.title.asc()).all()
    elif sort_query == 'desc':
        tasks = Task.query.order_by(Task.title.desc()).all()
    else:
        tasks = Task.query.all()

    tasks_response = [task.to_dict() for task in tasks]

    return jsonify(tasks_response), 200

@tasks_bp.route("/<task_id>", methods=["GET"])
def get_task(task_id):
    task = validate_model(Task, task_id)
    return {"task": task.to_dict()}, 200

@tasks_bp.route("", methods=["POST"])
def create_task():
    request_body = request.get_json()
    try:
        new_task = Task.from_dict(request_body)
    except KeyError:
        return {
        "details": "Invalid data"
        }, 400

    db.session.add(new_task)
    db.session.commit()

    return {
        "task": new_task.to_dict()
    }, 201

@tasks_bp.route("/<task_id>", methods=["PUT"])
def update_task(task_id):
    task_to_update = validate_model(Task, task_id)

    request_body = request.get_json()
    for key, value in request_body.items():
        if key == "title":
            task_to_update.title = value
        elif key == "description":
            task_to_update.description = value
        elif key == "is_complete":
            task_to_update.is_complete = value
    
    db.session.commit()

    return {
        "task": task_to_update.to_dict()
    }, 200

@tasks_bp.route("/<task_id>", methods=["DELETE"])
def delete_task(task_id):
    task_to_delete = validate_model(Task, task_id)

    db.session.delete(task_to_delete)
    db.session.commit()

    return {
        "details": f'Task {task_to_delete.id} "{task_to_delete.title}" successfully deleted'
    }, 200

@tasks_bp.route("/<task_id>/<completion_marker>", methods=["PATCH"])
def patch_task_completion(task_id, completion_marker):
    task_to_update = validate_model(Task, task_id)

    if completion_marker == 'mark_complete':
        task_to_update.completed_at = datetime.now()
        path = "https://slack.com/api/chat.postMessage"
        auth_header = {
        "Authorization": f"Bearer {SLACK_API_KEY}"
        }
        request_body = {
            "channel": "task-notifications",
            "text": f"Someone just completed the task {task_to_update.title}"
        }
        requests.post(path, headers=auth_header, data=request_body)
    elif completion_marker == 'mark_incomplete':
        task_to_update.completed_at = None

    db.session.commit()

    return {
        "task": task_to_update.to_dict()
    }, 200

# -----------------------------------------------

@goals_bp.route("", methods=["GET"])
def read_all_goals():
    sort_query = request.args.get("sort")
    if sort_query == 'asc':
        goals = Goal.query.order_by(Goal.title.asc()).all()
    elif sort_query == 'desc':
        goals = Goal.query.order_by(Goal.title.desc()).all()
    else:
        goals = Goal.query.all()

    goals_response = [goal.to_dict() for goal in goals]

    return jsonify(goals_response), 200

@goals_bp.route("/<goal_id>", methods=["GET"])
def get_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    return {"goal": goal.to_dict()}, 200

@goals_bp.route("", methods=["POST"])
def create_goal():
    request_body = request.get_json()
    try:
        new_goal = Goal.from_dict(request_body)
    except KeyError:
        return {
        "details": "Invalid data"
        }, 400

    db.session.add(new_goal)
    db.session.commit()

    return {
        "goal": new_goal.to_dict()
    }, 201

@goals_bp.route("/<goal_id>", methods=["PUT"])
def update_goal(goal_id):
    goal_to_update = validate_model(Goal, goal_id)

    request_body = request.get_json()
    for key, value in request_body.items():
        if key == "title":
            goal_to_update.title = value
    
    db.session.commit()

    return {
        "goal": goal_to_update.to_dict()
    }, 200

@goals_bp.route("/<goal_id>", methods=["DELETE"])
def delete_task(goal_id):
    goal_to_delete = validate_model(Goal, goal_id)

    db.session.delete(goal_to_delete)
    db.session.commit()

    return {
        "details": f'Goal {goal_to_delete.id} "{goal_to_delete.title}" successfully deleted'
    }, 200

@goals_bp.route("/<goal_id>/tasks", methods=["POST"])
def create_task(goal_id):
    goal = validate_model(Goal, goal_id)
    request_body = request.get_json()
    for task_id in request_body["task_ids"]:
        task = validate_model(Task, task_id)
        task.goal = goal

    db.session.commit()
    return {
        "id": goal.id,
        "task_ids": [task_id for task_id in request_body["task_ids"]]
    }, 200