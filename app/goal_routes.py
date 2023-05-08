from flask import Blueprint
from app import db
from app.models.goal import Goal
from flask import Blueprint, jsonify, make_response, request, abort
from app.task_routes import validate_model
# from sqlalchemy import asc, desc
# from datetime import datetime
# import requests
# import os
# import json


goals_bp = Blueprint("goals", __name__, url_prefix="/goals")


#goals routes:
@goals_bp.route("", methods=["POST"])
def create_goal():
    request_body = request.get_json()
    if not request_body.get("title"):
        abort(make_response({
            "details": "Invalid data"
        }, 400))

    new_goal = Goal.from_dict(request_body)

    db.session.add(new_goal)
    db.session.commit()

    return {
        "goal": new_goal.to_dict()
    }, 201

#este no tiene tests --> get all goals
@goals_bp.route("", methods=["GET"])
def get_goals():
    goals_response = []
    goals = Goal.query.all()

    for goal in goals:
        goals_response.append(goal.to_dict())
    return jsonify(goals_response)


#get goal by id
@goals_bp.route("/<goal_id>", methods=["GET"])
def get_goal_by_id(goal_id):
    goal = validate_model(Goal, goal_id)
    return {
        "goal": goal.to_dict()
    }, 200


#Update goal by id:
@goals_bp.route("/<goal_id>", methods=["PUT"])
def update_goal_by_id(goal_id):
    goal = validate_model(Goal, goal_id)

    request_body = request.get_json()
    goal.title = request_body["title"]

    db.session.commit()

    return {
        "goal": goal.to_dict()
    }

#Delete goal
@goals_bp.route("/<goal_id>", methods=["DELETE"])
def delete_goal(goal_id):
    goal = validate_model(Goal, goal_id)

    db.session.delete(goal)
    db.session.commit()

    return {
        "details": f'Goal {goal_id} "{goal.title}" successfully deleted'
    }


#nested routes:

# POST request to /goals/1/tasks
@goals_bp.route("/<goal_id>/tasks", methods=["POST"])#post?
def post_tasks_ids_with_goals(goal_id):
    goal = validate_model(Goal, goal_id)
    request_body = request.get_json()
    task_ids = request_body.get("task_ids")

    new_goal = Goal(title=goal.title,
                    description=goal.description,
                    task_ids=task_ids)
    #if it is a post and doesnt have a title?
    db.session.add(new_goal)


#getting task of one goal:
@goals_bp.route("/<goal_id>/tasks", methods=["GET"])
def get_task_from_goal(goal_id):
    goal = validate_model(Goal, goal_id)

    tasks_list = []
    for task in goal.tasks:
        tasks_list.append(
            {
            "id": task.id,
            "goal_id": goal.id,
            "title": task.title,
            "description": task.desciption,
            "is_complete": task.complete_at
            }
        )
    return jsonify(tasks_list)
