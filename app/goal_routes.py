from flask import Blueprint, jsonify, abort, make_response, request
from app import db
from app.models.task import Task
from app.models.goal import Goal
from app.task_routes import validate_model
from datetime import datetime
import requests
import os

goals_bp = Blueprint("goals_bp",__name__, url_prefix="/goals")

@goals_bp.route("", methods=["POST"])
def post_goal():
    request_body = request.get_json()
    
    if not request_body.get("title"):
        return jsonify({"details": "Invalid data"}), 400
    
    new_goal = Goal(
        title=request_body["title"]
        )

    db.session.add(new_goal)
    db.session.commit()

    return new_goal.to_dic(), 201

@goals_bp.route("", methods=["GET"])
def read_all_goals():
    sort_query = request.args.get("sort")
    
    if sort_query:
        goals = Goal.query.order_by(Goal.title).all()
    else:
        goals = Goal.query.all()

    goal_response = []
    for goal in goals:
        goal_response.append(goal.to_dic()["goal"])

    return jsonify(goal_response), 200

@goals_bp.route("/<goal_id>", methods=["GET"])
def read_goal_by_id(goal_id):
    goal = validate_model(Goal, goal_id)

    return goal.to_dic(), 200

@goals_bp.route("/<goal_id>", methods=["PUT"])
def update_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    request_body = request.get_json()

    title = request_body["title"]

    db.session.commit()

    return goal.to_dic()

@goals_bp.route("/<goal_id>", methods=["DELETE"])
def delete_goal(goal_id):
    goal = validate_model(Goal, goal_id)

    db.session.delete(goal)
    db.session.commit()

    return make_response({'details': f'Goal {goal_id} \"{goal.title}\" successfully deleted'}, 200)

@goals_bp.route("<goal_id>/tasks", methods=["POST"])
def add_tasks_to_goal_by_id(goal_id):
    goal = validate_model(Goal, goal_id)
    request_body = request.get_json()

    for id in request_body["task_ids"]:
        task = validate_model(Task, id)
        goal.tasks.append(task)
    
    db.session.commit()
    
    return {
        "id": goal.goal_id,
        "task_ids": request_body["task_ids"]
    }

@goals_bp.route("/<goal_id>/tasks", methods=["GET"])
def get_task_by_id(goal_id):
    goal = validate_model(Goal, goal_id)

    tasks_response = goal.task_by_goal_id()
    
    return jsonify(tasks_response)
    
    

