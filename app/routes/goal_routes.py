from flask import Blueprint, jsonify, request, make_response, abort
from app.models.goal import Goal
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


