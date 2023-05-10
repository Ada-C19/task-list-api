from app import db
from app.models.goal import Goal
from app.models.task import Task
from app.helper_functions import validate_model, create_model, assign_tasks, task_dicts, abort
from flask import Blueprint, jsonify, make_response, request

goal_bp = Blueprint("goal_bp", __name__, url_prefix="/goals")

@goal_bp.route("", methods=["POST"])
def creat_goal():
    request_body = request.get_json()
    new_goal = create_model(request_body, Goal)

    return make_response(jsonify({
        "goal": {
            "id" : new_goal.goal_id,
            "title" : new_goal.title
        }
    }), 201)

@goal_bp.route("", methods=["GET"])
def read_all_goal():
    title_query = request.args.get("title")

    if title_query:
        goals = Goal.query.filter_by(title=title_query)
    else:
        goals = Goal.query.all()

    goals_response = []
    for goal in goals:
        goals_response.append(goal.to_dict())
    return jsonify(goals_response)

@goal_bp.route("/<goal_id>", methods=["GET"])
def read_one_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    return jsonify({"goal": goal.to_dict()}), 200

@goal_bp.route("/<goal_id>", methods=["PUT"])
def update_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    request_body = request.get_json()

    if "title" not in request_body:
        abort(make_response(jsonify({"details": "Invalid data"}), 400))

    goal.title = request_body["title"]

    db.session.commit()

    return make_response(jsonify({
        "goal": {
            "id" : goal.goal_id,
            "title" : goal.title
        }
    }), 200)

@goal_bp.route("/<goal_id>", methods=["DELETE"])
def delete_goal(goal_id):
    goal = validate_model(Goal, goal_id)

    db.session.delete(goal)
    db.session.commit()

    return make_response(jsonify({"details": f"Goal 1 \"{goal.title}\" successfully deleted"})), 200

@goal_bp.route("/<goal_id>/tasks", methods=["POST"])
def create_task(goal_id):
    request_body = request.get_json()
    goal = validate_model(Goal, goal_id)
    task_ids= request_body["task_ids"]

    new_task_ids = assign_tasks(goal, task_ids)
    
    return jsonify({"id": goal.goal_id, 
                    "task_ids": new_task_ids}), 200

@goal_bp.route("/<goal_id>/tasks", methods=["GET"])
def read_task_by_goal(goal_id):
    goal = validate_model(Goal, goal_id)

    task_dicts_list = task_dicts(goal_id)

    return make_response(jsonify({
        "id": goal.goal_id,
        "title": goal.title,
        "tasks": task_dicts_list
    }))