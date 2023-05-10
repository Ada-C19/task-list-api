from flask import Blueprint, request, jsonify, abort, make_response
from app import db
from app.models.task import Task
from app.models.goal import Goal
from datetime import *
import os
from slack_sdk import WebClient


tasks_bp = Blueprint("tasks_bp",__name__, url_prefix="/tasks")
goals_bp = Blueprint("goals_bp", __name__, url_prefix="/goals")

def validate_model(cls, model_id):
    try:
        model_id = int(model_id)
    except:
        abort(make_response({"message":f"{cls.__name__} {model_id} invalid"}, 400))

    model = cls.query.get(model_id)

    if not model:
        abort(make_response({"message":f"{cls.__name__} {model_id} not found"}, 404))

    return model

@tasks_bp.route("",methods=["POST"])
def create_task():
    request_body = request.get_json()

    try:
        new_task = Task.from_dict(request_body)
    except:
        return {"details": "Invalid data"} , 400
    
    db.session.add(new_task)
    db.session.commit()

    return {"task": {"id":new_task.task_id,
            "title": new_task.title,
            "description": new_task.description,
            "is_complete": (new_task.completed_at != None)}}, 201

@tasks_bp.route("",methods=["GET"])
def read_all_tasks():

    sort_query = request.args.get("sort")

    if sort_query == "asc":
        tasks = Task.query.order_by(Task.title.asc()).all()
    elif sort_query == "desc":
        tasks = Task.query.order_by(Task.title.desc()).all()
    else:
        tasks = Task.query.all()

    tasks_response = []
    for task in tasks:
        tasks_response.append(task.to_dict())
    return jsonify(tasks_response), 200

@tasks_bp.route("/<task_id>", methods=["GET"])
def read_one_task(task_id):
    task = validate_model(Task, task_id)
    result = {
        "task":{
            "id": task.task_id,
            "title": task.title,
            "description": task.description,
            "is_complete": (task.completed_at != None)}
        }

    return result, 200

@tasks_bp.route("/<task_id>", methods=["PUT"])
def update_task(task_id):
    task_to_update = validate_model(Task, task_id)

    request_body = request.get_json()

    task_to_update.title = request_body["title"]
    task_to_update.description = request_body["description"]

    db.session.commit()

    return jsonify({"task":task_to_update.to_dict()}), 200

@tasks_bp.route("/<task_id>", methods=["DELETE"])
def delete_task(task_id):
    task = validate_model(Task, task_id)

    db.session.delete(task)
    db.session.commit()

    return abort(make_response({"details":f"Task {task_id} \"{task.title}\" successfully deleted"}, 200))

@tasks_bp.route("/<task_id>/mark_complete", methods=["PATCH"])
def update_task_complete(task_id):

    task = validate_model(Task, task_id)

    if task.completed_at is not None:
        # The task is already complete
        return {"task": task.to_dict()}, 200
    
    task.completed_at = datetime.utcnow()

    db.session.commit()

    slack_token= os.environ["SLACK_TOKEN"]
    client = WebClient(token=slack_token)
    result = client.chat_postMessage(channel="task-notifications", 
        text=f"Someone just completed the task {task.title}")

    return make_response({"task": task.to_dict()}, 200)

@tasks_bp.route("/<task_id>/mark_incomplete", methods=["PATCH"])
def update_task_incomplete(task_id):
    task = validate_model(Task, task_id)

    if task.completed_at is None:
        # The task is already incomplete
        return {"task": task.to_dict()}, 200
    
    task.completed_at = None

    db.session.commit()

    return {"task": task.to_dict()}, 200

@goals_bp.route("", methods=["POST"])
def create_goal():
    request_body = request.get_json()

    try:
        new_goal = Goal.from_dict(request_body)
    except:
        abort(make_response({"details": "Invalid data"}, 400))

    db.session.add(new_goal)
    db.session.commit()

    return {"goal": new_goal.to_dict()}, 201

@goals_bp.route("", methods=['GET'])
def handle_goals():
    title_query = request.args.get("sort")

    if title_query:
        if title_query == "asc":
            goals = Goal.query.order_by(Goal.title.asc())
        elif title_query == "desc":
            goals = Goal.query.order_by(Goal.title.desc())
    else:
        goals = Goal.query.all()
    goals_response = [goal.to_dict() for goal in goals]

    return jsonify(goals_response), 200

def get_valid_item_by_id(model, id):
    try:
        id = int(id)
    except:
        abort(make_response({"message":f"Goal {id} invalid"}, 400))

    item = model.query.get(id)

    return item if item else abort(make_response({"message":f"Goal {id} not found"}, 404))

@goals_bp.route("/<goal_id>", methods=["GET"])
def handle_goal(goal_id):
    goal = get_valid_item_by_id(Goal, goal_id)
    goal.query.get(goal_id)

    return {"goal":{
        "id": goal.goal_id,
        "title": goal.title}}, 200

@goals_bp.route("/<goal_id>", methods=["PUT"])
def update_goal(goal_id):
    goal = get_valid_item_by_id(Goal, goal_id)
    request_body = request.get_json()

    goal.title = request_body["title"]

    db.session.commit()

    return {"goal":goal.to_dict()},200

@goals_bp.route("/<goal_id>", methods=["DELETE"])
def delete_goal(goal_id):
    goal = get_valid_item_by_id(Goal, goal_id)
    db.session.delete(goal)
    db.session.commit()

    return {"details": f"goal {goal_id} \"{goal.title}\" successfully deleted"}