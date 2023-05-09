from flask import Blueprint, request, jsonify, abort, make_response
from datetime import datetime
import requests, os
from app.models.goal import Goal
from app import db
from app.routes.routes_helper_function import handle_valid_id

#Blueprint for goals, all routes have url prefix (/goals)
goals_bp = Blueprint("goals_bp", __name__, url_prefix="/goals")

@goals_bp.route("", methods=["POST"])
def create_goal():
    request_body = request.get_json()
    if 'title' not in request_body:
        return {"details": "Invalid data"}, 400
    
    new_goal = Goal(title=request_body["title"])

    db.session.add(new_goal)
    db.session.commit()

    return {
        "goal":{
            "id":new_goal.goal_id,
            "title":new_goal.title
        }
    }, 201

@goals_bp.route("", methods=["GET"])
def read_all_goals():
    #Retrieve a list of all the goal objects in database
    all_goals = Goal.query.all() 
    goals_response = []
    for goal in all_goals:
        goals_response.append(goal.to_dict())

    return jsonify(goals_response), 200

@goals_bp.route("<goal_id>", methods=["GET"])
def get_goal(goal_id):
    goal = handle_valid_id(Goal, goal_id)

    return {"goal": goal.to_dict()}, 200

@goals_bp.route("<goal_id>", methods=["PUT"])
def update_goal(goal_id):
    goal_to_update = handle_valid_id(Goal, goal_id)
    request_body = request.get_json()
    goal_to_update.title = request_body["title"]
    
    db.session.commit()

    return {"goal": goal_to_update.to_dict()}, 200

@goals_bp.route("<goal_id>", methods=["DELETE"])
def delete_goal(goal_id):
    goal_to_delete = handle_valid_id(Goal, goal_id)
    db.session.delete(goal_to_delete)
    db.session.commit()

    return {
        "details": f'Goal {goal_id} "{goal_to_delete.title}" successfully deleted'
    }, 200