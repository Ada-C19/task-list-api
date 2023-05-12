from flask import Blueprint, jsonify, abort, make_response, request
from sqlalchemy import asc, desc
from app import db
import requests
from app.say_bot import token
from app.models.task import Task
from app.models.goal import Goal
from datetime import datetime


tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")
goals_bp = Blueprint("goals", __name__, url_prefix="/goals")

@tasks_bp.route("", methods = ["POST"])
def create_tasks():
    request_body = request.get_json()
    try:
        new_task = Task.create_new_task(request_body)
        db.session.add(new_task)
        db.session.commit()

        message = Task.generate_message(new_task)

        return make_response(jsonify(message), 201)
    except KeyError as e:
        message = "Invalid data"
        return make_response({"details": message}, 400)

@tasks_bp.route("", methods = ["GET"])
def read_all_tasks():
    query_params = request.args.to_dict()
    tasks = filter_tasks_by_params(query_params)
    tasks_response = [task.task_to_dict() for task in tasks]
    return jsonify(tasks_response)

def filter_tasks_by_params(query_params):
    sort_by = query_params.get("sort")
    
    if sort_by:
        return get_sorted_tasks(query_params)
    
    if query_params:
        query_params = {k.lower(): v.title() for k, v in query_params.items()}
        tasks = Task.query.filter_by(**query_params).all()
    else:
        tasks = Task.query.all()
    
    return tasks

@tasks_bp.route("/<task_id>", methods=["GET"])
def read_one_task(task_id):
    task = validate_model(Task, task_id)
    task = Task.query.get(task_id)
    task = Task.generate_message(task)
    return jsonify(task), 200

@tasks_bp.route("/<task_id>", methods=["PUT"])
def update_task(task_id):
    task = validate_model(Task, task_id)
    request_body = request.get_json()
    task.update(request_body)

    db.session.commit()
    message = Task.generate_message(task)
    return make_response(jsonify(message))
          
@tasks_bp.route("/<task_id>", methods=["DELETE"])
def delete_task(task_id):
    task = validate_model(Task, task_id)
    db.session.delete(task)
    db.session.commit()

    message = {
        "details": f'Task {task_id} "{task.title}" successfully deleted'
        }
    return make_response(jsonify(message), 200)

def validate_model(cls, id):
    try:
        id = int(id)
    except:
        message = f"{cls.__name__} {id} is invalid"
        abort(make_response({"message": message}, 400))

    obj = cls.query.get(id)
    if not obj:
        abort(make_response(jsonify(message=f"{cls.__name__} not found"), 404))
    
    return obj

def get_sorted_tasks(query_params):
    sort_param = query_params.pop('sort', None)

    if sort_param == 'asc':
        return Task.query.filter_by(**query_params).order_by(Task.title.asc()).all()
    elif sort_param == 'desc':
        return Task.query.filter_by(**query_params).order_by(Task.title.desc()).all()
    else:
        return Task.query.filter_by(**query_params).order_by(Task.id.asc()).all()

@tasks_bp.route("/<task_id>/mark_complete", methods=["PATCH"])
def mark_task_complete(task_id):
    task = validate_model(Task, task_id)
    task.is_complete = True
    task.completed_at = datetime.now()
    db.session.commit()

    slack_post_message(task)
    
    message = Task.generate_message(task)
    return make_response(jsonify(message), 200)
@tasks_bp.route("/<task_id>/mark_incomplete", methods=["PATCH"])
def mark_task_incomplete(task_id):
    task = validate_model(Task, task_id)
    task.is_complete = False
    task.completed_at = None
    db.session.commit()
    message = Task.generate_message(task)
    return make_response(jsonify(message), 200)

def slack_post_message(task):
    api_url = 'http://slack.com/api/chat.postMessage'

    payload = {
        "channel": "api-test-channel",
        "text":f"Someone just completed the task {task.title}"
    }
    headers = {
        "Authorization": f"Bearer {token}"
    }
    response = requests.post(api_url, headers=headers, data=payload)

    print(response.text)

@goals_bp.route("", methods = ["POST"])
def create_goals():
    request_body = request.get_json()
    try:
        new_goal = Goal.create_new_goal(request_body)
        db.session.add(new_goal)
        db.session.commit()

        # message = Goal.generate_message(new_goal)
        message = new_goal.__str__()

        return make_response(jsonify(message), 201)
    except KeyError as e:
        message = "Invalid data"
        return make_response({"details": message}, 400)

@goals_bp.route("", methods = ["GET"])
def read_all_goals():
    goals = Goal.query.all()
    goal_response = [goal.goal_to_dict() for goal in goals]
    return jsonify(goal_response)


