from flask import Blueprint, jsonify, abort, make_response, request
import requests
import os
from sqlalchemy import text
from app.models.task import Task
from app.models.goal import Goal
from app import db
from .routes_helpers import validate_model
from datetime import datetime

bp = Blueprint("tasks", __name__, url_prefix="/tasks")
goal_bp = Blueprint("goals", __name__,url_prefix="/goals")

# GET ALL ENDPOINT
@bp.route("", methods=["GET"])
def handle_tasks():

    if request.args.get("sort") == "asc":
        tasks = Task.query.order_by(text("title asc"))
    elif request.args.get("sort") == "desc":
        tasks = Task.query.order_by(text("title desc"))

    else:
        tasks = Task.query.all()
    tasks_list = [task.to_dict() for task in tasks]

    return jsonify(tasks_list), 200


# CREATE ENDPOINT
@bp.route("", methods=["POST"])
def create_task():
    request_body = request.get_json()

    if request_body.get("title") is None or request_body.get("description") is None:
        result=dict(details='Invalid data') 
        return make_response(jsonify(result),400)

    new_task = Task.from_dict(request_body)

    db.session.add(new_task)
    db.session.commit()
    result=dict(task=new_task.to_dict()) 
    return make_response(jsonify(result),201)


# GET ONE ENDPOINT
@bp.route("/<id>", methods=["GET"])
def handle_task(id):
    task = validate_model(Task, id).to_dict()
    result=dict(task=task)
    return make_response(jsonify(result),200)


# UPDATE ONE ENDPOINT
@bp.route("/<id>", methods=["PUT"])
def update_task(id):
    task = validate_model(Task, id)
    request_body = request.get_json()

    task.title = request_body["title"]
    task.description = request_body["description"]

    db.session.commit()
    result=dict(task=task.to_dict()) 
    return make_response(jsonify(result),200)


# DELETE ONE ENDPOINT
@bp.route("/<id>", methods=["DELETE"])
def delete_task(id):
    task = validate_model(Task, id)
    result=dict(details=f'Task {task.id} "{task.title}" successfully deleted') 
    db.session.delete(task)
    db.session.commit()
    
    return make_response(jsonify(result),200)

# PATCH ONE ENDPOINT
@bp.route("/<id>/mark_complete", methods=["PATCH"])
def patch_task_complete(id):
    task = validate_model(Task, id)

    task.completed_at = datetime.now()


    db.session.commit()

    path="https://slack.com/api/chat.postMessage"
    params={
        "channel":"C057EB36R4K",
        "text": f"Task\"{task.title}\" has been completed!"
        }
    
    headers = {"Authorization": os.environ.get("SLACK_API_KEY")}
    response = requests.post(path,params=params,headers=headers)
    

    return jsonify({"task":task.to_dict()}),200

    #result=dict(task=task.to_dict()) 
    #return make_response(jsonify(result),200)

@bp.route("/<id>/mark_incomplete", methods=["PATCH"])
def patch_task_incomplete(id):
    task = validate_model(Task, id)

    task.completed_at = None


    db.session.commit()
    result=dict(task=task.to_dict()) 
    return make_response(jsonify(result),200)

#****************************GOAL ROUTES***********************

# GET ALL ENDPOINT
@goal_bp.route("", methods=["GET"])
def handle_goals():
    goals = Goal.query.all()
    goals_list = [goal.to_dict() for goal in goals]

    return jsonify(goals_list), 200


# CREATE ENDPOINT
@goal_bp.route("", methods=["POST"])
def create_goal():
    request_body = request.get_json()

    if request_body.get("title") is None:
        result=dict(details='Invalid data') 
        return make_response(jsonify(result),400)

    new_goal = Goal.from_dict(request_body)

    db.session.add(new_goal)
    db.session.commit()
    result=dict(goal=new_goal.to_dict()) 
    return make_response(jsonify(result),201)


# GET ONE ENDPOINT
@goal_bp.route("/<goal_id_parent>", methods=["GET"])
def handle_goal(goal_id_parent):
    goal = validate_model(Goal, goal_id_parent)
    result=dict(goal=goal.to_dict())
    return make_response(jsonify(result),200)


# UPDATE ONE ENDPOINT
@goal_bp.route("/<goal_id_parent>", methods=["PUT"])
def update_goal(goal_id_parent):
    goal = validate_model(Goal, goal_id_parent)
    request_body = request.get_json()

    goal.title = request_body["title"]

    db.session.commit()
    result=dict(goal=goal.to_dict()) 
    return make_response(jsonify(result),200)


# DELETE ONE ENDPOINT
@goal_bp.route("/<goal_id_parent>", methods=["DELETE"])
def delete_goal(goal_id_parent):
    goal = validate_model(Goal, goal_id_parent)
    result=dict(details=f'Goal {goal.goal_id} "{goal.title}" successfully deleted') 
    db.session.delete(goal)
    db.session.commit()
    
    return make_response(jsonify(result),200)

#****************************ONE TO MANY***********************


# CREATE TASK BY GOAL ENDPOINT
@goal_bp.route("/<goal_id_parent>/tasks", methods=["POST"])
def create_task(goal_id_parent):
    goal = validate_model(Goal,goal_id_parent)
    request_body = request.get_json()

    tasks_list_dict = request_body
    for task_id in tasks_list_dict["task_ids"]:
        task=validate_model(Task,task_id)
        task.goal=goal

    db.session.commit()
    result=dict(id=goal.goal_id,
                task_ids=tasks_list_dict["task_ids"])

    return make_response(jsonify(result), 200)

# GET ALL TASKS BY GOAL ENDPOINT
@goal_bp.route("/<goal_id_parent>/tasks", methods=["GET"])
def handle_tasks_from_goal(goal_id_parent):
    goal = validate_model(Goal,goal_id_parent)
    tasks=goal.tasks
    tasks_lists = [validate_model(Task,task.id).to_dict() for task in tasks]

    for task_dict in tasks_lists:
        task_dict["goal_id"]=int(goal_id_parent)

    result = dict(id=goal.goal_id,
                    title=goal.title,
                    tasks=tasks_lists)
    
    return make_response(jsonify(result),200)

    





