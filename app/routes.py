from os import abort
from app import db
from app.models.task import Task
from flask import Blueprint, jsonify, abort, make_response, request
from sqlalchemy import asc, desc
from datetime import datetime
# from slack_sdk import WebClient
# from slack_sdk.errors import SlackApiError
import os
import requests
from app.models.goal import Goal
import requests, json




tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")
goals_bp = Blueprint("goals", __name__, url_prefix="/goals")

def validate_model(cls, model_id):
    try:
        model_id = int(model_id)
    except:
        abort(make_response({"message":f"task {model_id} invalid"}, 400))

    model = cls.query.get(model_id)
    
    if not model:
        abort(make_response({"message":f"{cls.__name__} {model_id} not found"}, 404))
    
    return model


@tasks_bp.route("", methods=["POST"])
def create_task():
    request_body = request.get_json()
    try:
        new_task = Task.from_dict(request_body)

    except:
        abort(make_response({"details": "Invalid data"}, 400))

    db.session.add(new_task)
    db.session.commit()

    
    return make_response(jsonify({"task": new_task.to_dict()}),201)

@tasks_bp.route("", methods=["GET"])

def read_all_tasks():
    title_query = request.args.get("title")
    sort_filter = request.args.get("sort")
    
    if title_query:
        tasks = Task.query.filter_by(title=title_query)
    else:
        tasks = Task.query.all()

    if sort_filter:
        if sort_filter == "asc":
            tasks = Task.query.order_by(Task.title.asc())
        elif sort_filter == "desc":
            tasks = Task.query.order_by(Task.title.desc())
    else:
        tasks = Task.query.all()
    
    tasks_response = []
    for task in tasks:
        tasks_response.append(task.to_dict())
    
    return jsonify(tasks_response)

@tasks_bp.route("/<task_id>", methods=["GET"])

def read_one_task(task_id):
    task = validate_model(Task, task_id)
    if task.goal_id:
        return {"task": task.to_dict_with_goal()}
    else:
        return {"task": task.to_dict()}

@tasks_bp.route("/<task_id>", methods=["PUT"])
def update_task(task_id):
    task = validate_model(Task, task_id)

    request_body = request.get_json()

    task.title = request_body["title"]
    task.description = request_body["description"]

    db.session.commit()

    return {"task": task.to_dict()}

@tasks_bp.route("/<task_id>", methods=["DELETE"])
def delete_task(task_id):
    task = validate_model(Task, task_id)

    
    db.session.delete(task)
    db.session.commit()

    return make_response({"details":f'Task {task.task_id} "{task.title}" successfully deleted'})

@tasks_bp.route("/<task_id>/mark_complete", methods=["PATCH"])
def mark_task_complete(task_id):
    
    task = validate_model(Task, task_id)
    
    task.completed_at = datetime.utcnow()

#use requests instead of WebClient and add bearer... add token to .env look up requests.post
    # client = WebClient(token=os.environ.get("slack_token"))
    # client.chat_postMessage(channel="C0570RZGHDL", text=f"Someone just completed the task {task.title}")

    # payload = {"text":f"Someone just completed the task {task.title}"}
    # url = os.environ.get("SLACK_URL")

    # requests.post(url, json.dumps(payload))
    # token = os.environ.get("slack_token")
    # url="https://slack.com/api/chat.postMessage"
    # data = {

    #     "token": f"{token}",
    #     "channel": 'C0570RZGHDL',
    #     "text": f"Someone just completed the task {task.title}", 
    # }

    # response = requests.post(
    #      url=url, data=data,
    #      headers={})

    
    



   
   
    db.session.commit()

    return {"task": task.to_dict()}

@tasks_bp.route("/<task_id>/mark_incomplete", methods=["PATCH"])
def mark_task_incomplete(task_id):
    
    task = validate_model(Task, task_id)
    
    if task.completed_at:
        task.completed_at = None
        

    db.session.commit()

    return {"task": task.to_dict()}


@goals_bp.route("", methods=["POST"])
def create_goal():
    request_body = request.get_json()
    try:
        new_goal = Goal.from_dict_goals(request_body)

    except:
        abort(make_response({"details": "Invalid data"}, 400))

    db.session.add(new_goal)
    db.session.commit()

    
    return make_response(jsonify({"goal": new_goal.to_dict_goals()}),201)

@goals_bp.route("", methods=["GET"])

def read_all_goals():
    title_query = request.args.get("title")
    sort_filter = request.args.get("sort")
    
    if title_query:
        goals = Goal.query.filter_by(title=title_query)
    else:
        goals = Goal.query.all()

    if sort_filter:
        if sort_filter == "asc":
            goals = Goal.query.order_by(Goal.title.asc())
        elif sort_filter == "desc":
            goals = Goal.query.order_by(Goal.title.desc())
    else:
        goals = Goal.query.all()
    
    goals_response = []
    for goal in goals:
        goals_response.append(goal.to_dict_goals())
    
    return jsonify(goals_response)

@goals_bp.route("/<goal_id>", methods=["GET"])

def read_one_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    return {"goal": goal.to_dict_goals()}

@goals_bp.route("/<goal_id>", methods=["PUT"])
def update_goal(goal_id):
    goal = validate_model(Goal, goal_id)

    request_body = request.get_json()

    goal.title = request_body["title"]
    

    db.session.commit()

    return {"goal": goal.to_dict_goals()}

@goals_bp.route("/<goal_id>", methods=["DELETE"])
def delete_goal(goal_id):
    goal = validate_model(Goal, goal_id)

    
    db.session.delete(goal)
    db.session.commit()

    return make_response({"details":f'Goal {goal.goal_id} "{goal.title}" successfully deleted'})

@goals_bp.route("/<goal_id>/tasks", methods=["POST"])
def create_goal_by_id(goal_id):
    goal = validate_model(Goal, goal_id)
    request_body = request.get_json()

    for task in request_body["task_ids"]:
        task = validate_model(Task, task)
        goal.tasks.append(task)
    
    db.session.commit()
    return {
        "id": goal.goal_id,
        "task_ids": request_body["task_ids"]
    }


@goals_bp.route("/<goal_id>/tasks", methods=["GET"])
def get_all_tasks_with_id(goal_id):
    goal = validate_model(Goal, goal_id)

    # return {"goal": goal.to_dict_goals_tasks()}

    goals_tasks = {
        "id": goal.goal_id,
        "title": goal.title,
        "tasks": []

    }

    for task in goal.tasks:
        goals_tasks["tasks"].append(task.to_dict_with_goal
        ())

    return jsonify(goals_tasks), 200

    

    


    
    
