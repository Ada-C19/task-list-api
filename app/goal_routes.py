from app import db
from app.models.goal import Goal
from flask import Blueprint, jsonify, abort, make_response, request
# import datetime
# import requests
# from app import token 

goal_bp = Blueprint("goals", __name__, url_prefix="/goals")

def validate_goal(id):
    try:
        id = int(id)
    except:
        abort(make_response({"message": f"Goal {id} is invalid"}, 400))

    goal = Goal.query.get(id)

    if not goal:
        abort(make_response({"message": f"Goal {id} not found"}, 404))

    return goal

@goal_bp.route("", methods=["POST"])
def create_goal():
    if request.method == "POST":
        request_body = request.get_json()
        if "title" not in request_body:
            return make_response(jsonify({"details": "Invalid data"}), 400)

    new_goal = Goal(
        title = request_body["title"]
    )
    
    db.session.add(new_goal)
    db.session.commit()
    goal_dict = dict(goal=new_goal.to_dict())
    
    return make_response(jsonify(goal_dict), 201)

@goal_bp.route("", methods=["GET"])
def get_goals():
    sort = request.args.get("sort")
    
    if sort == "asc":
        goals = Goal.query.order_by(Goal.title.asc()).all()
    else:
        goals = Goal.query.order_by(Goal.title.desc()).all()
    
    goals_list = []
    for goal in goals:
        goals_list.append(goal.to_dict())
    return jsonify(goals_list)

@goal_bp.route("/<id>", methods=["GET"])
def get_one_goal(id):
    goals = validate_goal(id)
    goal_dict = dict(goal=goals.to_dict())
    
    return make_response(jsonify(goal_dict), 200)

@goal_bp.route("/<id>", methods=["PUT"])
def update_goal(id):
    goal = validate_goal(id)
    goal_data = request.get_json()
    
    goal.title = goal_data["title"]
    
    db.session.commit()
    
    goal_dict = dict(goal=goal.to_dict())
    return make_response(jsonify(goal_dict), 200)

@goal_bp.route("/<id>", methods=["DELETE"])
def delete_one_goal(id):
    goal = validate_goal(id)
    
    deleted_response = {
        "details": f'Goal {goal.goal_id} "{goal.title}" successfully deleted'
    }
    
    db.session.delete(goal)
    db.session.commit()
    
    return make_response(jsonify(deleted_response), 200)