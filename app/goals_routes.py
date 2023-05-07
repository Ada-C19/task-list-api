from app import db
from flask import Blueprint, request, make_response, jsonify
from app.models.goal import Goal
from app.models.task import Task
from .routes_helpers import validate_model, slack_call
from sqlalchemy import text
from datetime import datetime

goals_bp = Blueprint("goals", __name__, url_prefix="/goals")

@goals_bp.route("", methods=["POST"])
def create_goal():
    request_body = request.get_json()
    new_goal = Goal.from_dict(request_body)

    db.session.add(new_goal)
    db.session.commit()

    new_goal = new_goal.to_dict()

    return make_response({"goal":new_goal}, 201)

@goals_bp.route("/<id>", methods=["PUT"])
def update_goal(id):
    goal = validate_model(Goal, id)
    request_body = request.get_json()

    goal.title = request_body['title'],
    
    db.session.commit()

    goal = goal.to_dict()

    return make_response({"goal":goal}, 200)

@goals_bp.route("", methods=["GET"])
def handle_goals():
    if request.args.get("sort") == "asc":
        goals = Goal.query.order_by(text("title asc"))
    elif request.args.get("sort") == "desc":
        goals = Goal.query.order_by(text("title desc"))
    else:
        goals = Goal.query.all()
    goals_response = [Goal.to_dict(goal) for goal in goals]

    return make_response(jsonify(goals_response),200)

@goals_bp.route("/<goal_id>", methods=["GET"])
def handle_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    goal = goal.to_dict()
    return make_response({"goal":goal}, 200)

@goals_bp.route("/<id>", methods=["DELETE"])
def delete_goal(id):
    goal = validate_model(Goal, id)

    db.session.delete(goal)
    db.session.commit()

    return make_response({"details":f'Goal 1 "{goal.title}" successfully deleted'}, 200)

@goals_bp.route("/<goal_id>/tasks", methods=["GET"])
def read_tasks(goal_id):

    goal = validate_model(Goal, goal_id)

    tasks_response = [Task.to_dict(task) for task in goal.tasks]
    
    return make_response({"id": goal.goal_id,"tasks":tasks_response, "title": goal.title}, 200)

@goals_bp.route("/<goal_id>/tasks", methods=["POST"])
def post_task_ids(goal_id):
    goal = validate_model(Goal, goal_id)
    request_body = request.get_json()

    tasks = Task.query.filter(Task.task_id.in_(request_body['task_ids'])).all()
    for task in tasks:
        goal.tasks.append(task)
    
    db.session.commit()

    added_task_ids = [task.task_id for task in tasks]

    return make_response({"id":goal.goal_id,"task_ids":added_task_ids}, 200)