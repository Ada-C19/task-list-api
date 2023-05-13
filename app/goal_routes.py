from app import db
from app.models.goal import Goal
from app.models.task import Task
from app.helper_functions import validate_model
from flask import Blueprint, jsonify, make_response, request
from sqlalchemy import asc, desc


goals_bp = Blueprint("goal_bp", __name__, url_prefix="/goals")

@goals_bp.route("", methods=["POST"])
def create_goal():
    request_body = request.get_json()

    if "title" not in request_body:
        return make_response({"details": "Invalid data"}, 400)
    
    new_goal = Goal.from_dict(request_body)

    db.session.add(new_goal)
    db.session.commit()

    return make_response({"goal": new_goal.to_dict()}, 201)

@goals_bp.route("/<goal_id>/tasks", methods=["POST"])
def create_tasks_under_goal(goal_id):
    request_body = request.get_json()
    goal = validate_model(Goal, goal_id)

    task_list = []
    for task_id in request_body["task_ids"]:
        task = validate_model(Task, task_id)
        task.goal = goal
        task_list.append(task_id)
    
    db.session.commit()

    return make_response({"id": goal.goal_id, "task_ids": task_list}, 200)

@goals_bp.route("", methods=["GET"])
def read_all_goals():
    sort_query = request.args.get("sort")
    if sort_query:
        if sort_query == "asc":
            goals = Goal.query.order_by(Goal.title.asc()).all()
        elif sort_query == "desc":
            goals = Goal.query.order_by(Goal.title.desc()).all()
    else:
        goals = Goal.query.all()
    
    all_goals = [goal.to_dict() for goal in goals]

    return jsonify(all_goals), 200

@goals_bp.route("/<goal_id>", methods=["GET"])
def read_one_goal(goal_id):
    goal = validate_model(Goal, goal_id)

    return make_response({"goal": goal.to_dict()}, 200)

@goals_bp.route("/<goal_id>/tasks", methods=["GET"])
def read_tasks_under_goal(goal_id):
    goal = validate_model(Goal, goal_id)

    task_list = []
    for task in goal.tasks:
        task_list.append(task.to_dict())
    
    return make_response({"id": goal.goal_id, "title": goal.title, "tasks": task_list})

@goals_bp.route("/<goal_id>", methods=["PUT"])
def update_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    request_body = request.get_json()
    goal.title = request_body["title"]

    db.session.commit()

    return make_response({"goal": goal.to_dict()}, 200)

@goals_bp.route("/<goal_id>", methods=["DELETE"])
def delete_goal(goal_id):
    goal = validate_model(Goal, goal_id)

    db.session.delete(goal)
    db.session.commit()

    return make_response({"details":f"Goal {goal.goal_id} \"{goal.title}\" successfully deleted"}), 200