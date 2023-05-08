from flask import Blueprint, make_response, request, jsonify, abort
from app import db
from app.models.task import Task
from app.models.goal import Goal
from datetime import datetime
import os
import requests


tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")
goals_bp = Blueprint("goals", __name__, url_prefix="/goals")

@goals_bp.route("/<goal_id>/tasks", methods=["POST"])
def assign_tasks_to_goal(goal_id):
    goal = validate_item(Goal, goal_id)
    request_body = request.get_json()

    if "task_ids" not in request_body:
        return {"details": "Invalid data"}, 400
    
    response = []
    # validate each of the tasks in the request 
    for task_id in request_body["task_ids"]:
        task = validate_item(Task, task_id)
        # for each valid task, add it to the goal
        goal.tasks.append(task)
        response.append(task.task_id)

    db.session.commit()

    return make_response({"id": goal.goal_id, "task_ids": response}, 200)

@goals_bp.route("/<goal_id>/tasks", methods=["GET"])
def get_all_tasks_of_one_goal(goal_id):
    goal = validate_item(Goal, goal_id)
    tasks = Task.query.filter_by(goal_id = int(goal_id)).all()
    response = []

    for task in tasks:
        response.append(task.to_dict())
    
    return make_response({"id": int(goal_id), "title": goal.title, "tasks": response}, 200)

@goals_bp.route("", methods=["POST"])
def create_goal():
    request_body = request.get_json()

    if "title" not in request_body:
        return {"details": "Invalid data"}, 400

    new_goal = Goal(title =request_body["title"])

    db.session.add(new_goal)
    db.session.commit()

    return {"goal":new_goal.to_dict()}, 201

@goals_bp.route("", methods = ["GET"])
def get_all_goals():
    response = []
    all_goals = Goal.query.all()

    for goal in all_goals:
        response.append(goal.to_dict())
    
    return jsonify(response), 200

@goals_bp.route("/<goal_id>", methods=["GET"])
def get_one_goal(goal_id):
    goal = validate_item(Goal, goal_id)
    
    return {"goal": goal.to_dict()}, 200

@goals_bp.route("/<goal_id>", methods=["PUT"])
def update_goal(goal_id):
    goal = validate_item(Goal, goal_id)
    request_body = request.get_json()

    if "title" not in request_body:
        return (make_response({"details": "Invalid data"}, 400))

    goal.title = request_body["title"]

    db.session.commit()

    return {"goal": goal.to_dict()}, 200    

@goals_bp.route("/<goal_id>", methods=["DELETE"])
def delete_goal(goal_id):
    goal = validate_item(Goal, goal_id)
    title = goal.title
    db.session.delete(goal)
    db.session.commit()

    return {"details": f'Goal {goal_id} "{title}" successfully deleted'}, 200


@tasks_bp.route("", methods=["POST"])
def create_task():
    request_body = request.get_json()
    if "title" not in request_body or "description" not in request_body:
        return {"details": "Invalid data"}, 400

    if "completed_at" in request_body:
        new_task = Task(
            title = request_body["title"],
            description = request_body["description"],
            completed_at = request_body["completed_at"]
        )
    else:
        new_task = Task(
            title = request_body["title"],
            description = request_body["description"]
        )

    db.session.add(new_task)
    db.session.commit()

    return {"task":new_task.to_dict()}, 201

@tasks_bp.route("", methods=["GET"])
def get_all_tasks():
    response = []
    sort_query = request.args.get("sort")

    if sort_query is None:
        all_tasks = Task.query.all()
    elif sort_query == "asc":
        all_tasks = Task.query.order_by(Task.title.asc())
    else:
        all_tasks = Task.query.order_by(Task.title.desc())

    for task in all_tasks: 
        response.append(task.to_dict())

    return jsonify(response), 200

@tasks_bp.route("/<task_id>", methods=["GET"])
def get_one_task(task_id):
    task = validate_item(Task, task_id)
    
    return {"task": task.to_dict()}, 200

def validate_item(model, id):
    try:
        id = int(id)
    except ValueError:
        return abort(make_response({"details": "Invalid Data"}, 400))

    if model.query.get(id) is None:
        return abort(make_response({"details": "id not found"}, 404))

    return model.query.get(id)

@tasks_bp.route("/<task_id>", methods=["PUT"])
def update_task(task_id):
    task = validate_item(Task, task_id)
    request_body = request.get_json()

    if "title" not in request_body or "description" not in request_body:
        return (make_response({"details": "Invalid data"}, 400))

    task.title = request_body["title"]
    task.description = request_body["description"]

    db.session.commit()

    return {"task": task.to_dict()}, 200

@tasks_bp.route("/<task_id>", methods=["DELETE"])
def delete_task(task_id):
    task = validate_item(Task, task_id)
    title = task.title
    db.session.delete(task)
    db.session.commit()

    return {"details": f'Task {task_id} "{title}" successfully deleted'}, 200

@tasks_bp.route("/<task_id>/mark_complete", methods=["PATCH"])
def mark_complete(task_id):
    task = validate_item(Task, task_id)

    task.completed_at = datetime.utcnow()
    db.session.commit()

    api_url = os.environ.get("API_URL")
    payload = {"text": f"Someone just completed the task {task.title}"}
    head = {"Authorization": f"Bearer {os.environ.get('SLACK_BOT_TOKEN')}"}

    requests.post(url=api_url, json=payload, headers=head)
    
    return {"task": task.to_dict()}, 200

@tasks_bp.route("/<task_id>/mark_incomplete", methods=["PATCH"])
def mark_incomplete(task_id):
    task = validate_item(Task, task_id)

    task.completed_at = None
    
    db.session.commit()
    
    return {"task": task.to_dict()}, 200