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