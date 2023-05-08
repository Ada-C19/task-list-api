from flask import Blueprint, jsonify, request, make_response, abort
from sqlalchemy import asc, desc
from app import db
from app.models.goal import Goal
from app.models.task import Task
from datetime import datetime
from slack_sdk import WebClient
import os
import requests
from slack_sdk.errors import SlackApiError


goal_bp = Blueprint("goals", __name__, url_prefix="/goals")


def validate_item(model, item_id):
    try:
        item_id = int(item_id)
    except ValueError:
        return abort(make_response({"details": "Invalid data"}, 400))
    
    item = model.query.get(item_id)

    if not item:
        return abort(make_response({"details": f"id {item_id} not found"}, 404))
    
    return item


@goal_bp.route("", methods=["POST"])
def add_goals():
    request_body = request.get_json()
    
    if "title" not in request_body:
        return {f"details": "Invalid data"}, 400
    
    new_goal = Goal(title=request_body["title"])

    db.session.add(new_goal)
    db.session.commit()

    return make_response(jsonify({"goal": new_goal.goal_to_dict()}), 201)


@goal_bp.route("", methods=["GET"])
def get_all_goals():
    response = []

    all_goals = Goal.query.all()
    
    for goal in all_goals:
        response.append(goal.goal_to_dict())

    return make_response(jsonify(response), 200)


@goal_bp.route("/<goal_id>", methods=["GET"])
def get_one_goal(goal_id):
    goal = validate_item(Goal, goal_id)
    return make_response(jsonify({"goal": goal.goal_to_dict()}), 200)


@goal_bp.route("/<goal_id>", methods=["PUT"])
def update_goal(goal_id):
    goal = validate_item(Goal, goal_id)

    request_body = request.get_json()

    goal.title = request_body["title"]

    db.session.commit()

    return make_response(jsonify({"goal": goal.goal_to_dict()}), 200)


@goal_bp.route("/<goal_id>", methods=["DELETE"])
def delete_one_task(goal_id):
    goal = validate_item(Goal, goal_id)

    db.session.delete(goal)

    db.session.commit()

    return {"details": f'Goal {goal_id} "{goal.title}" successfully deleted'}, 200


@goal_bp.route("/<goal_id>/tasks", methods=["POST"])
def create_task(goal_id):
    goal = validate_item(Goal, goal_id)

    request_body = request.get_json()

    task_ids = request_body["task_ids"]

    for task_id in task_ids:
        new_task = validate_item(Task, task_id)
        goal.tasks.append(new_task)

    db.session.commit()

    return {"id": int(goal_id), "task_ids": task_ids}, 200

@goal_bp.route("/<goal_id>/tasks", methods=["GET"])
def get_tasks_one_goal(goal_id):

    goal = validate_item(Goal, goal_id)

    goal_dict = goal.goal_to_dict()
    goal_dict["tasks"]= []

    for task in goal.tasks:
        task_dict = task.to_dict()
        task_dict["goal_id"] = int(goal_id)
        goal_dict["tasks"].append(task_dict)


    return jsonify(goal_dict), 200

    
