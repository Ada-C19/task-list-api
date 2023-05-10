from flask import Blueprint, jsonify, abort, make_response, request
from app.models.goal import Goal
from app.models.task import Task
from app.routes.helper_funcs import get_valid_item_by_id
from app import db

# All routes for goals start with "/goals" URL prefix
goals_bp = Blueprint("goals", __name__, url_prefix="/goals")


@goals_bp.route("", methods=['POST'])
def create_goal():
    request_body = request.get_json()

    if "title" not in request_body:
        return {
            "details": "Invalid data"
        }, 400
    new_goal = Goal.from_dict(request_body)

    db.session.add(new_goal)
    db.session.commit()

    return {
        "goal": new_goal.to_dict()
    }, 201


@goals_bp.route("", methods=["GET"])
def handle_get_goals_request():
    sort_query = request.args.get("sort")

    if sort_query:
        if sort_query == "asc":
            goals = Goal.query.order_by(Goal.title.asc())
        elif sort_query == "desc":
            goals = Goal.query.order_by(Goal.title.desc())
    else:
        goals = Goal.query.all()

    goals = Goal.query.all()
    
    goal_response = []
    for goal in goals:
        goal_response.append(goal.to_dict())

    return jsonify(goal_response), 200


@goals_bp.route("/<goal_id>", methods=["GET"])
def handle_get_single_goal(goal_id):
    goal = get_valid_item_by_id(Goal, goal_id)

    return {
        "goal": goal.to_dict()
    }, 200


@goals_bp.route("/<goal_id>", methods=["PUT"])
def update_one_goal(goal_id):
    request_body = request.get_json()
    if "title" not in request_body:
        return {
            "details": "Invalid data"
        }, 400
    goal_to_update = get_valid_item_by_id(Goal, goal_id)
    
    goal_to_update.title = request_body["title"]

    db.session.commit()

    return {
        "goal": goal_to_update.to_dict()
    }, 200


@goals_bp.route("/<goal_id>", methods=["DELETE"])
def delete_one_goal(goal_id):
    goal_to_delete = get_valid_item_by_id(Goal, goal_id)

    db.session.delete(goal_to_delete)
    db.session.commit()

    return {'details': f'Goal {goal_to_delete.goal_id} "{goal_to_delete.title}" successfully deleted'}, 200


@goals_bp.route("/<goal_id>/tasks", methods=["POST"])
def assign_tasks_to_goal(goal_id):
    goal = get_valid_item_by_id(Goal, goal_id)

    request_body = request.get_json()
    tasks = request_body["task_ids"]

    for task_id in tasks:
        task = get_valid_item_by_id(Task, task_id)
        task.goal_id = goal.goal_id

    db.session.commit()

    return {
        "id": goal.goal_id,
        "task_ids": tasks
    }, 200


@goals_bp.route("/<goal_id>/tasks", methods=["GET"])
def get_tasks_by_goal(goal_id):
    goal = get_valid_item_by_id(Goal, goal_id)

    tasks = goal.tasks
    tasks_by_goal_response = []

    for task in tasks:
        tasks_by_goal_response.append(task.to_dict())

    return {
        "id": goal.goal_id,
        "title": goal.title,
        "tasks": tasks_by_goal_response
    }, 200