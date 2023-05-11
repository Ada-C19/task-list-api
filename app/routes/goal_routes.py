from flask import Blueprint, jsonify, request
from app.models.task import Task
from app.models.goal import Goal
from .routes_helpers import validate_model
from app import db

goal_bp = Blueprint("goals", __name__, url_prefix="/goals")

@goal_bp.route("", methods=["POST"])
def create_goal():
    if request.method == "POST":
        request_body = request.get_json()
        if "title" not in request_body:
            return jsonify({"details": "Invalid data"}), 400
        
        new_goal = Goal.from_dict(request_body)

        db.session.add(new_goal)
        db.session.commit()

        output = {"goal":new_goal.to_dict()}
        return jsonify(output), 201
    
@goal_bp.route("", methods=["GET"])
def get_all_goals():
    goals_list = []

    goals = Goal.query.all()
    
    for goal in goals:
        goals_list.append(goal.to_dict())
    
    return jsonify(goals_list), 200

@goal_bp.route("/<goal_id>", methods=["GET"])
def get_one_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    output = {"goal":goal.to_dict()}

    return jsonify(output), 200

@goal_bp.route("/<goal_id>", methods=["PUT"])
def update_goal(goal_id):
    goal = validate_model(Goal, goal_id)

    request_body = request.get_json()

    goal.title=request_body["title"]

    db.session.commit()

    output = {"goal":goal.to_dict()}

    return jsonify(output), 200

@goal_bp.route("/<goal_id>", methods=["DELETE"])
def delete_goal(goal_id):
    goal = validate_model(Goal, goal_id)

    db.session.delete(goal)
    db.session.commit()

    output = {"details": f'Goal {goal_id} \"{goal.title}\" successfully deleted'}
    
    return jsonify(output), 200

@goal_bp.route("/<goal_id>/tasks", methods=["POST"])
def adding_tasks(goal_id):
    goal = validate_model(Goal, goal_id)
    
    request_body = request.get_json()

    for task_id in request_body["task_ids"]:
        task = validate_model(Task, task_id)
        task.goal_id = goal.goal_id

    db.session.commit()

    output = {
        "id": goal.goal_id,
        "task_ids": request_body["task_ids"]
    }

    return jsonify(output), 200

@goal_bp.route("/<goal_id>/tasks", methods=["GET"])
def get_tasks_by_goal_id(goal_id):
    goal = validate_model(Goal, goal_id)

    tasks_return = []
    for task in goal.task:
        tasks_return.append(task.to_dict())

    output = {
        "id": goal.goal_id,
        "title": goal.title,
        "tasks": tasks_return
    }

    return jsonify(output), 200