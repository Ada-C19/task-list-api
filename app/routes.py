from flask import Blueprint, abort, jsonify, make_response, request
from app import db
from app.models.task import Task
from app.models.goal import Goal
import datetime
from dotenv import load_dotenv
import requests
import os

load_dotenv()

task_bp = Blueprint("tasks", __name__, url_prefix="/tasks")
goal_bp = Blueprint("goals", __name__, url_prefix="/goals")

# validation helper function

def validate_item(model, item_id):
    try:
        item_id = int(item_id)
    except ValueError:
        abort(make_response({"msg": f"{model.__name__} {item_id} invalid"}, 400))
    
    item = model.query.get(item_id)
    
    if not item:
        abort(make_response({"msg": f"{model.__name__} {item_id} not found"}, 404))
    
    return item

# Task model routes

@task_bp.route("", methods=["POST"])
def add_task():
    request_body = request.get_json()
    try:
        new_task = Task.from_dict(request_body)
    except KeyError:
        return {
            "details": "Invalid data"
        }, 400

    db.session.add(new_task)
    db.session.commit()

    return {"task": new_task.to_dict()}, 201

@task_bp.route("", methods=["GET"])
def get_tasks():
    response = []

    title_query = request.args.get("title")
    sort_query = request.args.get("sort")

    if title_query:
        tasks = Task.query.filter_by(title=title_query)
    elif sort_query == "asc":
        tasks = Task.query.order_by(Task.title)
    elif sort_query == "desc":
        tasks = Task.query.order_by(Task.title.desc())
    else:
        tasks = Task.query.all()
    
    #refactor to do list comprehension
    for task in tasks: 
        response.append(task.to_dict())

    
    print(tasks)

    return (jsonify(response), 200)

@task_bp.route("/<task_id>", methods=["GET"])
def get_one_task(task_id):
    task = validate_item(Task, task_id)

    if task.goal_id:
        return {"task":task.to_dict_with_goal()}, 200

    return {"task":task.to_dict()}, 200 

@task_bp.route("/<task_id>", methods=["PUT"])
def update_task(task_id):
    task = validate_item(Task,task_id)

    request_body = request.get_json()

    task.title = request_body["title"]
    task.description = request_body["description"]

    db.session.commit()

    return {"task":task.to_dict()}, 200

@task_bp.route("/<task_id>", methods=["DELETE"])
def delete_task(task_id):
    task = validate_item(Task, task_id)

    db.session.delete(task)
    db.session.commit()

    return {'details': f'Task {task.task_id} "{task.title}" successfully deleted'}, 200

@task_bp.route("/<task_id>/mark_complete", methods=["PATCH"])
def mark_complete(task_id):
    task = validate_item(Task,task_id)

    task.completed_at = datetime.datetime.now()

    db.session.commit()

    data_bot = {
        "token": os.environ.get("SLACKBOT_TOKEN_API"),
        "channel": "task-notifications",
        "text": f"Someone just completed the task {task.title}"
    }

    requests.post(url="https://slack.com/api/chat.postMessage", data=data_bot)

    return {"task": task.to_dict()}, 200

@task_bp.route("/<task_id>/mark_incomplete", methods=["PATCH"])
def mark_incomplete(task_id):
    task = validate_item(Task,task_id)

    task.completed_at = None

    db.session.commit()

    return {"task": task.to_dict()}, 200

# Goal model routes

@goal_bp.route("", methods=["POST"])
def add_goal():
    request_body = request.get_json()
    try:
        new_goal = Goal.from_dict(request_body)
    except KeyError:
        return  {
            "details": "Invalid data"
        }, 400

    db.session.add(new_goal)
    db.session.commit()

    return {"goal": new_goal.to_dict()}, 201

@goal_bp.route("", methods=["GET"])
def get_goals():
    response = []

    all_goals = Goal.query.all()

    for goal in all_goals:
        response.append(goal.to_dict())
    
    return jsonify(response), 200

@goal_bp.route("/<goal_id>", methods=["GET"])
def get_one_goal(goal_id):
    goal = validate_item(Goal, goal_id)

    return {"goal": goal.to_dict()}, 200

@goal_bp.route("/<goal_id>", methods=["PUT"])
def update_goal(goal_id):
    goal = validate_item(Goal, goal_id)

    request_body = request.get_json()

    goal.title = request_body["title"]

    db.session.commit()

    return {"goal": goal.to_dict()}, 200

@goal_bp.route("/<goal_id>", methods=["DELETE"])
def delete_goal(goal_id):
    goal = validate_item(Goal, goal_id)

    db.session.delete(goal)
    db.session.commit()

    return {'details': f'Goal {goal.goal_id} "{goal.title}" successfully deleted'}, 200


@goal_bp.route("/<goal_id>/tasks", methods=["POST"])
def add_task_to_goal(goal_id):
    goal = validate_item(Goal, goal_id)

    # getting the list of task ids from the request body
    request_body = request.get_json()

    for task_id in request_body["task_ids"]:
        task = validate_item(Task, task_id)
        task.goal_id = goal_id
        db.session.add(task)

    # iterate through the list of task ids to associate each task with one goal
    # only have the task id, so I need to grab the task instance
    # then associate the task id with a goal id

    
    db.session.commit()

    return {"id": goal.goal_id, "task_ids": request_body["task_ids"]}, 200

@goal_bp.route("<goal_id>/tasks", methods=["GET"])
def get_all_tasks_of_goal(goal_id):
    goal = validate_item(Goal, goal_id)

    return goal.to_dict_with_task(), 200