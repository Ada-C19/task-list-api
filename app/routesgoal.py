from app import db
from app.models.goal import Goal
from flask import Blueprint, jsonify, make_response, request, abort
from datetime import datetime


def validate_goal(goal_id):
    try:
        goal_id = int(goal_id)
    except:
        abort(make_response({"message":f"goal {goal_id} invalid"}, 400))

    goal = Goal.query.get(goal_id)

    if not goal:
        abort(make_response({"message":f"goal {goal_id} not found"}, 404))

    return goal



goal_bp = Blueprint("goals", __name__, url_prefix="/goals")
@goal_bp.route("", methods=["POST"])
def create_goals():
    
    request_body = request.get_json()
    try:
        new_goal = Goal.from_dict(request_body)
    except:
        abort(make_response({"details": "Invalid data"},400))
        
    db.session.add(new_goal)
    db.session.commit()
    
    response_body = {"goal": new_goal.to_dict()}
    
    return make_response(jsonify(response_body), 201)

@goal_bp.route("", methods=["GET"])
def read_all_gaols():
    title = request.args.get("title")
    if title:
        goals = Goal.query.filter_by(title=title)
    else:
        goals = Goal.query.all()


    goal_response = []
    for goal in goals:
        goal_response.append(goal.to_dict())

    return jsonify(goal_response)


@goal_bp.route("/<goal_id>", methods=["GET"])
def read_one_goal(goal_id):
    goal = validate_goal(goal_id)
    return make_response(jsonify({"goal":goal.to_dict()}))
# @goal_bp.route("", methods=["PUT"])
# @goal_bp.route("", methods=["DELETE"])