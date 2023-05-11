#/task-list-api/app/routes.py
from flask import Blueprint, request, jsonify
from app.models.task import Task
from app.models.goal import Goal
from app import db
from datetime import datetime
from slack import send_slack_notification


tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")
goals_bp = Blueprint("goals", __name__, url_prefix="/goals")

@tasks_bp.route("", methods=["GET"])
def get_tasks():
    sort_query = request.args.get("sort")

    if sort_query == "asc":
        tasks = Task.query.order_by(Task.title.asc()).all()
    elif sort_query == "desc":
        tasks = Task.query.order_by(Task.title.desc()).all()
    else:
        tasks = Task.query.all()

    tasks_response = [task.to_dict() for task in tasks]

    return jsonify(tasks_response), 200


@tasks_bp.route('/<int:task_id>', methods=['GET'])
def get_task(task_id):
    task = Task.query.get(task_id)
    if task:
        return jsonify(task=task.to_dict()), 200
    else:
        return jsonify(details="Task not found"), 404

@tasks_bp.route('', methods=['POST'])
def create_task():
    request_data = request.get_json()

    if "title" not in request_data or "description" not in request_data:
        return jsonify(details="Invalid data"), 400

    new_task = Task(title=request_data['title'], description=request_data['description'])
    db.session.add(new_task)
    db.session.commit()
    return jsonify(task=new_task.to_dict()), 201

@tasks_bp.route('/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    task = Task.query.get(task_id)
    if task:
        request_data = request.get_json()
        task.title = request_data.get('title', task.title)
        task.description = request_data.get('description', task.description)
        db.session.commit()
        return jsonify(task=task.to_dict()), 200
    else:
        return jsonify(details="Task not found"), 404

@tasks_bp.route('/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    task = Task.query.get(task_id)
    if task:
        db.session.delete(task)
        db.session.commit()
        return jsonify(details=f'Task {task_id} "{task.title}" successfully deleted'), 200
    else:
        return jsonify(details="Task not found"), 404


@tasks_bp.route("/<int:task_id>/mark_complete", methods=["PATCH"])
def mark_complete(task_id):
    task = Task.query.get(task_id)  # Find the task with the given task_id
    if task:
        task.completed_at = datetime.utcnow()
        db.session.commit()
        send_slack_notification(task.title)  # Send Slack notification
        return jsonify(task=task.to_dict()), 200
    else:
        return jsonify(details="Task not found"), 404



@tasks_bp.route("/<int:task_id>/mark_incomplete", methods=["PATCH"])
def mark_incomplete(task_id):
    task = Task.query.get(task_id)
    if task:
        task.completed_at = None
        db.session.commit()
        return jsonify(task=task.to_dict()), 200
    else:
        return jsonify(details="Task not found"), 404
    
@goals_bp.route("", methods=["POST"])
def create_goal():
    request_data = request.get_json()

    if "title" not in request_data:
        return jsonify(details="Invalid data"), 400

    new_goal = Goal(title=request_data["title"])
    db.session.add(new_goal)
    db.session.commit()
    return jsonify(goal=new_goal.to_dict()), 201

@goals_bp.route("", methods=["GET"])
def get_goals():
    goals = Goal.query.all()
    goals_response = [goal.to_dict() for goal in goals]
    return jsonify(goals_response), 200

@goals_bp.route("/<int:goal_id>", methods=["GET"])
def get_goal(goal_id):
    goal = Goal.query.get(goal_id)
    if goal:
        return jsonify(goal=goal.to_dict()), 200
    else:
        return jsonify(details="Goal not found"), 404

@goals_bp.route("/<int:goal_id>", methods=["PUT"])
def update_goal(goal_id):
    goal = Goal.query.get(goal_id)
    if goal:
        request_data = request.get_json()
        goal.title = request_data.get("title", goal.title)
        db.session.commit()
        return jsonify(goal=goal.to_dict()), 200
    else:
        return jsonify(details="Goal not found"), 404

@goals_bp.route("/<int:goal_id>", methods=["DELETE"])
def delete_goal(goal_id):
    goal = Goal.query.get(goal_id)
    if goal:
        db.session.delete(goal)
        db.session.commit()
        return jsonify(details=f'Goal {goal_id} "{goal.title}" successfully deleted'), 200
    else:
        return jsonify(details="Goal not found"), 404
