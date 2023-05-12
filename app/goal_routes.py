from os import abort
from app import db
from app.models.goal import Goal
from app.models.task import Task
from flask import Blueprint, jsonify, abort, make_response, request
from datetime import datetime
import requests  
import os


goals_bp = Blueprint("goal", __name__, url_prefix="/goals")


@goals_bp.route("", methods=["POST"])
def create_goal():
    request_body = request.get_json()
    if "title" not in request_body:
        return make_response(jsonify({"details": "Invalid data"}), 400)
    
    new_goal = Goal.from_dict(request_body)
    db.session.add(new_goal)
    db.session.commit()

    return make_response(jsonify(new_goal.to_dict()), 201)


@goals_bp.route("", methods=["GET"])
def get_goals():
    goals = Goal.query.all()
    goal_list = [goal.to_dict()["goal"]for goal in goals]
    return make_response(jsonify(goal_list), 200)


@goals_bp.route("/<goal_id>", methods=["GET"])
def read_one_goal(goal_id):
    goal = Goal.validate_goal(goal_id)
    return make_response(jsonify(goal.to_dict()), 200)


@goals_bp.route("/<goal_id>", methods=["PUT"])
def update_goal(goal_id):
    goal = Goal.validate_goal(goal_id)
    request_body = request.get_json()
    goal.title = request_body["title"]
    db.session.commit()
    return make_response(jsonify(goal.to_dict()), 200)


@goals_bp.route("/<goal_id>", methods=["DELETE"])
def delete_goal(goal_id):
    goal = Goal.validate_goal(goal_id)
    db.session.delete(goal)
    db.session.commit()
    return make_response(jsonify({"details": f'Goal {goal_id} "{goal.title}" successfully deleted'}))


@goals_bp.route("/<goal_id>/tasks", methods=["POST"])
def add_tasks_to_goal(goal_id):
    goal = Goal.validate_goal(goal_id)

    data = request.json
    task_ids = data.get("task_ids", [])
    tasks = Task.query.filter(Task.task_id.in_(task_ids)).all()

    goal.tasks.extend(tasks)

    db.session.commit()

    return {
        "id": goal.goal_id,
        "task_ids": task_ids
    }, 200



@goals_bp.route("/<goal_id>/tasks", methods=["GET"])
def get_tasks_for_goal(goal_id):
    goal = Goal.validate_goal(goal_id)
    tasks = Task.query.filter_by(goal_id = goal.goal_id).all()
    task_list = []
    
    for task in tasks:
        task_dict = {
            "id": task.task_id,
            "goal_id": goal.goal_id,
            "title": task.title,
            "description": task.description,
            "is_complete": task.completed_at is not None
        }
        task_list.append(task_dict)

    response_body = {
        "id": goal.goal_id,
        "title": goal.title,
        "tasks": task_list
    }

    return make_response(jsonify(response_body), 200)


# @goals_bp.route("/tasks/<task_id>", methods=["GET"])
# def get_task(task_id):
#     task = Task.validate_task(task_id)
#     task_dict = task.to_dict_with_goal_id()
    
#     return jsonify(task_dict), 200      

