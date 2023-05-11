from app import db
from flask import Blueprint,jsonify, request, make_response, abort
from app.models.goal import Goal
from app.models.task import Task
from app.helper import validate_model

goals_bp = Blueprint("goals", __name__, url_prefix="/goals")

@goals_bp.route("", methods=["POST"])
def create_goal():

    request_body = request.get_json()
    try: 
        new_goal = Goal.from_dict(request_body)

        db.session.add(new_goal)
        db.session.commit()

        return make_response(jsonify({"goal": new_goal.to_dict()}), 201)

    except KeyError as error:
        abort(make_response(jsonify({"details": "Invalid data"}), 400))

@goals_bp.route("", methods=["GET"])
def get_all_goals():
    goals = Goal.query.all()

    goals_response = [goal.to_dict() for goal in goals]

    return jsonify(goals_response)

@goals_bp.route("/<goal_id>", methods=["GET"])
def get_one_goal(goal_id):
    goal = validate_model(Goal, goal_id)

    return jsonify({"goal":goal.to_dict()})

@goals_bp.route("/<goal_id>", methods=["PUT"])
def update_goal(goal_id):
    goal = validate_model(Goal, goal_id)

    request_body = request.get_json()

    goal.title = request_body["title"]

    db.session.commit()

    return jsonify({"goal":goal.to_dict()})

@goals_bp.route("/<goal_id>", methods=["DELETE"])
def delete_goal(goal_id):
    goal = validate_model(Goal, goal_id)

    db.session.delete(goal)
    db.session.commit()

    return jsonify({"details": f"Goal {goal_id} \"{goal.title}\" successfully deleted"})

@goals_bp.route("/<goal_id>/tasks", methods=["POST"])
def create_task_with_goal(goal_id):
    goal = validate_model(Goal, goal_id)

    request_body = request.get_json()

    task_ids = request_body.get("task_ids")

    new_task_ids = []
    for task_id in task_ids:
        task = validate_model(Task, task_id)
        task.goal=goal
        new_task_ids.append(task_id)
    
    db.session.commit()

    return make_response(jsonify({
        "id": goal.goal_id, 
        "task_ids": new_task_ids
        }), 200)


@goals_bp.route("/<goal_id>/tasks", methods=["GET"])
def get_tasks_with_goal(goal_id):
    goal = validate_model(Goal, goal_id)

    task_response = []
    for tasks in goal.tasks:
        task_response.append(tasks.to_dict())

        if task_response:
            for task in task_response:
                task["goal_id"] = goal.goal_id


    return make_response(jsonify({
    "id": goal.goal_id, 
    "title": goal.title,
    "tasks": task_response }), 200)

