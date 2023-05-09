from flask import Blueprint, jsonify, abort, make_response, request
from app import db
from app.models.goal import Goal
from app.models.task import Task
from .route_helpers import validate_model
from datetime import datetime
import requests
from dotenv import load_dotenv
import os

goal_bp = Blueprint("goals", __name__, url_prefix="/goals")

@goal_bp.route("", methods=["GET"])
def get_goals():
    goals = Goal.query.all()
    goals_response = [goal.to_dict() for goal in goals]

    return make_response(jsonify(goals_response), 200)


@goal_bp.route("", methods=["POST"])
def create_goal():
    request_body = request.get_json()
    try:
        new_goal = Goal.from_dict(request_body)
    except KeyError:
        abort(make_response(jsonify({"details": "Invalid data"}), 400))

    db.session.add(new_goal)
    db.session.commit()

    return make_response(jsonify({"goal": new_goal.to_dict()}), 201)



@goal_bp.route("/<goal_id>", methods=["GET"])
def get_one_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    return make_response(jsonify({"goal": goal.to_dict()}), 200)


@goal_bp.route("/<goal_id>", methods=["PUT"])
def update_one_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    request_body = request.get_json()
    goal.title = request_body["title"]

    db.session.commit()

    return make_response(jsonify({"goal": goal.to_dict()}), 200)


@goal_bp.route("/<goal_id>", methods=["DELETE"])
def delete_one_goal(goal_id):
    goal = validate_model(Goal, goal_id)

    db.session.delete(goal)
    db.session.commit()

    return make_response(jsonify({"details": f'Goal {goal.id} "{goal.title}" successfully deleted'}), 200)


@goal_bp.route("/<goal_id>/tasks", methods=["POST"])
def assign_tasks_to_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    request_body = request.get_json()
    task_ids = request_body['task_ids']
    tasks = []
    print(f"{tasks=}")
    for id in task_ids:
        print(f"{id=}")
        task = validate_model(Task, id)
        task.goal = goal
        tasks.append(task)
    
    db.session.add_all(tasks)
    db.session.commit()
    return make_response(jsonify(goal.to_dict()))


@goal_bp.route("/<goal_id>/tasks", methods=["GET"])
def get_related_tasks(goal_id):
    pass