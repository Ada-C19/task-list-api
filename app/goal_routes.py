from app import db
from app.models.goal import Goal
from app.helper import validate_model
from flask import Blueprint, jsonify, abort, make_response, request

goals_bp = Blueprint("goals", __name__, url_prefix="/goals")

@goals_bp.route("", methods=["POST"])
def create_goal():
    request_body = request.get_json()
    try:
        new_goal = Goal.from_dict(request_body)
        db.session.add(new_goal)
        db.session.commit()
        return make_response(jsonify({"goal": new_goal.to_dict()}), 201)
    except KeyError as error:
        abort(make_response({"details": "Invalid data"}, 400))

@goals_bp.route("", methods=["GET"])
def read_all_goals():
    goals = Goal.query.all()
    goals_response = [goal.to_dict() for goal in goals]
    return jsonify(goals_response)

@goals_bp.route("/<goal_id>", methods=["GET"])
def read_one_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    return jsonify({"goal": goal.to_dict()})

@goals_bp.route("/<goal_id>", methods=["PUT"])
def update_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    request_body = request.get_json()

    goal.title = request_body["title"]
    
    db.session.commit()
    return make_response(jsonify({"goal": goal.to_dict()}), 200)

@goals_bp.route("/<goal_id>", methods=["DELETE"])
def delete_goal(goal_id):
    goal = validate_model(Goal, goal_id)

    db.session.delete(goal)
    db.session.commit()
    return make_response({"details": f"Goal {goal.goal_id} \"{goal.title}\" successfully deleted"}, 200)