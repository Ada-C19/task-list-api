from flask import Blueprint, jsonify, make_response, request
from app import db
from app.helper import validate_model
from app.models.goal import Goal
from app.models.task import Task


goals_bp = Blueprint("goals", __name__, url_prefix="/goals")

@goals_bp.route("", methods = ["POST"])
def create_goals():
    request_body = request.get_json()
    try:
        new_goal = Goal.create_new_goal(request_body)
        db.session.add(new_goal)
        db.session.commit()

        message = new_goal.__str__()

        return make_response(jsonify(message), 201)
    except KeyError as e:
        message = "Invalid data"
        return make_response({"details": message}, 400)

@goals_bp.route("", methods = ["GET"])
def read_all_goals():
    goals = Goal.query.all()
    goal_response = [goal.goal_to_dict() for goal in goals]
    return jsonify(goal_response)

@goals_bp.route("/<goal_id>", methods=["GET"])
def read_one_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    message = goal.__str__()

    return make_response(jsonify(message), 201)

@goals_bp.route("/<goal_id>", methods=["PUT"])
def update_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    request_body = request.get_json()
    goal.update(request_body)

    db.session.commit()
    message = goal.__str__()
    return make_response(jsonify(message))

@goals_bp.route("/<goal_id>", methods=["DELETE"])
def delete_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    db.session.delete(goal)
    db.session.commit()

    message = {
        "details": f'Goal {goal_id} "{goal.title}" successfully deleted'
        }
    return make_response(jsonify(message), 200)

def add_task_to_goal(task_id, goal):
    goal.task_id = task_id
    db.session.commit()

@goals_bp.route("/<goal_id>/tasks", methods=["POST"])
def create_task(goal_id):
    goal = validate_model(Goal, goal_id)
    request_body = request.get_json()
    new_task = Task.create_new_task(request_body)

    new_task.goal_id = goal.goal_id
    db.session.add(new_task)
    db.session.commit()
    add_task_to_goal(new_task.task_id, goal)

    return make_response(jsonify(f"Task {new_task.title} successfully created"), 201)