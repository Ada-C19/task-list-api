from app import db
from app.models.task import Task
from app.models.goal import Goal
from app.routes.helpers import create_item, get_all_items, get_item, \
    update_item, delete_item, validate_model
from flask import Blueprint, request, make_response

goals_bp = Blueprint("goals", __name__, url_prefix="/goals")

@goals_bp.route("", methods=["POST"])
def create_goal():
    return create_item(Goal)

@goals_bp.route("", methods=["GET"])
def get_all_goals():
    return get_all_items(Goal)

@goals_bp.route("/<goal_id>", methods=["GET"])
def get_goal(goal_id):
    return get_item(Goal, goal_id)

@goals_bp.route("/<goal_id>", methods=["PUT"])
def update_goal(goal_id):
    return update_item(Goal, goal_id)

@goals_bp.route("/<goal_id>", methods=["DELETE"])
def delete_goal(goal_id):
    return delete_item(Goal, goal_id)

@goals_bp.route("/<goal_id>/tasks", methods=["POST"])
def add_tasks_to_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    request_body = request.get_json()
    task_ids = request_body["task_ids"]

    for task in goal.tasks:
        task.goal_id = None

    for task_id in task_ids:
        task = validate_model(Task, task_id)
        task.goal_id = goal.id
    
    goal.title = request.args.get("title", goal.title)

    db.session.commit()

    return make_response({"id": goal.id, "task_ids": task_ids}, 200)

@goals_bp.route("/<goal_id>/tasks", methods=["GET"])
def get_tasks_for_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    return make_response(goal.to_dict(tasks=True), 200)