from flask import abort, Blueprint, jsonify, make_response, request
from app import db
from app.models.task import Task
from app.models.goal import Goal
from app.routes.task_routes import verify_item
from datetime import datetime
import requests

goal_bp = Blueprint("goal", __name__, url_prefix="/goals")

@goal_bp.route("", methods=["POST"])
def add_goal():
    request_body = request.get_json()
    verify_goal_inputs(request_body)

    new_goal = Goal.from_dict(request_body)

    db.session.add(new_goal)
    db.session.commit()

    response_dict = message_for_only_one_goal(new_goal)

    return make_response(response_dict, 201)

@goal_bp.route("", methods=["GET"])
def get_goals():
    response_list = []
    all_goals = Goal.query.all()

    for goal in all_goals:
        response_list.append(goal.to_dict())

    return jsonify(response_list), 200

@goal_bp.route("/<goal_id>", methods=["GET"])
def get_one_goal(goal_id):
    goal = verify_item(Goal, goal_id)

    response_dict = message_for_only_one_goal(goal)

    return jsonify(response_dict), 200

@goal_bp.route("/<goal_id>", methods=["PUT"])
def update_one_goal(goal_id):
    goal = verify_item(Goal, goal_id)
    request_body = request.get_json()

    goal.title = request_body["title"]
    db.session.commit()

    response_dict = message_for_only_one_goal(goal)

    return jsonify(response_dict), 200

@goal_bp.route("/<goal_id>", methods=["DELETE"])
def delete_one_goal(goal_id):
    goal = verify_item(Goal, goal_id)

    db.session.delete(goal)
    db.session.commit()

    return make_response({"details": f"Goal {goal.goal_id} \"{goal.title}\" successfully deleted"})

@goal_bp.route("/<goal_id>/tasks", methods=["POST"])
def add_tasks_to_goal(goal_id):
    goal = verify_item(Goal, goal_id)

    request_body = request.get_json()
    try:
        tasks = request_body["task_ids"]
    except KeyError:
        abort(make_response({"details": "Invalid data"}, 400))
    
    for task_id in tasks:
        task = verify_item(Task, task_id)
        task.goal_id = goal.goal_id

    db.session.commit()
    return make_response({"id": goal.goal_id, "task_ids": tasks}, 200)

@goal_bp.route("/<goal_id>/tasks", methods=["GET"])
def get_tasks_from_goal(goal_id):
    goal = verify_item(Goal, goal_id)

    return make_response(goal.to_dict_with_tasks(), 200)

def message_for_only_one_goal(goal):
    return {"goal": goal.to_dict()}

def verify_goal_inputs(request_body):
    if "title" in request_body:
        return request_body
    abort(make_response({"details": "Invalid data"}, 400))