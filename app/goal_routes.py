from app import db
from flask import Blueprint, request, make_response, jsonify, abort
from app.models.goal import Goal
import datetime, requests, json, os
from app.task_routes import validate_model
from app.models.task import Task

goals_bp = Blueprint("goals_bp", __name__, url_prefix="/goals")




# CREATES NEW GOALS
@goals_bp.route("", methods=["POST"])
def create_new_goal():

    try:
        request_body = request.get_json()
        new_goal = Goal(title=request_body["title"])

    except: 
        return make_response({"details": "Invalid data"}), 400
    
    db.session.add(new_goal)
    db.session.commit()

    return make_response({"goal": new_goal.to_dict()}), 201

# READS ALL TASKS
@goals_bp.route("", methods=["GET"])
def read_all_tasks():
    
    goals = Goal.query.all()

    goals_response = []
    
    for goal in goals:
        goals_response.append(goal.to_dict())

    return jsonify(goals_response), 200

# READS ONE GOAL
@goals_bp.route("/<goal_id>", methods=["GET"])
def read_one_task(goal_id):
    goal = validate_model(Goal, goal_id)
    
    return {"goal": goal.to_dict()}, 200
    
# UPDATES ONE GOAL    
@goals_bp.route("/<goal_id>", methods=["PUT"])
def update_one_goal(goal_id):
    goal = validate_model(Goal, goal_id)

    request_body = request.get_json()

    goal.title = request_body["title"]

    db.session.commit()

    return make_response({"goal": goal.to_dict()}), 200


# DELETES ONE GOAL
@goals_bp.route("/<goal_id>", methods=["DELETE"])
def delete_one_goal(goal_id):

    try:
        goal = validate_model(Goal, goal_id)
    except:
        return make_response(f"Goal {goal_id} not found"), 404
    
    db.session.delete(goal)
    db.session.commit()

    return {'details': f'Goal {goal_id} "{goal.title}" successfully deleted'}

# NESTED ROUTES - POST
@goals_bp.route("<goal_id>/tasks", methods=["POST"])
def create_task(goal_id):
    goal = validate_model(Goal, goal_id)
    request_body = request.get_json()

    response_body = {
        "id": goal.goal_id,
        "task_ids":request_body["task_ids"]
    }

    for task_id in request_body["task_ids"]:
        task = validate_model(Task, task_id)
        goal.tasks.append(task)

    db.session.commit()
    

    return response_body

# NESTED ROUTES - GET
@goals_bp.route("<goal_id>/tasks",  methods=["GET"])
def get_tasks_of_one_goal(goal_id):
    goal = validate_model(Goal, goal_id)

    tasks_response = []
    for task in goal.tasks:
        tasks_response.append(task.to_dict())

    response_body = {
        "id": goal.goal_id,
        "title": goal.title,
        "tasks": tasks_response
        }

    return response_body