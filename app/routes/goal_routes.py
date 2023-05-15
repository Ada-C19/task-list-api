from flask import Blueprint, jsonify, abort, make_response, request
from app.models.goal import Goal
from app.routes.routes import validate_model
from datetime import datetime
from app import db

goals_bp = Blueprint("goals", __name__, url_prefix="/goals")

@goals_bp.route("", methods=["POST"])
def create_goal():
    request_body = request.get_json()
    if "title" not in request_body:
        abort(make_response({"details": "Invalid data"}, 400))
    

    new_goal = Goal(title=request_body["title"])
    db.session.add(new_goal)
    db.session.commit()
    return make_response(jsonify({"goal": new_goal.to_dict()}), 201)

@goals_bp.route("", methods=["GET"])
def read_all_goals():
    goals = Goal.query.all()
    goal_response = []

    for goal in goals:
        goal_response.append(goal.to_dict())
    return jsonify(goal_response)

@goals_bp.route("/<goal_id>", methods=["GET"])
def read_one_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    return make_response(jsonify({"goal":goal.to_dict()}), 200)



@goals_bp.route("/<goal_id>", methods=["PUT"])
def update_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    request_body = request.get_json()

    goal.title = request_body["title"]
    
    db.session.commit()
    return make_response({"goal":goal.to_dict()}, 200)

@goals_bp.route("/<goal_id>", methods=["DELETE"])
def delete_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    
    db.session.delete(goal)
    db.session.commit()

    return make_response({"details": 'Goal 1 "Build a habit of going outside daily" successfully deleted'}, 200)
