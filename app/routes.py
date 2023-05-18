from flask import Blueprint, jsonify, request
from app import db
from app.models.task import Task
from app.models.goal import Goal
from datetime import datetime
import requests

tasks_bp = Blueprint("tasks", __name__, url_prefix=("/tasks"))
goals_bp = Blueprint("goals", __name__, url_prefix="/goals")


# create route (get) to get all tasks
@tasks_bp.route("", methods=["GET"])
def get_all_tasks():
    tasks_response = []
    sort = request.args.get("sort")
    
    if sort == "asc":
        tasks = Task.query.order_by(Task.title.asc()).all()
    elif sort == "desc":
        tasks = Task.query.order_by(Task.title.desc()).all()
    else:
        tasks = Task.query.all()
        
    for task in tasks: 
        tasks_response.append({
            "id": task.task_id,
            "title": task.title,
            "description": task.description,
            "is_complete": task.completed_at != None
        })
        
    return jsonify(tasks_response)


# create a task
@tasks_bp.route("", methods=["POST"])
def create_task():
    request_body = request.get_json()
    
    if "title" not in request_body or "description" not in request_body:
        return jsonify({"details": "Invalid data"}), 400
    
    new_task = Task(
        title = request_body.get("title"),
        description = request_body.get("description"),
        completed_at = request_body.get("completed_at")
        )
    
    db.session.add(new_task)
    db.session.commit()
    
    return jsonify({
        "task": {
            "id": new_task.task_id,
            "title": new_task.title,
            "description": new_task.description,
            "is_complete": new_task.completed_at != None
        }
    }), 201
    

# get a specific task
@tasks_bp.route("/<task_id>", methods=["GET"])
def get_specific_task(task_id):
    task = Task.query.get_or_404(task_id)
    
    return jsonify({
        "task": {
            "id": task.task_id,
            "title": task.title,
            "description": task.description,
            "is_complete": task.completed_at != None
        }
    })
    


# update a task
@tasks_bp.route("/<task_id>", methods=["PUT"])
def update_task(task_id):
    task = Task.query.get(task_id)
    request_body = request.get_json()
    
    if task is None:
        return jsonify({"details": f"Task {task_id} was not found."}), 404
    
    task.title = request_body.get("title", task.title)
    task.description = request_body.get("description", task.description)
    
    db.session.commit()
    
    return jsonify({
        "task": {
            "id": task.task_id,
            "title": task.title,
            "description": task.description,
            "is_complete": task.completed_at != None
        }
    })
    
    
# detele a task & return 404 + message if not found
@tasks_bp.route("/<task_id>", methods=["DELETE"])
def delete_task(task_id):
    task = Task.query.get(task_id)
    
    if task is None:
        return jsonify({"details": f"Task {task_id} was not found."}), 404
    
    db.session.delete(task)
    db.session.commit()
    
    return jsonify({
        "details": f'Task {task_id} "{task.title}" successfully deleted'
    })


# Get task not found
@tasks_bp.route("/<int:task_id>", methods=["GET"])
def get_task_not_found(task_id):
    task = Task.query.get(task_id)
    
    if task is None:
        return jsonify({"details": f"Task {task_id} was not found."}), 404
    
    return jsonify({
        "task": {
            "id": task.task_id,
            "title": task.title,
            "description": task.description,
            "is_complete": task.completed_at != None
        }
    })
    
# mark task complete
@tasks_bp.route("/<task_id>/mark_complete", methods=["PATCH"])
def mark_complete(task_id):
    task = Task.query.get(task_id)
    
    if task is None:
        return jsonify({"details": f"Task {task_id} was not found."}), 404
    
    task.completed_at = datetime.now()
    db.session.add(task)
    db.session.commit()
    
    message = f"Task {task.title} is complete."
    send_slack_request("study-sesh", message)
    
    return jsonify({
        "task": {
            "id": task.task_id,
            "title": task.title,
            "description": task.description,
            "is_complete": True
        }
    })


@tasks_bp.route("/<task_id>/mark_incomplete", methods=["PATCH"])
def mark_incomplete(task_id):
    task = Task.query.get(task_id)
    
    if task is None:
        return jsonify({"details": f"Task {task_id} was not found."}), 404
    
    task.completed_at = None
    db.session.add(task)
    db.session.commit()
    
    return jsonify({
        "task": {
            "id": task.task_id,
            "title": task.title,
            "description": task.description,
            "is_complete": False
        }
    })
    

# create function that sends request to slack API
def send_slack_request(channel, message):
    path = "https://slack.com/api/chat.postMessage"
    headers = {
        "Type": "application/json",
        "Authorization": "xoxb-4715007748918-5273625376965-Fd54AOr5GENxXWt10KbNsgpE"
    }
    payload = {
        "channel": channel,
        "text": message
    }
    response = requests.post(path, headers=headers, json=payload)
    response.raise_for_status()
    

# get a goal
@goals_bp.route("", methods=["GET"])
def get_goals():
    goals = Goal.query.all()
    goals_dict = [goal.to_dict() for goal in goals]
    return jsonify(goals_dict)


# create a new goal
@goals_bp.route("", methods=["POST"])
def create_goal():
    request_data = request.get_json()
    if "title" not in request_data:
        return jsonify({"details": "Invalid data"}), 400

    title = request_data["title"]
    goal = Goal(title=title)
    db.session.add(goal)
    db.session.commit()

    return jsonify({"goal": goal.to_dict()}), 201


# update existing goal
@goals_bp.route("/<goal_id>", methods=["PUT"])
def update_goal(goal_id):
    goal = Goal.query.get(goal_id)

    if goal is None:
        return jsonify({"details": f"Goal {goal_id} was not found."}), 404

    request_data = request.get_json()
    goal.title = request_data.get("title", goal.title)
    db.session.commit()

    return jsonify({"goal": goal.to_dict()})


# get specific goal/ account for 404
@goals_bp.route("/<goal_id>", methods=["GET"])
def get_goal(goal_id):
    goal = Goal.query.get(goal_id)

    if goal is None:
        return jsonify({"details": f"Goal {goal_id} was not found."}), 404

    return jsonify({"goal": goal.to_dict()})


# delete a goal
@goals_bp.route("/<goal_id>", methods=["DELETE"])
def delete_goal(goal_id):
    goal = Goal.query.get(goal_id)

    if goal is None:
        return jsonify({"details": f"Goal {goal_id} was not found."}), 404

    db.session.delete(goal)
    db.session.commit()

    return jsonify({
        "details": f'Goal {goal.id} "{goal.title}" successfully deleted'
    }), 200