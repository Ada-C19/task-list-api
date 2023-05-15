from flask import Blueprint, make_response, request
from app.models.goal import Goal
from app.models.task import Task
from app.routes.helpers import validate_model, create_item, get_all_items, get_one_item, update_item, delete_item
from app import db

goals_bp = Blueprint("goals", __name__, url_prefix="/goals")

@goals_bp.route("", methods=["POST"])
def create_goal():
    return create_item(Goal)


@goals_bp.route("", methods=["GET"])
def get_all_goals():
    return get_all_items(Goal)


@goals_bp.route("/<goal_id>", methods=["GET"])
def get_one_goal(goal_id):
    return get_one_item(Goal, goal_id)
    

@goals_bp.route("<goal_id>", methods=["PUT"])
def update_task(goal_id):
    return update_item(Goal, goal_id)
    

@goals_bp.route("<goal_id>", methods=["DELETE"])
def delete_goal(goal_id):
    return delete_item(Goal, goal_id)


@goals_bp.route("/<goal_id>/tasks", methods=['POST'])
def create_goal_with_tasks(goal_id):

    goal = validate_model(Goal, goal_id)
    request_body = request.get_json()
    task_ids = request_body.get("task_ids")

    for task_id in task_ids:
        task = validate_model(Task, task_id)
        task.goal_id = goal.goal_id

    db.session.commit()

    message = {
        "id": goal.goal_id, 
        "task_ids": task_ids
        }

    return make_response(message, 200)

        
@goals_bp.route("/<goal_id>/tasks", methods=['GET'])
def get_all_tasks_one_goal(goal_id):

    goal = validate_model(Goal, goal_id)
    return make_response(goal.to_dict(tasks=True), 200)