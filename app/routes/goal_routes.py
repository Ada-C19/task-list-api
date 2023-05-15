from app import db
from flask import Blueprint, jsonify, request, make_response, abort
from app.models.task import Task
from app.models.goal import Goal
from sqlalchemy import text
import datetime
import requests
import os

goals_bp = Blueprint("goals_bp", __name__, url_prefix="/goals")

@goals_bp.route("", methods=["POST"])
def create_goal():
    request_body = request.get_json()
    if "title" not in request_body:
        return make_response({ "details": "Invalid data"}, 400)
    
    new_goal = Goal.from_dict(request_body)

    db.session.add(new_goal)
    db.session.commit()

    response = {"goal" : new_goal.to_dict()}
    
    return make_response(jsonify(response), 201)

@goals_bp.route("", methods = ["GET"])
def read_all_goals():
    goals = Goal.query.all()

    # sort_query = request.args.get("sort")
    # if sort_query == "asc":
    #     goals = Goal.query.order_by(Goal.title.asc()).all()
    # elif sort_query == "desc":
    #     goals = Goal.query.order_by(Goal.title.desc()).all()

    goals_response = []
    if not goals:
        return jsonify(goals_response)
    for goal in goals:
        goals_response.append(
            {
            "id": goal.id,
            "title": goal.title,
            }
            )
    return jsonify(goals_response)

@goals_bp.route("/<goal_id>", methods =["GET"])
def read_one_goal(goal_id):
    try:
        goal_id = int(goal_id)
    except:
        abort(make_response({"message":f"goal {goal_id} invalid"}, 400))
    
    goals = Goal.query.all()
    for goal in goals:
        if goal.id == goal_id:
            return make_response(jsonify({"goal" : goal.to_dict()}))
        
    abort(make_response({"message":f"goal {goal_id} not found"}, 404))


@goals_bp.route("/<goal_id>", methods=["PUT"])
def update_goal(goal_id):
    request_body = request.get_json()
    try: 
        goal_id = int(goal_id)
    except:
        abort(make_response({"message":f"goal {goal_id} invalid"}, 400))
       
    goal = Goal.query.get(goal_id)
    if not goal:
        abort(make_response({"message":f"Goal {goal_id} not found"}, 404))  

    goal.title = request_body["title"]

    db.session.commit()

    return make_response(jsonify({"goal" : goal.to_dict()}))


@goals_bp.route("/<goal_id>", methods=["DELETE"])
def delete_goal(goal_id):
    goal = Goal.query.get(goal_id)

    if not goal:
        abort(make_response({"message":f"Goal {goal_id} not found"}, 404))         

    db.session.delete(goal)
    db.session.commit()

    response= (f"Goal {goal_id} \"{goal.title}\" successfully deleted")

    return make_response(jsonify({"details": response}))