from app import db
from app.models.goal import Goal
from app.models.task import Task
from flask import Blueprint, jsonify, make_response, request, abort
from .routes_helper import validate_model

goals_bp = Blueprint("goals", __name__, url_prefix = "/goals")
@goals_bp.route("", methods=["POST"])
def create_goal():
    request_body = request.get_json()
    if "title" not in request_body:
        return make_response(jsonify({"details": "Invalid data"}), 400)
    # Create a new goal in the database
    new_goal = Goal(
        title=request_body["title"]
    )

    db.session.add(new_goal)
    db.session.commit()

    response_body = dict(goal = new_goal.to_dict())

    return jsonify(response_body), 201

@goals_bp.route("", methods=["GET"])
def get_all_goals():

    goals = Goal.query.all()
    goal_list = [goal.to_dict() for goal in goals]


    return jsonify(goal_list), 200

@goals_bp.route("/<goal_id>", methods=["GET"])
def get_one_goal(goal_id):
    goal = validate_model(Goal,goal_id)
    response_body = dict(goal = goal.to_dict())

    return jsonify(response_body), 200

@goals_bp.route("/<goal_id>", methods=["PUT"])
def update_goal(goal_id):
    goal = validate_model(Goal,goal_id)
    request_body = request.get_json()

    goal.title = request_body["title"]

    db.session.commit()

    response_body = dict(goal = goal.to_dict())

    return jsonify(response_body) , 200

@goals_bp.route("/<goal_id>", methods=["DELETE"])
def delete_goal(goal_id):
    goal = validate_model(Goal, goal_id)

    db.session.delete(goal)
    db.session.commit()

    return make_response({"details": f"Goal {goal.id} \"{goal.title}\" successfully deleted"}, '200 OK')

@goals_bp.route("/<goal_id>/tasks", methods=["POST"])
def adding_task_ids(goal_id):
    goal = validate_model(Goal, goal_id)

    request_body = request.get_json()

    task_ids = request_body.get("task_ids")
    for task_id in task_ids:
        task = validate_model(Task, task_id)
        task.goal_id = goal.id

        db.session.commit()

    task_ids = [task.task_id for task in goal.tasks]

    response_body = {
        "id": goal.id,
        "task_ids": task_ids

    }
    return make_response(response_body), 200

@goals_bp.route("/<goal_id>/tasks", methods=["GET"])
def get_tasks_by_goal_id(goal_id):
    goal = validate_model(Goal,goal_id)
    tasks = Goal.query.get(goal_id).tasks
    task_list= [task.to_dict() for task in tasks]

    response_body = dict(
        id = goal.id,
        title = goal.title,
        tasks = task_list
        )

    return jsonify(response_body), 200
