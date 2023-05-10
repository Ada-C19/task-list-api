from flask import Blueprint, jsonify, request, Response, abort, make_response
from app.models.task import Task
from app.models.goal import Goal
from app import db 
from datetime import datetime
from dotenv import load_dotenv
import requests
import os


# create blueprint 
task_bp = Blueprint("task", __name__, url_prefix="/tasks")
goal_bp = Blueprint("goal", __name__, url_prefix="/goals")

# Create Task Route
@task_bp.route("", methods=["POST"])
def add_task(): 
    response_body = request.get_json()

    # TODO - from_dict method
    try:
        new_task = Task(title=response_body["title"], 
                        description=response_body["description"], 
                        )
    except KeyError: 
        return {"details": "Invalid data"}, 400
    
    db.session.add(new_task)
    db.session.commit()

    return {"task": new_task.to_result()}, 201

# Get All Tasks Route
@task_bp.route("", methods=["GET"])
def get_tasks():
    response = []
    # query params
    sort_order = request.args.get('sort', None)

    if sort_order == 'asc': 
        all_tasks = Task.query.order_by(Task.title.asc()).all()
    elif sort_order == 'desc': 
        all_tasks = Task.query.order_by(Task.title.desc()).all()
    else: 
        all_tasks = Task.query.all()

    for task in all_tasks: 
        response.append(task.to_result())
    
    return jsonify(response), 200

# Get One Task Route
@task_bp.route("/<task_id>", methods=["GET"])
def get_one_task(task_id): 
    task = validate_item(Task, task_id)

    return {"task": task.to_result()}, 200

# Update a Task Route
@task_bp.route("/<task_id>", methods=["PUT"])
def update_task(task_id):
    task = validate_item(Task, task_id)

    request_data = request.get_json()

    task.title = request_data["title"]
    task.description = request_data["description"]

    db.session.commit()

    return {"task": task.to_result()}, 200

# Delete a Task Route 
@task_bp.route("/<task_id>", methods=["DELETE"])
def delete_task(task_id):
    task = validate_item(Task, task_id)

    db.session.delete(task)
    db.session.commit()

    return {"details": f"Task {task_id} \"{task.title}\" successfully deleted"}, 200

# Mark Task as Completed Route
@task_bp.route("/<task_id>/mark_complete", methods=["PATCH"])
def update_task_as_complete(task_id):
    task = validate_item(Task, task_id)

    request_data = request.get_json()
    task.completed_at = datetime.now()

    db.session.commit()

    kim_bot = {
        "text": f"You completed the task {task.title} congrats!! :clap:",
        "channel": "task-notifications",
        "token": os.environ.get("SLACK_BOT_TOKEN")
    }

    r = requests.post(url='https://slack.com/api/chat.postMessage',data=kim_bot)

    return {"task": task.to_result()}, 200

# Mark Task as Incompleted Route
@task_bp.route("/<task_id>/mark_incomplete", methods=["PATCH"])
def update_task_as_incomplete(task_id):
    task = validate_item(Task, task_id)

    request_data = request.get_json()
    task.completed_at = None

    db.session.commit()

    return {"task": task.to_result()}, 200


# *****************************************************************
# **********************Goal Routes********************************
# *****************************************************************

# Create Goal Route
@goal_bp.route("", methods=["POST"])
def add_goal(): 
    response_body = request.get_json()

    # TODO - from_dict method
    try:
        new_goal = Goal(title=response_body["title"])
    except KeyError: 
        return {"details": "Invalid data"}, 400
    
    db.session.add(new_goal)
    db.session.commit()

    return {"goal": new_goal.to_dict()}, 201

# Get Goal Route
@goal_bp.route("", methods=["GET"])
def get_goals(): 
    response = [] 
    all_goals = Goal.query.all()

    for goal in all_goals: 
        response.append(goal.to_dict())
    
    return jsonify(response), 200

# Get One Goal Route
@goal_bp.route("/<goal_id>", methods=["GET"])
def get_one_goal(goal_id): 
    goal = validate_item(Goal, goal_id)

    return {"goal": goal.to_dict()}, 200

# Update a Goal Route
@goal_bp.route("/<goal_id>", methods=["PUT"])
def update_goal(goal_id):
    goal = validate_item(Goal, goal_id)
    request_data = request.get_json()
    goal.title = request_data["title"]

    db.session.commit()

    return {"goal": goal.to_dict()}, 200

# Delete a Goal Route 
@goal_bp.route("/<goal_id>", methods=["DELETE"])
def delete_goal(goal_id):
    goal = validate_item(Goal, goal_id)

    db.session.delete(goal)
    db.session.commit()

    return {"details": f"Goal {goal_id} \"{goal.title}\" successfully deleted"}, 200


# Adding Tasks to a Goal
@goal_bp.route("/<goal_id>/tasks", methods=["POST"])
def add_tasks_to_goal(goal_id):
    goal = validate_item(Goal, goal_id)
    request_body = request.get_json()
    all_tasks = request_body["task_ids"]

    for task_id in all_tasks: 
        task = validate_item(Task, task_id)
        task.goal = goal
    
    db.session.commit()

    return jsonify({"id": goal.goal_id, 
                    "task_ids": all_tasks}), 200

# Get Tasks of One Goal
@goal_bp.route("/<goal_id>/tasks", methods=["GET"])
def get_all_tasks_of_goal(goal_id):
    goal = validate_item(Goal, goal_id)
    tasks = []

    for task in goal.tasks:
        tasks.append(task.to_result())
    
    return jsonify({"id": goal.goal_id,
            "title": goal.title, 
            "tasks": tasks}), 200


# VALIDATION HELPER FUNCTION
def validate_item(model, item_id):
    try:
        item_id = int(item_id)

    except ValueError:
        return abort(make_response({"message": f"invalid id: {item_id}"}, 400))
    
    item = model.query.get(item_id)
    
    if not item: 
        return abort(make_response({"message": f"{model.__name__} {item_id} not found"}, 404))
    
    return item