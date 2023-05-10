from flask import Blueprint, make_response, jsonify, request, abort
from app.models.goal import Goal
from app.models.task import Task
from app import db
from .helper_functions import validate_model


goal_bp = Blueprint("goals", __name__, url_prefix="/goals")

@goal_bp.route("", methods=["POST"])
def create_goal():
    request_body = request.get_json()

    try:
        new_goal = Goal.from_dict(request_body)
        db.session.add(new_goal)
        db.session.commit()

        return make_response({"goal":new_goal.to_dict()}, 201)
    except:
        abort(make_response({"details": "Invalid data"}, 400))

@goal_bp.route("", methods=["GET"])
def get_all_goals():
    goals = Goal.query.all()

    goal_list = [goal.to_dict() for goal in goals]

    return make_response(jsonify(goal_list), 200)

@goal_bp.route("/<goal_id>", methods=["GET"])
def get_one_goal(goal_id):
    goal = validate_model(Goal, goal_id)

    return make_response({"goal":goal.to_dict()}, 200)

@goal_bp.route("/<goal_id>", methods=["PUT"])
def update_goal(goal_id):
    goal_data = request.get_json()
    goal_to_update = validate_model(Goal, goal_id)

    goal_to_update.title = goal_data["title"]

    db.session.commit()

    return make_response({"goal": goal_to_update.to_dict()}, 200)

@goal_bp.route("/<goal_id>", methods=["DELETE"])
def delete_goal(goal_id):
    goal_to_delete = validate_model(Goal, goal_id)

    db.session.delete(goal_to_delete)
    db.session.commit()

    message = f'Goal {goal_id} "{goal_to_delete.title}" successfully deleted'
    return make_response({"details":message}, 200)

@goal_bp.route("/<goal_id>/tasks", methods=["POST"])
def create_task(goal_id):
    goal = validate_model(Goal, goal_id)
    tasks_to_add = request.get_json()
    new_tasks_to_add_goal = []

    for task_id in tasks_to_add["task_ids"]:
        new_task = validate_model(Task, task_id)
        new_tasks_to_add_goal.append(new_task)

    goal.tasks = new_tasks_to_add_goal

    db.session.commit()

    return make_response({
        "id": goal.goal_id,
        "task_ids": [task.task_id for task in goal.tasks]
    }, 200)

@goal_bp.route("/<goal_id>/tasks", methods=["GET"])
def get_tasks_for_one_goal(goal_id):
    goal = validate_model(Goal, goal_id)

    tasks_response = [task.to_dict_in_goals() for task in goal.tasks]

    return make_response({
        "id": goal.goal_id,
        "title": goal.title,
        "tasks":tasks_response}, 200)