from app import db
from app.models.task import Task
from app.models.goal import Goal
from .task_routes import validate_model
from flask import Blueprint, jsonify, request, make_response, abort
from datetime import datetime
import os
import requests
goal_bp = Blueprint("goal_bp", __name__, url_prefix="/goals")

# ----------------------------- ROUTES FOR GOAL MODEL -------------------------

# create a new goal
@goal_bp.route("",methods=["POST"])
def create_goal():
    request_body = request.get_json()

    try:
        new_goal = Goal.from_dict(request_body)
    except:
        return {"details": "Invalid data"}, 400

    db.session.add(new_goal)
    db.session.commit()

    return {
        "goal":{
            "id": new_goal.goal_id,
            "title": new_goal.title
        }
    }, 201

# One (goal) to many (tasks) relationship 
@goal_bp.route("/<goal_id>/tasks", methods=["POST"])
def update_goal_id_for_task(goal_id):
    goal_from_id = validate_model(Goal, goal_id)

    request_body = request.get_json()

    for i in request_body["task_ids"]:
        task_to_update = validate_model(Task, i)
        task_to_update.goal = goal_from_id
        db.session.commit()

    return make_response(jsonify({
        "id": int(goal_id),
        "task_ids": request_body["task_ids"]
    })), 200


@goal_bp.route("", methods=["GET"])
def read_all_goals():
    goals = Goal.query.all()
    goals_response = []

    for goal in goals:
        goals_response.append(goal.to_dict())

    return jsonify(goals_response), 200


@goal_bp.route("/<goal_id>", methods=["GET"])
def read_one_task(goal_id):
    goal = validate_model(Goal, goal_id)

    return {
        "goal":{
            "id": goal.goal_id,
            "title": goal.title
        }
    }, 200

@goal_bp.route("/<goal_id>", methods=["PUT"])
def update_goal(goal_id):
    goal = validate_model(Goal, goal_id)

    request_body = request.get_json()

    goal.title = request_body["title"]

    db.session.commit()

    return {"goal": goal.to_dict()}



@goal_bp.route("/<goal_id>", methods=["DELETE"])
def delete_goal(goal_id):
    goal = validate_model(Goal, goal_id)
     
    db.session.delete(goal)
    db.session.commit()

    return make_response({"details":f'Goal {goal.goal_id} "{goal.title}" successfully deleted'}, 200)


# get tasks for a speciic goal
@goal_bp.route("/<goal_id>/tasks", methods=["GET"])
def get_tasks_for_specific_goal(goal_id):
    goal = validate_model(Goal, goal_id)

    tasks_response = []

    for task in goal.tasks:
        tasks_response.append({
            "id": task.task_id,
            "goal_id": task.goal_id,
            "title": task.title,
            "description": task.description,
            "is_complete": (task.completed_at != None)
        })

    return {
        "id": goal.goal_id,
        "title": goal.title,
        "tasks": tasks_response
    }
