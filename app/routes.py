from flask import Blueprint, request, jsonify, make_response, abort
import requests
from app import db
from app.models.task import Task
from app.models.goal import Goal
from sqlalchemy import desc, asc
from datetime import datetime
import os

tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")
goals_bp = Blueprint("goals", __name__, url_prefix="/goals")

## Helper Functions
# Validate ID function
def validate_model(cls, model_id):
    model_item = cls.query.get(model_id)

    if not model_item:
        return abort(make_response({"message": f"{cls.__name__} with ID {model_id} not found."}, 404))

    return model_item

def query_sort(cls):
    query_sort = request.args.get("sort")

    if query_sort == "asc":
        model_items = db.session.query(cls).order_by(asc(cls.title)).all()
    elif query_sort == "desc":
        model_items = db.session.query(cls).order_by(desc(cls.title)).all()
    else:
        model_items = cls.query.all()

    return model_items

## Routes
# Route to get tasks
@tasks_bp.route("", methods=["GET"])
def get_all_tasks():
    
    tasks = query_sort(Task)
    
    tasks_response = []
    for task in tasks:
        tasks_response.append(task.to_json())
    
    return jsonify(tasks_response), 200



@tasks_bp.route("/<task_id>", methods=["GET"])
def get_task_by_id(task_id):

    task = validate_model(Task, task_id)

    return {"task": task.to_json()}, 200

@tasks_bp.route("", methods=["POST"])
def create_task():
    request_body = request.get_json()

    try: 
        new_task = Task(
            title = request_body["title"],
            description = request_body["description"]
        )  
    except:
        return {
            "details": "Invalid data"
        }, 400
    
    db.session.add(new_task)
    db.session.commit()

    return {"task": new_task.to_json()}, 201

@tasks_bp.route("/<task_id>", methods=["PUT"])
def update_task(task_id):
    task = validate_model(Task, task_id)
    request_body = request.get_json()
    
    task.title = request_body["title"],
    task.description = request_body["description"]
    
    db.session.commit()

    return {"task": task.to_json()}, 200

@tasks_bp.route("/<task_id>", methods=["DELETE"])
def delete_task(task_id):
    task = validate_model(Task, task_id)

    db.session.delete(task)
    db.session.commit()

    return {
        "details": f'Task {task.id} "{task.title}" successfully deleted'
    }, 200

@tasks_bp.route("/<task_id>/mark_incomplete", methods=["PATCH"])
def mark_incomplete(task_id):
    task = validate_model(Task, task_id)

    task.completed_at = None

    db.session.commit()

    return {"task": task.to_json()}, 200

@tasks_bp.route("/<task_id>/mark_complete", methods=["PATCH"])
def mark_complete(task_id):
    task = validate_model(Task, task_id)

    task.completed_at = datetime.utcnow()
    db.session.commit()
    
    key = os.environ.get("key")
    url_path = "https://slack.com/api/chat.postMessage"
    body = {
        "channel": "C056TH84MSN",
        "text": f"Task '{task.title}' has been completed! Well done!"
    }
    header = {
        "Authorization": f"Bearer {key}"
    }
    
    try:
        slack = requests.post(url_path, headers=header, json=body)
    except:
        pass

    return {"task": task.to_json()}, 200


@goals_bp.route("", methods=["POST"])
def create_goal():
    request_body = request.get_json()
    try:
        new_goal = Goal(
            title = request_body["title"]
        )
    except:
        return {
            "details": "Invalid data"
        }, 400

    db.session.add(new_goal)
    db.session.commit()

    return {"goal": new_goal.to_json()}, 201

@goals_bp.route("", methods=["GET"])
def get_all_goals():
    goals = query_sort(Goal)
        
    goals_response = []
    for goal in goals:
        goals_response.append(goal.to_json())
    
    return jsonify(goals_response), 200

@goals_bp.route("/<goal_id>", methods=["GET"])
def get_goal_by_id(goal_id):
    goal = validate_model(Goal, goal_id)
    
    return {"goal": goal.to_json()}, 200

@goals_bp.route("/<goal_id>", methods=["PUT"])
def update_goal(goal_id):
    goal = validate_model(Goal, goal_id)

    request_body = request.get_json()
    
    goal.title = request_body["title"],
    
    db.session.commit()

    return {"goal": goal.to_json()}, 200

@goals_bp.route("/<goal_id>", methods=["DELETE"])
def delete_goal(goal_id):
    goal = validate_model(Goal, goal_id)

    db.session.delete(goal)
    db.session.commit()
    
    return jsonify({
        "details": f"Goal {goal.id} \"{goal.title}\" successfully deleted"
        }), 200

@goals_bp.route("/<goal_id>/tasks", methods=["POST"])
def sending_tasks_to_goal(goal_id):
    goal = validate_model(Goal, goal_id)

    request_body = request.get_json()

    for task_id in request_body["task_ids"]:
        task = validate_model(Task, task_id)
        task.goal_id = goal.id

    db.session.commit()

    return {
        "id": goal.id,
        "task_ids": request_body["task_ids"]
        }, 200

@goals_bp.route("/<goal_id>/tasks", methods=["GET"])
def get_tasks_by_goal_id(goal_id):
    goal = validate_model(Goal, goal_id)

    tasks_response = []

    for task in goal.tasks:
        tasks_response.append(task.to_json())

    return jsonify({
        "id": goal.id,
        "title": goal.title,
        "tasks": tasks_response
    }), 200
