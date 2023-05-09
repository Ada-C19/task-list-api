from flask import Blueprint, request, jsonify, make_response, abort
from app.models.goal import Goal
from app.models.task import Task
from .routes_helpers import validate_model
from app import db

goals_bp = Blueprint("goals", __name__, url_prefix="/goals")

# CREATE GOAL ENDPOINT
@goals_bp.route("", methods=["POST"])
def create_goal():
    request_body = request.get_json()

    if not request_body.get("title"):
        abort(make_response({"details": "Invalid data"}, 400))
    else:
        new_goal = Goal(title=request_body["title"])

    db.session.add(new_goal)
    db.session.commit()

    return make_response({"goal": new_goal.to_dict()}, 201)

# CREATE TASK TO GOAL ENDPOINT
@goals_bp.route("/<goal_id>/tasks", methods=["POST"])
def create_task(goal_id):
    goal = validate_model(Goal,goal_id)

    request_body = request.get_json()

    for task_id in request_body["task_ids"]:
        task = Task.query.get(task_id)
        task.goal_id = goal.goal_id

    db.session.commit()

    return make_response({"id": goal.goal_id,
                          "task_ids": request_body["task_ids"]})

# GET GOALS ENDPOINT
@goals_bp.route("", methods=["GET"])
def read_goals():
    goals = Goal.query.all()

    goals_response = [goal.to_dict() for goal in goals]

    return jsonify(goals_response)

# GET ONE GOAL ENDPOINT
@goals_bp.route("/<goal_id>", methods=["GET"])
def read_one_goal(goal_id):
    goal = validate_model(Goal, goal_id)

    return {"goal": goal.to_dict()}

# GET TASK BY GOAL ENDPOINT
@goals_bp.route("/<goal_id>/tasks", methods=["GET"])
def read_task_by_goal(goal_id):
    goal = validate_model(Goal, goal_id)

    tasks = Task.query.filter(Task.goal_id == goal.goal_id)

    tasks_body = [task_dict(task) for task in tasks]

    return make_response(jsonify({
        "id": goal.goal_id,
        "title": goal.title,
        "tasks": tasks_body
    }))

# UPDATE GOAL ENDPOINT
@goals_bp.route("/<goal_id>", methods=["PUT"])
def update_goal(goal_id):
    request_body = request.get_json()

    goal = validate_model(Goal, goal_id)

    goal.title = request_body["title"]

    db.session.commit()

    return {"goal": goal.to_dict()}

# DELETE GOAL ENDPOINT
@goals_bp.route("/<goal_id>", methods=["DELETE"])
def delete_goal(goal_id):
    goal = validate_model(Goal, goal_id)

    db.session.delete(goal)
    db.session.commit()

    return make_response({"details": f"Goal {goal.goal_id} \"{goal.title}\" successfully deleted"})


# HELPER FUNCTIONS
def task_dict(task):
    return {
        "id": task.task_id,
        "goal_id": task.goal_id,
        "title": task.title,
        "description": task.description,
        "is_complete": False
    }