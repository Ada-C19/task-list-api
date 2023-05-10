from app import db
from app.models.goal import Goal
from flask import Blueprint, jsonify, make_response, request, abort
from .routes_helper import validate_model

goals_bp = Blueprint("goals", __name__, url_prefix = "/goals")
@goals_bp.route("", methods=["POST"])
def create_goal():
    request_body = request.get_json()
    if "title" not in request_body:
        return make_response(jsonify({"details": "Invalid data"}), 400)
    # Create a new goal in the database
    new_goal = Goal(
        title=request_body["title"]
    )

    db.session.add(new_goal)
    db.session.commit()

    response_body = dict(goal = new_goal.to_dict())

    return jsonify(response_body), 201

@goals_bp.route("", methods=["GET"])
def get_all_goal():

    goals = Goal.query.all()
    goal_list = [goal.to_dict() for goal in goals]


    return jsonify(goal_list), 200

@goals_bp.route("/<task_id>", methods=["PUT"])
def update_goal(goal_id):
    goal = validate_model(Goal,goal_id)
    request_body = request.get_json()

    goal.title = request_body["title"]
    goal.description =request_body["description"]
    #goal.completed_at = request_body[ "completed_at"]

    db.session.commit()

    response_body = dict(goal = goal.to_dict())
