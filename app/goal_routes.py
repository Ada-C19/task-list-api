from flask import Blueprint, request, jsonify, abort, make_response
from app import db
from app.models.goal import Goal
from app.routes_helper import validate_item_by_id

# Blueprint for goals
goals_bp = Blueprint("goals", __name__, url_prefix="/goals")

@goals_bp.route("", methods=["POST"])
def create_a_goal():
    
    request_body = request.get_json()
    
    try:
        new_goal = Goal(title=request_body["title"])
        
    except KeyError:
        return {
            "details": "Invalid data"
        }, 400
    db.session.add(new_goal)
    db.session.commit()
    
    return {
        "goal": new_goal.to_dict()
    }, 201
    

@goals_bp.route("", methods=["GET"])
def get_saved_goals():
    goals = Goal.query.all()
    goal_response = []
    if goals:
        for goal in goals:
            goal_response.append(goal.to_dict())
    return jsonify(goal_response), 200


@goals_bp.route("/<goal_id>", methods=["GET"])
def get_one_goal(goal_id):
    goal = validate_item_by_id(Goal, goal_id)
    return {
        "goal": goal.to_dict()
    }, 200
    
@goals_bp.route("/<goal_id>", methods=["PUT"])
def update_one_goal(goal_id):
    request_body = request.get_json()
    goal = validate_item_by_id(Goal, goal_id)
    if "title" in request_body:
        goal.title = request_body["title"]
    db.session.commit()
    return {"goal": goal.to_dict()}, 200


@goals_bp.route("/<goal_id>", methods=["DELETE"])
def delete_one_goal(goal_id):
    goal_to_delete = validate_item_by_id(Goal, goal_id)
    
    db.session.delete(goal_to_delete)
    db.session.commit()
    
    return {
        "details": f'Goal {goal_to_delete.goal_id} "{goal_to_delete.title}" successfully deleted'
    }, 200