from flask import Blueprint, request, make_response, jsonify, abort
from ..models.task import Task
from ..models.goal import Goal
from app import db
from datetime import datetime
from flask import Flask 
from app.routes.helper import send_requsest_to_slack, validate_model

goal_bp = Blueprint("goal_bp", __name__, url_prefix="/goals")

# Get, post, update and delete for goals===================================
# Read all goals:
@goal_bp.route("", methods=["GET"])
def get_all_goals():
    goal_objects = Goal.query.all()
    goal_list = [goal.to_dict() for goal in goal_objects]
    return make_response(jsonify(goal_list), 200)
 
 # Read one goal:
@goal_bp.route("/<goal_id>", methods=["GET"])
def get_one_goal(goal_id):
    goal_object = validate_model(Goal, goal_id)
    return make_response({"goal" : goal_object.to_dict()}, 200)

# Create goal:
@goal_bp.route("", methods=["POST"])
def create_a_goal():
    try:
        request_body_dict = request.get_json()
        goal_object = Goal.from_dict(request_body_dict)
        db.session.add(goal_object)
        db.session.commit()
        return make_response({"goal" : goal_object.to_dict()}, 201)
    except(KeyError):
        return make_response({"details": "Invalid data"}, 400)
    
# Replace a goal
@goal_bp.route("/<goal_id>", methods=["PUT"])
def replace_a_goal(goal_id):
    goal_object = validate_model(Goal, goal_id)
    goal_request_body_dict = request.get_json()
    goal_object.title = goal_request_body_dict.get("title")
    db.session.commit()
    return make_response({"goal" : goal_object.to_dict()}, 200)

# Delete a goal
@goal_bp.route("/<goal_id>", methods=["DELETE"])
def delete_a_goal(goal_id):
    response_object = validate_model(Goal, goal_id)
    db.session.delete(response_object)
    db.session.commit()
    return make_response({
        'details': f'Goal {response_object.goal_id} "{response_object.title}" successfully deleted'}, 200)

# one to many ===============================================
# Get tasks with a specific id
@goal_bp.route("<goal_id>/tasks", methods=["GET"])
def get_all_tasks_associates_one_goal(goal_id):
    goal_object= validate_model(Goal, goal_id)
    task_list = [task.to_dict() for task in goal_object.tasks]
    return make_response(goal_object.add_goal_keys(task_list), 200)

# Post tasks
@goal_bp.route("<goal_id>/tasks", methods=["POST"]) 
def post_task_belong_to_specific_goal(goal_id):
    goal_object= validate_model(Goal, goal_id)
    request_body_dict = request.get_json()
    for id in request_body_dict["task_ids"]:
        task = Task.query.get(id)
        task.goal_id = goal_id
    
    db.session.add(goal_object)
    db.session.commit()
    response = {"id": goal_object.goal_id,
                "task_ids":request_body_dict["task_ids"]}
    return make_response(response, 200)

