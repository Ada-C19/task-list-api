from flask import Blueprint, jsonify, abort, make_response, request
from app.models.task import Task
from app.models.goal import Goal
from app import db
from datetime import datetime
import os, requests


tasks_bp = Blueprint("tasks_bp", __name__, url_prefix="/tasks")
goals_bp = Blueprint("goals_bp", __name__, url_prefix="/goals")


def validate_goal_by_id(id):
    try:
        id = int(id)
    except:
        abort(make_response({"message":f"Goal {id} invalid"}, 400))

    goal = Goal.query.get(id)

    if not goal:
        abort(make_response({"message":f"goal {id} not found"}, 404)) 
    
    return goal


def validate_task_by_id(id):
    try:
        id = int(id)
    except:
        abort(make_response({"message":f"task {id} invalid"}, 400))

    task = Task.query.get(id)

    if not task:
        abort(make_response({"message":f"task {id} not found"}, 404)) 
    
    return task
    

@tasks_bp.route("", methods=["POST"])
def create_task():
    request_body = request.get_json()

    if "title" not in request_body or "description" not in request_body:
        abort(make_response({"details":"Invalid data"}, 400))

    new_task = Task(title=request_body["title"],
                    description=request_body["description"])
    
    db.session.add(new_task)
    db.session.commit()

    return {"task": new_task.to_dict()}, 201


@goals_bp.route("/<goal_id>/tasks", methods=["POST"])
def send_tasks_to_goal(goal_id):
    goal = validate_goal_by_id(goal_id)

    request_body = request.get_json()

    tasks = Task.query.all()

    task_ids = request_body["task_ids"]

    for task in tasks:
        if task.id in task_ids:
            task.goal_id = goal_id
    
    db.session.commit()
    return {"id": goal_id, "task_ids": task_ids}, 200


@tasks_bp.route("", methods=["GET"])
def get_all_tasks():
    tasks_response = []
    query = request.args.get("sort")

    if query == "asc":
        tasks = Task.query.order_by(Task.title.asc())
    elif query == "desc":
        tasks = Task.query.order_by(Task.title.desc())
    else:
        tasks = Task.query.all()

    for task in tasks:
        tasks_response.append(task.to_dict())
    return jsonify(tasks_response)



@tasks_bp.route("/<id>", methods=["GET"])
def get_one_task(id):
    task = validate_task_by_id(id)
    print("IM PRINTING", task.to_dict()) # DELETE THIS LATER
    return {"task": task.to_dict()}, 200


@tasks_bp.route("/<id>", methods=["PUT"])
def update_task(id):
    task = validate_task_by_id(id)

    request_body = request.get_json()
    task.title = request_body["title"]
    task.description = request_body["description"]
    
    db.session.commit()
    return {"task": task.to_dict()}, 200


@tasks_bp.route("/<id>", methods=["DELETE"])
def delete_task(id):
    task = validate_task_by_id(id)

    db.session.delete(task)
    db.session.commit()

    return {
        "details": f"Task {id} \"{task.title}\" successfully deleted"
    }, 200

@tasks_bp.route("/<id>/mark_complete", methods=["PATCH"])
def mark_complete(id):
    task = validate_task_by_id(id)

    task.completed_at = datetime.utcnow()

    url = "https://slack.com/api/chat.postMessage"
    slack_token = os.environ.get('SLACKBOT_TOKEN')
    header = {"Authorization": f"Bearer {slack_token}"}
    data = {
        "channel": "task-notifications",
        "text": f"Someone just completed the task {task.title}"
        }
    
    requests.post(url, data=data, headers=header)

    db.session.commit()

    return {"task": task.to_dict()}, 200


@tasks_bp.route("/<id>/mark_incomplete", methods=["PATCH"])
def mark_incomplete(id):
    task = validate_task_by_id(id)

    task.completed_at = None

    db.session.commit()
    return {"task": task.to_dict()}, 200


@goals_bp.route("", methods=["POST"])
def create_goal():
    request_body = request.get_json()

    if "title" not in request_body:
        abort(make_response({"details":"Invalid data"}, 400))

    new_goal = Goal(title=request_body["title"])
    
    db.session.add(new_goal)
    db.session.commit()

    return {"goal": new_goal.to_dict()}, 201


@goals_bp.route("", methods=["GET"])
def get_all_goals():
    goals = Goal.query.all()

    goals_response = []

    for goal in goals:
        goals_response.append(goal.to_dict())
    return jsonify(goals_response)


@goals_bp.route("/<goal_id>", methods=["GET"])
def get_one_goal(goal_id):
    goal = validate_goal_by_id(goal_id)
    return {"goal": goal.to_dict()}, 200


@goals_bp.route("/<goal_id>", methods=["PUT"])
def update_goal(goal_id):
    goal = validate_goal_by_id(goal_id)

    request_body = request.get_json()
    goal.title = request_body["title"]
    
    db.session.commit()
    return {"goal": goal.to_dict()}, 200


@goals_bp.route("/<goal_id>", methods=["DELETE"])
def delete_goal(goal_id):
    goal = validate_goal_by_id(goal_id)

    db.session.delete(goal)
    db.session.commit()

    return {
        "details": f"Goal {goal_id} \"{goal.title}\" successfully deleted"
    }, 200