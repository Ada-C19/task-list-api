from flask import Blueprint, jsonify, abort, make_response, request
from app import db
from app.models.task import Task
from app.models.goal import Goal
import os, datetime, requests

task_bp = Blueprint("task", __name__, url_prefix="/tasks")
goal_bp = Blueprint("goal", __name__, url_prefix="/goals")

# Helper Functions 

def validate_item(model, id):
    try: 
        id = int(id)
    except ValueError:
        return abort(make_response({"msg": f"Invalid id: {id}"}, 400))
    
    item = model.query.get(id)

    if not item:
        return abort(make_response({"message": f"id {id} not found"}, 404))
    
    return item


# Task routes 
@task_bp.route("", methods=["POST"])
def add_task():
    request_body = request.get_json()
    if "title" not in request_body or "description" not in request_body:
        return {"details": "Invalid data"}, 400
    
    new_task = Task(
        title=request_body["title"],
        description=request_body["description"],
        completed_at=request_body.get("completed_at", None)
    )

    db.session.add(new_task)
    db.session.commit()

    return {"task": new_task.to_dict()}, 201


@task_bp.route("", methods=["GET"])
def get_at_least_one_task():
    response = []
    sort_order = request.args.get('sort', None)
    if sort_order == 'asc':
        all_tasks = Task.query.order_by(Task.title.asc()).all()
    elif sort_order == 'desc':
        all_tasks = Task.query.order_by(Task.title.desc()).all()
    else:
        all_tasks = Task.query.all()
        
    for task in all_tasks: 
        response.append(task.to_dict())

    return jsonify(response), 200

@task_bp.route("/<task_id>", methods=["GET"])
def get_one_task(task_id):
    task = validate_item(Task, task_id)

    return ({"task": task.to_dict()}), 200

@task_bp.route("/<task_id>", methods=["PUT"])
def update_task(task_id):
    task = validate_item(Task, task_id)
    
    request_data = request.get_json()

    task.title = request_data["title"]
    task.description = request_data["description"]

    db.session.commit()
    return {"task": task.to_dict()}, 200

@task_bp.route("/<task_id>", methods=["DELETE"])
def delete_task(task_id):
    task = validate_item(Task, task_id)
    
    db.session.delete(task)
    db.session.commit()

    return {"details": f'Task {task_id} "{task.title}" successfully deleted'}, 200

@task_bp.route("/<task_id>/mark_complete", methods=["PATCH"])
def task_complete(task_id):
    
    task = validate_item(Task, task_id)
    task.completed_at = datetime.datetime.now()

    db.session.commit()

    slack_path = "https://slack.com/api/chat.postMessage"
    slack_channel = "task-notifications"
    slack_message = f"Someone just completed the task {task.title}."

    query_params = {
        "token": os.environ.get("SLACK_TOKEN"),
        "channel": slack_channel,
        "text": slack_message
    }

    requests.post(url=slack_path, data=query_params)

    return {"task": task.to_dict()}, 200

    
@task_bp.route("/<task_id>/mark_incomplete", methods=["PATCH"])
def task_incomplete(task_id):
    
    task = validate_item(Task, task_id)
    task.completed_at = None

    db.session.commit()

    return {"task": task.to_dict()}, 200



# Goal Routes 

@goal_bp.route("", methods=["POST"])
def add_goal():  
    request_body = request.get_json()      
    if "title" not in request_body:
        return {"details": "Invalid data"}, 400
    
    new_goal = Goal(
        title=request_body["title"]
    )

    db.session.add(new_goal)
    db.session.commit()

    return {"goal": new_goal.to_dict()}, 201

@goal_bp.route("/<goal_id>", methods=["GET"])
def get_one_goal(goal_id):
    goal = validate_item(Goal, goal_id)

    return {"goal": goal.to_dict()}, 200

@goal_bp.route("", methods=["GET"])
def get_at_least_one_goal():
    response = []
    all_goals = Goal.query.all()
        
    for goal in all_goals: 
        response.append(goal.to_dict())

    return jsonify(response), 200

@goal_bp.route("/<goal_id>", methods=["PUT"])
def update_goal(goal_id):
    goal = validate_item(Goal, goal_id)
    
    request_data = request.get_json()

    goal.title = request_data["title"]

    db.session.commit()
    return {"goal": goal.to_dict()}, 200

@goal_bp.route("/<goal_id>", methods=["DELETE"])
def delete_goal(goal_id):
    goal = validate_item(Goal, goal_id)
    
    db.session.delete(goal)
    db.session.commit()

    # return {"details": f'Goal {goal_id} "{goal.title}" successfully deleted'}, 200
    return {
        "details": f"Goal {goal.goal_id} \"{goal.title}\" successfully deleted"
    }, 200

#One goal to many tasks
@goal_bp.route("/<goal_id>/tasks", methods=["POST"])
def task_ids_to_a_goal(goal_id):
    goal = validate_item(Goal, goal_id)
    
    request_data = request.get_json()

    for task_id in request_data["task_ids"]:
        task = validate_item(Task, task_id)
        task.goal = goal
        
    db.session.commit()

    return {
        "id": goal.goal_id,
        "task_ids": request_data["task_ids"]
    }, 200

@goal_bp.route("/<goal_id>/tasks", methods=["GET"])
def tasks_of_one_goal(goal_id):
    goal = validate_item(Goal, goal_id)
    response = []

    for task in goal.tasks: 
        response.append(task.to_dict())

    return {
        "id": goal.goal_id,
        "title": goal.title,
        "tasks": response
    }, 200