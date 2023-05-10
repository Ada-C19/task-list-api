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

    return {
            "goal": {
            "id": new_goal.goal_id,
            "title": new_goal.title
        }
    }, 201

@goals_bp.route("", methods=["GET"])
def read_all_goals():
    goals = Goal.query.all()

    goal_response = []

    for goal in goals:
        goal_response.append({
            "id": goal.goal_id,
            "title": goal.title
        })

    return jsonify(goal_response), 200

@goals_bp.route("/<goal_id>", methods=["GET"])
def read_goal_by_id(goal_id):
    goal = validate_model(Goal, goal_id)

    return {
        "goal": {
            "id": goal.goal_id,
            "title": goal.title
        }
    }, 200

@goals_bp.route("/<goal_id>", methods=["PUT"])
def update_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    request_body = request.get_json()

    title = request_body["title"]

    db.session.commit()

    return {
        "goal": {
            "id": goal.goal_id,
            "title": goal.title
        }
    }

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
    tasks_response = ({
        "id": goal.goal_id,
        "title": goal.title,
        "tasks": []
        })
    for task in goal.tasks:
        tasks_response["tasks"].append({
            "id": task.task_id,
            "goal_id": task.goal_id,
            "title": task.title,
            "description": task.description,
            "is_complete": True if task.completed_at else False
            })
    
    return jsonify(tasks_response)
    
    

