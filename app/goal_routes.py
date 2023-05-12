from app import db
from app.models.goal import Goal
from app.models.task import Task
from flask import Blueprint, jsonify, make_response, abort, request
import requests
from app.task_routes import validate_model

goals_bp = Blueprint("goals'", __name__, url_prefix = "/goals")

@goals_bp.route("", methods=["POST"])
def create_goal():
    request_body = request.get_json()

    if not request_body.get("title"):
        abort(make_response(
                {
                    "details": "Invalid data"
                }, 400
            ))

    new_goal = Goal(
        title = request_body["title"],
    )

    db.session.add(new_goal)
    db.session.commit()

    return make_response({"goal": new_goal.to_dict()}, 201)

@goals_bp.route("/<goal_id>/tasks", methods=["POST"])
def add_task_to_goal(goal_id):
    goal = validate_model(Goal, goal_id)

    request_body = request.get_json()

    for task_id in request_body["task_ids"]:
        task = validate_model(Task, task_id)
        task.goal_id = goal.goal_id
    
    db.session.commit()

    return make_response(
        {
            "id": goal.goal_id,
            "task_ids": request_body["task_ids"]
        }
    ), 200
        

@goals_bp.route("", methods=["GET"])
def read_goals():
    goals = Goal.query.all()

    goals_response = []
    for goal in goals:
        goals_response.append(goal.to_dict())

    return jsonify(goals_response), 200

@goals_bp.route("/<goal_id>", methods=["GET"])
def read_one_saved_goal(goal_id):
    goal = validate_model(Goal, goal_id)

    return {
        "goal": goal.to_dict()
    }

@goals_bp.route("/<goal_id>/tasks", methods=["GET"])
def get_tasks_of_one_goal(goal_id):
    goal = validate_model(Goal, goal_id)

    tasks_response = []
    for task in goal.tasks:
        tasks_response.append(task.to_dict())
    
    return jsonify({
            "id": goal.goal_id,
            "title": goal.title,
            "tasks": tasks_response
        }), 200

@goals_bp.route("/<goal_id>", methods=["PUT"])
def update_goal(goal_id):
    goal = validate_model(Goal, goal_id)

    request_body = request.get_json()

    goal.title = request_body["title"]

    db.session.commit()

    return make_response({"goal": goal.to_dict()}), 200


@goals_bp.route("/<goal_id>", methods=["DELETE"])
def delete_goal(goal_id):
    goal = validate_model(Goal, goal_id)

    db.session.delete(goal)
    db.session.commit()

    return make_response(
        {
            "details": f"Goal {goal.goal_id} \"{goal.title}\" successfully deleted"
        }, 200
    )