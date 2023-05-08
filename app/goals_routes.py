from app import db
import os
from app.models.goal import Goal
from flask import Blueprint, jsonify, abort, make_response, request
from app.routes_helper import validate_model

goals_bp = Blueprint("goals_bp", __name__, url_prefix="/goals")

@goals_bp.route("", methods=["POST"])
def create_goal():
    request_body = request.get_json()
    response_body= {}

    if "title" not in request_body:
       response_body = {"details": "Invalid data"}
       return make_response(jsonify(response_body), 400)
    else:
        new_goal = Goal(title=request_body["title"])
        
        db.session.add(new_goal)
        db.session.commit()

        response_body["goal"] = new_goal.to_dict()

    return make_response(jsonify(response_body), 201)

@goals_bp.route("", methods=["GET"])
def read_all_goals():
    goals_response=[]
    goals= Goal.query.all()
        
    goals_response = [goal.to_dict() for goal in goals]

    return jsonify(goals_response)

@goals_bp.route("/<goal_id>", methods=["GET"])
def read_one_goal(goal_id):
    goal= validate_model(Goal,goal_id)
    response_body = {}
    
    response_body["goal"] = goal.to_dict()

    return response_body


@goals_bp.route("/<goal_id>", methods=["PUT"])
def update_goal(goal_id):
    goal= validate_model(Goal, goal_id)

    request_body = request.get_json()
    response_body = {}
    goal.title = request_body["title"]

    response_body["goal"] = goal.to_dict()

    db.session.commit()

    return jsonify(response_body)

@goals_bp.route("/<goal_id>", methods=["DELETE"])
def delete_goal(goal_id):
    goal = validate_model(Goal, goal_id)

    db.session.delete(goal)
    db.session.commit()

    return make_response({"details": f'Goal {goal.goal_id} "{goal.title}" successfully deleted'})