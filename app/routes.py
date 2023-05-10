import requests
from flask import Blueprint, jsonify, request, abort, make_response 
from app import db 
from app.models.task import Task
from app.models.goal import Goal
from datetime import datetime
import os
from dotenv import load_dotenv
import json




tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")
@tasks_bp.route("", methods=["POST"])
def add_task():
    request_body = request.get_json()

    if "description" not in request_body\
        or "title" not in request_body:
        return jsonify({"details": "Invalid data"}), 400
    
    new_task = Task(title=request_body["title"], description=request_body["description"])

    db.session.add(new_task)
    db.session.commit()

    is_complete = True if new_task.completed_at else False

    
    return {
        "task":
            {
            "id": new_task.id,
            "title": new_task.title,
            "description": new_task.description,
            "is_complete": is_complete
            }
    }, 201

@tasks_bp.route("", methods=["GET"])
def get_tasks():
    response = []
    sort_query = request.args.get("sort")
    if sort_query is None:
        all_tasks = Task.query.all()

    elif sort_query == "asc":
        all_tasks = Task.query.order_by(Task.title.asc())
    else:
        all_tasks = Task.query.order_by(Task.title.desc())
    
    for task in all_tasks:
        response.append(task.to_dict()["task"])
    
    return jsonify(response), 200

@tasks_bp.route("<task_id>", methods=["GET"])
def get_task_by_id(task_id):
    task = Task.query.get_or_404(task_id)
    response = task.to_dict()
    return jsonify(response), 200

@tasks_bp.route("<task_id>", methods=["PUT"])
def update_task(task_id):
    task = Task.query.get_or_404(task_id)

    request_data = request.get_json()

    task.title = request_data["title"]
    task.description = request_data["description"]

    db.session.commit()
    response = task.to_dict()
    return jsonify(response), 200


@tasks_bp.route("<task_id>", methods=["DELETE"])
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)

    db.session.delete(task)
    db.session.commit()

    return {"details": f'Task {task_id} "{task.title}" successfully deleted'}, 200

def ham_bot_posts(task):
    load_dotenv()
    path = "https://slack.com/api/chat.postMessage"
    HAM_BOT_TOKEN = os.environ.get("HAM_BOT_OAUTH")

    headers = {
        "Authorization": f"Bearer {HAM_BOT_TOKEN}",
        "Content-Type": "application/json"
    }

    data = {
        "channel": "#task-notifications",
        "text": f"Someone just completed the task {task.title}"
    }
    response = requests.post(path, headers=headers, data=json.dumps(data))
    print(response)


@tasks_bp.route("<task_id>/mark_complete", methods=["PATCH"])
def mark_task_complete(task_id):
    task = Task.query.get_or_404(task_id)
    request_data = request.get_json()

    task.completed_at = datetime.utcnow()
    db.session.commit()
    ham_bot_posts(task)

    response = task.to_dict()
    return jsonify(response), 200



@tasks_bp.route("<task_id>/mark_incomplete", methods=["PATCH"])
def mark_task_incomplete(task_id):
    task = Task.query.get_or_404(task_id)
    request_data = request.get_json()

    task.completed_at = None
    db.session.commit()

    response = task.to_dict()
    return jsonify(response), 200

goals_bp = Blueprint("goals", __name__, url_prefix="/goals")
@goals_bp.route("", methods=["POST"])
def create_a_goal():
    request_body = request.get_json()

    if "title" not in request_body:
        return jsonify({"details": "Invalid data"}), 400

    new_goal = Goal.from_dict(request_body)

    db.session.add(new_goal)
    db.session.commit()

    return {
        "goal": {
            "id": new_goal.goal_id,
            "title": new_goal.title
        }
    }, 201

@goals_bp.route("", methods=["GET"])
def get_goals():
    response = []
    title_query = request.args.get("title")

    if title_query is None:
        all_goals = Goal.query.all()
    else:
        all_goals = Goal.query.filter_by(title=title_query)
    
    for goal in all_goals:
        response.append(goal.to_dict())
    
    return jsonify(response), 200

@goals_bp.route("<goal_id>", methods=["GET"])
def get_goal_by_id(goal_id):
    goal = Goal.query.get_or_404(goal_id)
    response = {"goal": goal.to_dict()}
    return jsonify(response), 200

@goals_bp.route("<goal_id>", methods=["PUT"])
def update_goal(goal_id):
    goal = Goal.query.get_or_404(goal_id)

    request_data = request.get_json()

    goal.title = request_data["title"]

    db.session.commit()
    response = {"goal": goal.to_dict()}
    return jsonify(response), 200

@goals_bp.route("<goal_id>", methods=["DELETE"])
def delete_goal(goal_id):
    goal = Goal.query.get_or_404(goal_id)

    db.session.delete(goal)
    db.session.commit()

    return {"details": f'Goal {goal_id} "{goal.title}" successfully deleted'}, 200




