from app import db
from app.models.goal import Goal
from flask import Blueprint, jsonify, make_response, request, abort
from datetime import datetime
import requests, os

goal_list_bp = Blueprint("goal_list_bp", __name__, url_prefix="/goals")

# Create new goal
@goal_list_bp.route("", methods=["POST"])
def create_goal():
    request_body = request.get_json()
    
    if "title" not in request_body:
        return {"details": "Invalid data"}, 400
    
    new_goal = Goal(title=request_body["title"])
    
    db.session.add(new_goal)
    db.session.commit()
    
    return {"goal": {
        "id": new_goal.goal_id,
        "title": new_goal.title
        } }, 201
    
# Get all saved goals or zero saved goals
@goal_list_bp.route("", methods=["GET"])
def get_goals():
    goals = Goal.query.all()
    goals_response = []
    for goal in goals:
        goals_response.append( {
            "id": goal.goal_id,
            "title": goal.title
            } )
    return jsonify(goals_response)

# Get one goal
@goal_list_bp.route("/<goal_id>", methods=["GET"])
def get_one_goal(goal_id):
    goal = validate_item(Goal, goal_id)
    
    return {"goal": {
        "id": goal.goal_id,
        "title": goal.title
    } }
    
# Update goal
@goal_list_bp.route("/<goal_id>", methods=["PUT"])
def update_goal(goal_id):
    goal = validate_item(Goal, goal_id)
    
    request_data = request.get_json()
    
    goal.title = request_data["title"]
    
    db.session.commit()
    
    return {"goal": {
        "id": goal.goal_id,
        "title": goal.title
    }}
    
# Delete goal
@goal_list_bp.route("/<goal_id>", methods=["DELETE"])
def delete_goal(goal_id):
    goal = validate_item(Goal, goal_id)
    
    db.session.delete(goal)
    db.session.commit()
    
    return {"details": f'Goal {goal.goal_id} "{goal.title}" successfully deleted'}

# No matching Goal: Get, Update, and Delete
# Helper function
def validate_item (model, item_id):
    try:
        item_id_int = int(item_id)
    except:
        return abort(make_response({"message":f"Item {item_id} invalid"}, 400))
    
    item = model.query.get(item_id_int)
    
    if not item:
        return abort(make_response({"message":f"Item {item_id_int} not found"}, 404))
    
    return item    
    
# Helper function
def is_complete_status(completed_at):
    if completed_at is None:
        return False
    else:
        return True