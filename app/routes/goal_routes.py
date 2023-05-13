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

    return make_response(jsonify(message), 200)

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

@goals_bp.route("/<goal_id>/tasks", methods=["POST"])
def assign_tasks_to_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    request_body = request.get_json()
    if not request_body:
        return jsonify({'error': 'Invalid request body'}), 400

    task_ids = request_body.get('task_ids', [])
    for task_id in task_ids:
        task = validate_model(Task, task_id)
        task.goal_id = goal.goal_id
        db.session.commit()

    return jsonify({'id': goal.goal_id, 'task_ids': task_ids}), 200

@goals_bp.route("/<goal_id>/tasks", methods=["GET"])
def get_task_of_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    goal = Goal.query.get(goal_id)
    task_data = []
    for task in goal.tasks:
        task_data.append({
            "id": task.task_id,
            "goal_id": goal.goal_id,
            "title": task.title,
            "description": task.description,
            "is_complete": task.is_complete
        })
    response = {
        "id": goal.goal_id,
        "title": goal.title,
        "tasks": task_data
    }
    return jsonify(response), 200


