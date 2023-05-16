from app import db
from flask import Blueprint, jsonify, request, make_response, abort
from app.models.task import Task
from app.models.goal import Goal
from app.routes.helper_functions import validate_model
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
    goal = validate_model(Goal, goal_id)

    return make_response(jsonify({"goal" : goal.to_dict()}))


@goals_bp.route("/<goal_id>", methods=["PUT"])
def update_goal(goal_id):
    request_body = request.get_json()
    goal = validate_model(Goal, goal_id)

    goal.title = request_body["title"]

    db.session.commit()

    return make_response(jsonify({"goal" : goal.to_dict()}))


@goals_bp.route("/<goal_id>", methods=["DELETE"])
def delete_goal(goal_id):
    goal = validate_model(Goal, goal_id)    

    db.session.delete(goal)
    db.session.commit()

    response= (f"Goal {goal_id} \"{goal.title}\" successfully deleted")

    return make_response(jsonify({"details": response}))


@goals_bp.route("/<goal_id>/tasks", methods=["POST"])
def add_tasks_to_goal(goal_id):
    request_body = request.get_json()
    task_ids = request_body["task_ids"]

    goal = validate_model(Goal, goal_id)

    for task_id in task_ids:
        task = Task.query.get(task_id)
        task.goal_id = goal.id

    db.session.commit()

    response_message = {"id": int(goal_id), "task_ids": task_ids}

    return make_response(jsonify(response_message))


@goals_bp.route("/<goal_id>/tasks", methods=["GET"])
def get_all_tasks_one_goal(goal_id):
    goal = validate_model(Goal, goal_id)

    response_message = goal.to_dict()
    tasks = Task.query.filter_by(goal=goal)
    tasks_response = []

    if tasks:
        for task in tasks:
            task_dict = task.to_dict()
            task_dict["goal_id"] = int(goal_id)
            tasks_response.append(task_dict)

    response_message["tasks"] = tasks_response

    return make_response(jsonify(response_message))

    
