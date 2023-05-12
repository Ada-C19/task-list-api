from flask import Blueprint, jsonify, abort, make_response, request
from app import db
from app.models.task import Task
from app.models.goal import Goal
from .task_routes import validate_model
from datetime import datetime
import requests

goals_bp = Blueprint("goals",__name__,url_prefix="/goals")

@goals_bp.route("", methods=["POST"])
def create_goal():

    request_body = request.get_json()

    
    try:
        new_goal = Goal(title=request_body["title"])

    except:
        abort(make_response({
        "details": "Invalid data"
    }, 400)) 

    db.session.add(new_goal)
    db.session.commit()


    return make_response(jsonify({"goal":{
        "id" : new_goal.goal_id,
        "title" : new_goal.title,
        }}),201)

@goals_bp.route("", methods=["GET"])
def get_goals():
    
    goals = Goal.query.all()

    goals_response = [] 

    for goal in goals:
        goals_response.append(
            {
                "id":goal.goal_id,
                "title":goal.title
            }
        )
    
    return jsonify(goals_response)

@goals_bp.route("/<goal_id>", methods=["GET"])
def get_one_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    
    return {"goal":{
        "id": goal.goal_id,
        "title" : goal.title
    }}, 200

@goals_bp.route("/<goal_id>", methods=["PUT"])
def update_one_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    
    request_body = request.get_json()

    goal.title = request_body["title"]
    
    db.session.commit()

    return make_response(jsonify({"goal":{
        "id" : goal.goal_id,
        "title" : goal.title,
        }}),200)

@goals_bp.route("/<goal_id>", methods=["DELETE"])
def remove_one_goal(goal_id):
    goal = validate_model(Goal, goal_id)

    db.session.delete(goal)
    db.session.commit()



    return make_response({
        "details": f'{Goal.__name__} {goal_id} "{goal.title}" successfully deleted'
    }), 200