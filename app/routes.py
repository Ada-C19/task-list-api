from app import db
from .models.task import Task
from .models.goal import Goal
from sqlalchemy import asc, desc
from datetime import datetime
from flask import Blueprint, jsonify, make_response, request, abort
import requests
import os

tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")

@tasks_bp.route("", methods=["POST"])
def create_task():
    request_body = request.get_json()
    
    if request_body.get("title") is None or request_body.get("description") is None:
        return make_response ({"details": "Invalid data"}, 400)
    
    
    new_task = Task.from_dict(request_body)

    db.session.add(new_task)
    db.session.commit()

    response = {"task": new_task.to_dict()}

    return make_response(jsonify(response), 201)

@tasks_bp.route("", methods=["GET"])
def get_all_tasks():

    order_param = request.args.get("sort")

    
    if order_param == "asc" :
        tasks = Task.query.order_by(Task.title.asc())
    elif order_param == "desc": 
        tasks = Task.query.order_by(Task.title.desc())
    else:
        tasks = Task.query.all()

    task_list=[task.to_dict()for task in tasks]

    return jsonify(task_list), 200


@tasks_bp.route("/<task_id>", methods=["GET"])
def get_one_task(task_id):

    task = validate_model(Task, task_id)
    response = {"task": task.to_dict()}

    return make_response(jsonify(response), 200)


@tasks_bp.route("/<task_id>", methods=["PUT"])
def update_task(task_id):
    task=validate_model(Task, task_id)
    request_body=request.get_json()

    if request_body.get("title") is None or request_body.get("description") is None:
        return make_response(f"Some additional information needed to update task{task.task_id}{task.title}",400)

    task.title=request_body["title"]
    task.description=request_body["description"]
    

    db.session.commit()

    response = {"task": task.to_dict()}

    return make_response(jsonify(response), 200)


@tasks_bp.route("/<task_id>", methods=["DELETE"])
def delete_task(task_id):
    task = validate_model(Task, task_id)

    db.session.delete(task)
    db.session.commit()
    response = {"details": (f"Task {task.task_id} \"{task.title}\" successfully deleted")}

    return make_response(jsonify(response), 200)

@tasks_bp.route("/<task_id>/mark_incomplete", methods=["PATCH"])
def mark_incomplete(task_id):
    task = validate_model(Task, task_id)
    
    task.completed_at = None 
    db.session.commit()
    
    response = {"task": task.to_dict()}

    return make_response(jsonify(response), 200)
    

@tasks_bp.route("/<task_id>/mark_complete", methods=["PATCH"])
def mark_complete(task_id):
    task = validate_model(Task, task_id)
    
    task.completed_at = datetime.utcnow()
    
    db.session.commit()
    
    response = {"task": task.to_dict()}

    message = f"Someone just completed the task {task.title}"

    path = "https://slack.com/api/chat.postMessage"

    SLACK_TOKEN = os.environ.get("SLACK_API_KEY")

    request_body = {
        "token": SLACK_TOKEN,
        "channel": "task-notifications",
        "text": message }

    requests.post(path, data=request_body)
    


    return make_response(jsonify(response), 200)




"""GOAL ROUTES"""

goals_bp = Blueprint("goals", __name__, url_prefix="/goals")


@goals_bp.route("", methods=["POST"])
def create_goal():
    request_body = request.get_json()
    
    if request_body.get("title") is None:
        return make_response ({"details": "Invalid data"}, 400)
        request_body = request.get_json()
    
    new_goal = Goal.from_dict(request_body)

    db.session.add(new_goal)
    db.session.commit()

    response = {"goal": new_goal.to_dict()}

    return make_response(jsonify(response), 201)


@goals_bp.route("", methods=["GET"])
def get_all_goals():
    
    goals = Goal.query.all()

    goals_list =[goal.to_dict() for goal in goals]

    return jsonify(goals_list), 200
    
    
@goals_bp.route("/<goal_id>", methods=["GET"])
def get_one_goal(goal_id):

    goal = validate_model(Goal, goal_id)
    response = {"goal": goal.to_dict()}

    return make_response(jsonify(response), 200)

@goals_bp.route("/<goal_id>", methods=["PUT"])
def update_task(goal_id):
    goal=validate_model(Goal, goal_id)
    request_body=request.get_json()

    if request_body.get("title") is None:
        return make_response(f"Some additional information needed to update goal{goal.goal_id}{goal.title}",400)

    goal.title=request_body["title"]


    db.session.commit()

    response = {"goal": goal.to_dict()}

    return make_response(jsonify(response), 200)

@goals_bp.route("/<goal_id>", methods=["DELETE"])
def delete_goal(goal_id):
    goal = validate_model(Goal, goal_id)

    db.session.delete(goal)
    db.session.commit()
    response = {"details": (f"Goal {goal.goal_id} \"{goal.title}\" successfully deleted")}

    return make_response(jsonify(response), 200)














"""HELPER FUNCTION"""
def validate_model(cls, id):
    try:
        id = int(id)
    except:
        abort(make_response({"message": f"{id} was invalid"}, 400))

    model = cls.query.get(id)

    if not model:
        abort(make_response(
            {"message": f"{cls.__name__} with id {id} was not found"}, 404))
    
    return model