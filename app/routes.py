from flask import Blueprint
from os import abort, environ
import os
from app import db
from app.models.task import Task
from app.models.goal import Goal
from flask import Blueprint, jsonify, abort, make_response, request
from datetime import datetime
import requests
from dotenv import load_dotenv
load_dotenv()

tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")
goals_bp = Blueprint("goals",__name__, url_prefix="/goals")

def get_valid_item_by_id(model, id):
    try:
        id = int(id)
    except:
        abort(make_response({'msg': f"Invalid id '{id}'"}, 400))

    item = model.query.get(id)

    return item if item else abort(make_response({'msg': f"No {model.__name__} with id {id}"}, 404))

@tasks_bp.route("", methods=["POST"])
def create_task():
    request_body = request.get_json()

    if not "title" in request_body or not "description" in request_body:
        abort (make_response({"details": "Invalid data"}, 400))

    new_task = Task(title=request_body["title"],
                    description=request_body["description"])
                    # completed_at=request_body["completed_at"])

    db.session.add(new_task)
    db.session.commit()

    return {"task" : new_task.to_result()}, 201

@tasks_bp.route("<task_id>/mark_complete", methods=['PATCH'])
def mark_task(task_id):
    task = get_valid_item_by_id(Task,task_id)
    request_body = request.get_json()

    task.completed_at = datetime.now()
    
    db.session.commit()

    slack_api = "https://slack.com/api/chat.postMessage"

    bot_info = {
        "token": os.environ.get("SLACK_PERSONAL_TOKEN"),
        "channel": "task-list",
        "text": f"Someone just completed the task {task.title}."
    }
    requests.post(slack_api, data=bot_info)

    return {"task": task.to_result()}, 200 

@tasks_bp.route("<task_id>/mark_incomplete", methods=['PATCH'])
def mark_incomp_task(task_id):
    task = get_valid_item_by_id(Task, task_id)
    request_body = request.get_json()

    task.completed_at = None
    
    db.session.commit()

    return {"task": task.to_result()}, 200 

@tasks_bp.route("", methods=["GET"])
def read_all_tasks():
    tasks_response = []
    sort_query = request.args.get("sort")
    if sort_query == "asc":
        tasks = Task.query.order_by(Task.title.asc()).all()
    elif sort_query == "desc":
        tasks = Task.query.order_by(Task.title.desc()).all()
    else:
        tasks = Task.query.all()
    for task in tasks:
        tasks_response.append(task.to_result())
    return jsonify(tasks_response), 200

@tasks_bp.route("/<task_id>", methods=["GET"])
def read_one_task(task_id):
    task = get_valid_item_by_id(Task, task_id)
    return {"task": task.to_result()}, 200 

@tasks_bp.route("/<task_id>", methods=["PUT"])
def update_task(task_id):
    task = get_valid_item_by_id(Task,task_id)
    request_body = request.get_json()

    task.title = request_body["title"]
    task.description = request_body["description"]
    
    db.session.commit()

    return {"task": task.to_result()}, 200 

@tasks_bp.route("/<task_id>", methods=["DELETE"])
def delete_task(task_id):
    task_to_delete = get_valid_item_by_id(Task,task_id)

    db.session.delete(task_to_delete)
    db.session.commit()

    # return {"details": task.to_result()}, 200 

    return make_response({"details":f'Task {task_id} "{task_to_delete.title}" successfully deleted'})

@goals_bp.route("", methods=["GET"])
def read_all_goals():
    goals_response = []
    goals = Goal.query.all()
    for goal in goals:
        goals_response.append(goal.to_dict())
    return jsonify(goals_response), 200

@goals_bp.route("", methods=["POST"])
def create_goal():
    request_body = request.get_json()

    if not "title" in request_body:
        abort (make_response({"details": "Invalid data"}, 400))

    new_goal = Goal(title=request_body["title"])

    db.session.add(new_goal)
    db.session.commit()

    return {"goal" : new_goal.to_dict()}, 201

@goals_bp.route("/<goal_id>", methods=["GET"])
def read_one_goal(goal_id):
    goal = get_valid_item_by_id(Goal, goal_id)
    return {"goal": goal.to_dict()}, 200 

@goals_bp.route("/<goal_id>", methods=["PUT"])
def update_goal(goal_id):
    goal = get_valid_item_by_id(Goal,goal_id)
    request_body = request.get_json()

    goal.title = request_body["title"]
    
    db.session.commit()

    return make_response({"goal": goal.to_dict()})

@goals_bp.route("/<goal_id>", methods=["DELETE"])
def delete_goal(goal_id):
    goal_to_delete = get_valid_item_by_id(Goal,goal_id)

    db.session.delete(goal_to_delete)
    db.session.commit()

    # return {"details": goal.to_result()}, 200 

    return make_response({"details":f'Goal {goal_id} "{goal_to_delete.title}" successfully deleted'})

@goals_bp.route("/<goal_id>/tasks", methods=['POST'])
def handle_all_tasks_of_one_goal(goal_id):
    goal = get_valid_item_by_id(Goal, goal_id)
    request_body=request.get_json()

    task_ids_list=request_body["task_ids"]

    for task_id in task_ids_list:
        task = get_valid_item_by_id(Task,task_id)
        task.goal_id = goal_id

    db.session.commit()

    return{
        "id": goal.goal_id, 
        "task_ids":task_ids_list
    }, 200

@goals_bp.route("/<goal_id>/tasks", methods=["GET"])
def read_one_goal_in_task(goal_id):
    goal = get_valid_item_by_id(Goal, goal_id)
    response = []
    for task in goal.tasks:
        response.append(task.to_result())
    return{
        "id": goal.goal_id,
        "title": goal.title,
        "tasks": response
    }, 200