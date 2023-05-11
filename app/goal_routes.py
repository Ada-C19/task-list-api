from app import db
from app.models.goal import Goal
from app.models.task import Task
from flask import Blueprint, jsonify, make_response, request, abort
from app.helper_functions import validate_model

goal_bp = Blueprint("goal", __name__, url_prefix="/goals")
    
@goal_bp.route("", methods=["POST"])
def create_goal():
    request_body = request.get_json()
    try:
        new_goal = Goal.from_dict(request_body)
        
        db.session.add(new_goal)
        db.session.commit()

        message  = {
            "goal": new_goal.to_dict()
        }
        return make_response(message, 201)
    except KeyError as e:
        abort(make_response({"details": "Invalid data"}, 400))

@goal_bp.route("", methods=["GET"])
def get_goals():    
    goals = Goal.query.all()
    goals_response = [goal.to_dict() for goal in goals]
    return jsonify(goals_response) 

@goal_bp.route("/<goal_id>", methods=["GET"])
def get_one_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    message  = {
        "goal": goal.to_dict()
        }
    return make_response(message, 200)

@goal_bp.route("/<goal_id>", methods=["PUT"])
def update_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    request_body = request.get_json()

    goal.title = request_body["title"]

    db.session.commit()

    message  = {
        "goal": goal.to_dict()
        }
    return make_response(message, 200)

@goal_bp.route("/<goal_id>", methods=["DELETE"])
def delete_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    
    db.session.delete(goal)
    db.session.commit()

    message  = {
            "details": f"Goal {goal.goal_id} \"{goal.title}\" successfully deleted"
        }

    return make_response(message, 200)

@goal_bp.route("/<goal_id>/tasks", methods=["POST"])
def create_tasks_for_goal_assignment(goal_id):
    request_body = request.get_json()
    goal = validate_model(Goal, goal_id)
    task_list = request_body.get("task_ids")

    tasks = []
    for task_id in task_list:
        task = validate_model(Task, task_id)
        task.goal = goal 
        tasks.append(task_id)

    db.session.commit()

    message = {
        "id": goal.goal_id,
        "task_ids": tasks
        }

    return make_response(message, 200)

@goal_bp.route("/<goal_id>/tasks", methods=["GET"])
def get_tasks_of_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    task_list = []
    for task_obj in goal.tasks:
        task = validate_model(Task, task_obj.task_id)
        task_list.append(task.to_dict())

    message = {
        "id": goal.goal_id,
        "title": goal.title,
        "tasks": task_list
    }

    return make_response(message, 200)