from app import db
from app.models.task import Task
from app.models.goal import Goal
from flask import Blueprint, jsonify, make_response, request, abort
from sqlalchemy.types import DateTime
from sqlalchemy.sql.functions import now
import requests, json
import os

goal_bp = Blueprint("goal_bp", __name__, url_prefix="/goals")

def validate_model_goal(cls, model_id):
    try:
        model_id = int(model_id)
    except:
        abort(make_response({"message": f"{cls.__name__} {model_id} invalid"}, 400))

    goal = cls.query.get(model_id)

    if not goal:
        abort(make_response({"message": f"{cls.__name__} {model_id} not found"}, 404))
    
    return goal

@goal_bp.route("", methods=["POST"])
def create_goal():
    request_body = request.get_json()
    is_valid_goal = "title" in request_body
    if not is_valid_goal:
        abort(make_response({"details": "Invalid data"}, 400))
    
    new_goal = Goal.goal_from_dict(request_body)

    db.session.add(new_goal)
    db.session.commit()

    response_body = {
        "goal": new_goal.goal_to_dict()
    }

    return make_response(jsonify(response_body), 201)

@goal_bp.route("", methods=["GET"])
def get_all_goals():
    # goal = validate_model_goal()
    sort_query = request.args.get("sort")
    if sort_query == "asc":
        goals = Goal.query.order_by(Goal.title)
    elif sort_query == "desc":
        goals = Goal.query.order_by(Goal.title.desc())
    else:
        goals = Goal.query.all()

    goals_response = [goal.goal_to_dict() for goal in goals]
    return jsonify(goals_response)

@goal_bp.route("/<goal_id>", methods=["GET"])
def get_one_goal(goal_id):
    goal = validate_model_goal(Goal, goal_id)
    response_body = {
        "goal": goal.goal_to_dict()
    }
    return jsonify(response_body)

@goal_bp.route("/<goal_id>", methods=["PUT"])
def update_goal(goal_id):
    goal = validate_model_goal(Goal, goal_id)
    request_body = request.get_json()
    goal.title = request_body["title"]

    db.session.commit()

    response_body = {
        "goal": goal.goal_to_dict()
    }
    return response_body

@goal_bp.route("/<goal_id>", methods=["DELETE"])
def delete_goal(goal_id):
    goal = validate_model_goal(Goal, goal_id)
    response_body = {
        "details": f'Goal {goal.goal_id} \"{goal.title}\" successfully deleted'
    }

    db.session.delete(goal)
    db.session.commit()

    return response_body

@goal_bp.route("/<goal_id>/tasks", methods=["POST"])
def create_task(goal_id):
    # validate goal_id
    goal = validate_model_goal(Goal, goal_id)

    # specify request format
    request_body = request.get_json()
    new_tasks = Task(
        task_ids = request_body["task_ids"],
        goal=goal
    )
    
    # create 3 new tasks for the goal_id given
    # new_tasks = [Task.task_from_dict(request_body) for task in task_ids]

    db.session.add(new_tasks)
    db.session.commit()

    response_body = {
        "id": int(goal_id),
        "task_ids": new_tasks
    }

    return response_body

@goal_bp.route("/<goal_id>/tasks", methods=["GET"])
def get_tasks_one_goal(goal_id):

    goal = validate_model_goal(Goal, goal_id)

    tasks_response = []
    for task in goal.tasks:
        tasks_response.append(
            {
            "id": task.task_id,
            "title": task.title,
            "description": task.description,
            "completed_at": None
            }
        )
    
    # tasks_response = [response_dict for task in goal.tasks]

    return jsonify(tasks_response)
