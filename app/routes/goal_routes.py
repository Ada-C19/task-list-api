from flask import Blueprint, jsonify, request, make_response, abort
from app.models.goal import Goal
from app.models.task import Task
from .routes_helpers import validate_model
from app import db

goals_bp = Blueprint("goals", __name__, url_prefix="/goals")

# create a goal endpoint
@goals_bp.route("", methods=["POST"])
def create_goal():
    request_body = request.get_json()

    try:
        new_goal = Goal.from_dict(request_body)
    except KeyError:
        abort(make_response({"details": "Invalid data"}, 400))

    db.session.add(new_goal)
    db.session.commit()

    return jsonify({"goal": new_goal.to_dict()}), 201

# get all goals endpoint
@goals_bp.route("", methods=["GET"])
def get_all_goals():

    goals = Goal.query.all()
    goal_list = [goal.to_dict() for goal in goals]

    return jsonify(goal_list), 200

# get one goal endpoint
@goals_bp.route("/<id>", methods=["GET"])
def get_goal(id):
    goal = validate_model(Goal, id)

    response_body = goal.to_dict()

    return jsonify({"goal": response_body}), 200

# delete goal endpoint
@goals_bp.route("/<id>", methods=["DELETE"])
def delete_goal(id):
    goal = validate_model(Goal, id)

    db.session.delete(goal)
    db.session.commit()

    return jsonify({"details": f'Goal {goal.id} "{goal.title}" successfully deleted'}), 200

# update goal endpoint
@goals_bp.route("/<id>", methods=["PUT"])
def update_goal(id):
    goal = validate_model(Goal, id)

    request_body = request.get_json()

    goal.title = request_body["title"]

    db.session.commit()

    return jsonify({"goal": goal.to_dict()}), 200

# assign tasks to goal
@goals_bp.route("/<goal_id>/tasks", methods=["POST"])
def assign_tasks_to_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    
    request_body = request.get_json()

    for task_id in request_body["task_ids"]:
        task = validate_model(Task, task_id)
        goal.tasks.append(task)
    
    db.session.commit()

    return jsonify({"id": goal.id, "task_ids": [task.id for task in goal.tasks]})

# get all tasks from a goal
@goals_bp.route("/<goal_id>/tasks", methods=["GET"])
def get_all_tasks_from_goal(goal_id):
    goal = validate_model(Goal, goal_id)

    goal_response = goal.to_dict()

    if "tasks" not in goal_response:
        goal_response["tasks"] = []

    return jsonify(goal_response), 200
