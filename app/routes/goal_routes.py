from flask import Blueprint, jsonify, abort, make_response, request
from app.models.goal import Goal
from app.models.task import Task
from app import db
from app.routes.task_routes import validate_model

goal_bp = Blueprint("goals", __name__, url_prefix="/goals")

@goal_bp.route("", methods=["POST"])
def create_goal():
    request_body = request.get_json()
    if request_body == {}:
        return jsonify({"details": "Invalid data"}), 400
    new_goal = Goal.from_dict(request_body)

    db.session.add(new_goal)
    db.session.commit()

    return jsonify({"goal": new_goal.to_dict()}), 201

@goal_bp.route("", methods=['GET'])
def get_goals():
    goals = Goal.query.all()

    goals_response = []
    for goal in goals:
        goals_response.append(goal.to_dict())
    
    return jsonify(goals_response), 200

@goal_bp.route('/<goal_id>', methods=["GET"])
def get_goal_by_id(goal_id):
    goal = validate_model(Goal, goal_id)
    if goal.tasks:
        return jsonify({"goal": goal.to_dict()})
    
    return jsonify({"goal": goal.to_dict()})

@goal_bp.route('/<goal_id>', methods=['PUT'])
def update_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    request_body = request.get_json()
    goal.title = request_body['title']

    db.session.commit()

    return jsonify({"goal": goal.to_dict()}), 200

@goal_bp.route('/<goal_id>', methods=['DELETE'])
def delete_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    response_body = {"details": f'Goal {goal_id} "{goal.title}" successfully deleted'}
    db.session.delete(goal)
    db.session.commit()

    return jsonify(response_body), 200

@goal_bp.route("/<goal_id>/tasks", methods=['POST'])
def add_tasks_to_goals(goal_id):
    request_body = request.get_json()
    goal = validate_model(Goal, goal_id)
    for task_id in request_body['task_ids']:
        goal.tasks.append(validate_model(Task, task_id))

    db.session.commit()


    return jsonify({"id": goal.goal_id, "task_ids": request_body['task_ids']}), 200

@goal_bp.route("/<goal_id>/tasks", methods=['GET'])
def get_tasks_of_one_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    return jsonify(goal.to_dict_with_tasks()), 200

# @goal_bp.route("/<goal_id>/tasks", methods=['GET'])
# def 