from flask import Blueprint, jsonify, abort, make_response, request
import requests
from app.models.goal import Goal
from app.models.task import Task
from app.routes.helpers import validate_model
from datetime import datetime
from app import db
import os

goals_bp = Blueprint("goals", __name__, url_prefix="/goals")

@goals_bp.route("", methods=["POST"])
def create_goal():
    try:
        request_body = request.get_json()
        new_goal = Goal.from_dict(request_body)
    except KeyError as err:
        return make_response({"details": "Invalid data"}, 400)

    db.session.add(new_goal)
    db.session.commit()

    return jsonify({"goal": new_goal.to_dict()}), 201


@goals_bp.route("", methods=["GET"])
def get_all_goals():

    goals = Goal.query.all()
    
    goal_response = []
    for goal in goals:
        goal_response.append(goal.to_dict())

    return jsonify(goal_response), 200


@goals_bp.route("/<goal_id>", methods=["GET"])
def get_one_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    if goal:
        return {"goal": goal.to_dict()}, 200
    
    else:
        return {'details': 'Invalid data'}, 404
    

@goals_bp.route("<goal_id>", methods=["PUT"])
def update_task(goal_id):
    try:
        goal = validate_model(Goal, goal_id)
    except:
        return jsonify({"Message": "Invalid id"}), 404

    request_body = request.get_json()

    goal.title = request_body["title"]

    db.session.commit()

    return jsonify({"goal": goal.to_dict()}), 200


@goals_bp.route("<goal_id>", methods=["DELETE"])
def delete_goal(goal_id):
    try:
        goal = validate_model(Goal, goal_id)

        db.session.delete(goal)
        db.session.commit()

        message = {"details": f"Goal 1 \"{goal.title}\" successfully deleted"}
        return make_response(message, 200)
    
    except:
        return {'details': 'Invalid data'}, 404

#----------------------------------------------------------

@goals_bp.route("/<goal_id>/tasks", methods=['POST'])
def create_goal_with_tasks(goal_id):

    request_body = request.get_json()
    goal = validate_model(Goal, goal_id)
    task_list = request_body.get("task_ids")

    tasks = []
    for task_id in task_list:
        task = validate_model(Task, task_id)
        task.goal = goal
        tasks.append(task_id)

    db.session.commit()

    message = {
        "id": goal.goal_id, 
        "task_ids": tasks
        }
    return make_response(message, 200)

        
@goals_bp.route("/<goal_id>/tasks", methods=['GET'])
def get_all_tasks_one_goal(goal_id):
    try:
        goal = validate_model(Goal, goal_id)
    except:
        return make_response({"details": "Invalid data"}, 404)

    task_list = []

    for task in goal.tasks:
        task = validate_model(Task, task.id)
        task_list.append(task.to_dict())
        
    message = {
        "id": goal.goal_id,
        "title": goal.title,
        "tasks": task_list
    }
    return make_response((message, 200))