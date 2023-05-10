from flask import Blueprint, jsonify, abort, make_response, request
from app import db
from app.models.goal import Goal
from app.models.task import Task
from .route_helpers import validate_model


goal_bp = Blueprint("goals", __name__, url_prefix="/goals")

@goal_bp.route("", methods=["GET"])
def get_goals():
    goals = Goal.query.all()
    goals_response = [goal.to_dict() for goal in goals]

    return make_response(jsonify(goals_response), 200)


@goal_bp.route("", methods=["POST"])
def create_goal():
    request_body = request.get_json()
    try:
        new_goal = Goal.from_dict(request_body)
    except KeyError:
        abort(make_response(jsonify({"details": "Invalid data"}), 400))

    db.session.add(new_goal)
    db.session.commit()

    return make_response(jsonify({"goal": new_goal.to_dict()}), 201)


@goal_bp.route("/<goal_id>", methods=["GET"])
def get_one_goal(goal_id):
    goal = validate_model(Goal, goal_id)

    return make_response(jsonify({"goal": goal.to_dict()}), 200)


@goal_bp.route("/<goal_id>", methods=["PUT"])
def update_one_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    request_body = request.get_json()

    goal.title = request_body["title"]

    db.session.commit()

    return make_response(jsonify({"goal": goal.to_dict()}), 200)


@goal_bp.route("/<goal_id>", methods=["DELETE"])
def delete_one_goal(goal_id):
    goal = validate_model(Goal, goal_id)

    db.session.delete(goal)
    db.session.commit()

    return make_response(jsonify({"details": f'Goal {goal.id} "{goal.title}" successfully deleted'}), 200)


@goal_bp.route("/<goal_id>/tasks", methods=["POST"])
def assign_tasks_to_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    request_body = request.get_json()
    
    try:
        task_ids = request_body['task_ids']
    except KeyError: # Catch requests without list of task ids
        abort(make_response(jsonify({"details": "Invalid data"}), 400))
    
    # Update each task to link it to this goal
    for id in task_ids:
        task = validate_model(Task, id)
        task.goal = goal

    goal_tasks = [task.id for task in goal.tasks] # Thought of making this into an object method, but decided against as it would only get used once

    db.session.commit()

    return make_response(jsonify({'id': goal.id, "task_ids": goal_tasks}), 200) 


@goal_bp.route("/<goal_id>/tasks", methods=["GET"])
def get_related_tasks(goal_id):
    goal = validate_model(Goal, goal_id)
    response_body = goal.to_dict()
    
    # Necessary conditional check to pass both Wave 5 and 6 tests
    if not goal.tasks:
        response_body["tasks"] = []

    return make_response(jsonify(response_body), 200)
