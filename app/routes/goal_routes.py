from app import db
from app.models.goal import Goal
from app.models.task import Task
from flask import Blueprint, jsonify, abort, make_response, request
from app.helpers import validate_model

goals_bp = Blueprint("goals", __name__, url_prefix="/goals")

@goals_bp.route("", methods=["GET"])
def get_all_goals():
    goals = Goal.query.all()
    results = [goal.to_dict() for goal in goals]

    return jsonify(results)

@goals_bp.route("/<goal_id>", methods=["GET"])
def get_one_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    response = {"goal": goal.to_dict()}

    return jsonify(response)

@goals_bp.route("", methods=["POST"])
def create_goal():
    request_body = request.get_json()
    
    new_goal_is_valid = "title" in request_body
    if not new_goal_is_valid:
        abort(make_response(jsonify({"details":"Invalid data"}), 400))

    new_goal = Goal.from_dict(request_body)
    db.session.add(new_goal)
    db.session.commit()
    
    response = {"goal": new_goal.to_dict()}

    return make_response((jsonify(response)), 201)

@goals_bp.route("<goal_id>", methods=["DELETE"])
def delete_one_goal(goal_id):
    goal_to_delete = validate_model(Goal, goal_id)
    
    db.session.delete(goal_to_delete)
    db.session.commit()

    message = {"details":f"Goal {goal_id} \"{goal_to_delete.title}\" successfully deleted"}
    return make_response(message, 200)

@goals_bp.route("/<goal_id>", methods=["PUT"])
def update_one_goal(goal_id):    
    goal = validate_model(Goal, goal_id)
    updated_data = request.get_json()

    goal.title = updated_data["title"]

    db.session.commit()

    response = {"goal": goal.to_dict()}

    return make_response(response, 200)

@goals_bp.route("/<goal_id>/tasks", methods=["POST"])
def create_tasks_for_one_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    request_body = request.get_json()

    for task_id in request_body["task_ids"]:
        task = validate_model(Task, task_id)
        task.goal_id = goal.goal_id
    db.session.commit()

    task_id_list = [task.task_id for task in goal.tasks]

    response_body = {
        "id":goal.goal_id,
        "task_ids": task_id_list
    }
    return jsonify(response_body)

@goals_bp.route("/<goal_id>/tasks", methods=["GET"])
def get_all_tasks_of_one_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    # tasks_response = [task.to_dict() for task in goal.tasks]
    goal = goal.to_dict()
    return jsonify(goal)