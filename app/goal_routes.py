from app import db
from flask import Blueprint, request, make_response, jsonify
from app.models.goal import Goal
from app.models.task import Task
from .routes_helpers import validate_model

goal_bp = Blueprint("goals", __name__, url_prefix="/goals")

@goal_bp.route("", methods=["POST"])
def create_goal():
    request_body = request.get_json()

    new_goal = Goal.from_dict(request_body)

    db.session.add(new_goal)
    db.session.commit()

    return make_response(jsonify({"goal": new_goal.to_dict()}), 201)


@goal_bp.route("", methods=["GET"])
def get_all_goals():
    goal_query = Goal.query

    sort_query = request.args.get("sort")
    title_query = request.args.get("title")

    if sort_query == "title":
        goal_query = goal_query.order_by(Goal.title)

    if title_query:
        goal_query = goal_query.filter(Goal.title.ilike(f"%{title_query}%"))
    
    goals_response = [goal.to_dict() for goal in goal_query]

    return jsonify(goals_response)


@goal_bp.route("/<goal_id>", methods=["GET"])
def get_one_goal(goal_id):
    goal = validate_model(Goal, goal_id)

    return jsonify({"goal": goal.to_dict()})


@goal_bp.route("/<goal_id>", methods=["PUT"])
def update_goal(goal_id):
    goal = validate_model(Goal, goal_id)

    request_body = request.get_json()
    goal.update_from_dict(request_body)

    db.session.commit()

    return make_response(jsonify({"goal": goal.to_dict()}), 200)


@goal_bp.route("/<goal_id>", methods=["DELETE"])
def delete_goal(goal_id):
    goal = validate_model(Goal, goal_id)

    db.session.delete(goal)
    db.session.commit()

    return make_response(jsonify({"details": f"Goal {goal.goal_id} \"{goal.title}\" successfully deleted"}))


@goal_bp.route("/<goal_id>/tasks", methods=["POST"])
def add_tasks_to_goal(goal_id):
    goal = validate_model(Goal, goal_id)

    request_body = request.get_json()
    task_ids_list = request_body["task_ids"]

    for task_id in task_ids_list:
        task = validate_model(Task, task_id)
        task.goal_id = goal.goal_id

        db.session.commit()
    
    goal_ids = [task.task_id for task in goal.tasks]

    return make_response(jsonify({"id": goal.goal_id, "task_ids": goal_ids}), 200)


@goal_bp.route("/<goal_id>/tasks", methods=["GET"])
def get_tasks_from_goal(goal_id):
    goal = validate_model(Goal, goal_id)

    tasks_response = [task.to_dict() for task in goal.tasks]

    return make_response(jsonify({"id": goal.goal_id, "title": goal.title, "tasks": tasks_response}))

