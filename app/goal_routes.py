from app import db
from flask import Blueprint, request, make_response, jsonify
from app.models.goal import Goal
from .routes_helpers import validate_model

goal_bp = Blueprint("goals", __name__, url_prefix="/goals")

@goal_bp.route("", methods=["POST"])
def create_goal():
    request_body = request.get_json()

    new_goal = Goal.from_dict(request_body)

    db.session.add(new_goal)
    db.session.commit()

    return make_response(jsonify({"goal": new_goal.to_dict()}), 201)


@goal_bp.route("", methods=["GET"])
def get_all_goals():
    goals = Goal.query.all()
    
    goals_response = [goal.to_dict() for goal in goals]

    return jsonify(goals_response)


@goal_bp.route("/<goal_id>", methods=["GET"])
def get_one_goal(goal_id):
    goal = validate_model(Goal, goal_id)

    return jsonify({"goal": goal.to_dict()})


@goal_bp.route("/<goal_id>", methods=["PUT"])
def update_goal(goal_id):
    goal = validate_model(Goal, goal_id)

    request_body = request.get_json()
    goal.update_from_dict(request_body)

    db.session.commit()

    return make_response(jsonify({"goal": goal.to_dict()}), 200)


@goal_bp.route("/<goal_id>", methods=["DELETE"])
def delete_goal(goal_id):
    goal = validate_model(Goal, goal_id)

    db.session.delete(goal)
    db.session.commit()

    return make_response(jsonify({"details": f"Goal {goal.goal_id} \"{goal.title}\" successfully deleted"}))
