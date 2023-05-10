from flask import Blueprint
from app import db
from app.models.goal import Goal
from app.models.task import Task
from flask import Blueprint, jsonify, make_response, request, abort
from app.task_routes import validate_model


goals_bp = Blueprint("goals", __name__, url_prefix="/goals")


@goals_bp.route("", methods=["POST"])
def create_goal():
    request_body = request.get_json()
    if not request_body.get("title"):
        abort(make_response({
            "details": "Invalid data"
        }, 400))

    new_goal = Goal.from_dict(request_body)

    db.session.add(new_goal)
    db.session.commit()

    return {
        "goal": new_goal.to_dict()
    }, 201


@goals_bp.route("", methods=["GET"])
def get_goals():
    goals_response = []
    goals = Goal.query.all()

    for goal in goals:
        goals_response.append(goal.to_dict())
    return jsonify(goals_response)


@goals_bp.route("/<goal_id>", methods=["GET"])
def get_goal_by_id(goal_id):
    goal = validate_model(Goal, goal_id)
    return {
        "goal": goal.to_dict()
    }, 200


@goals_bp.route("/<goal_id>", methods=["PUT"])
def update_goal_by_id(goal_id):
    goal = validate_model(Goal, goal_id)

    request_body = request.get_json()
    goal.title = request_body["title"]

    db.session.commit()

    return {
        "goal": goal.to_dict()
    }


@goals_bp.route("/<goal_id>", methods=["DELETE"])
def delete_goal(goal_id):
    goal = validate_model(Goal, goal_id)

    db.session.delete(goal)
    db.session.commit()

    return {
        "details": f'Goal {goal_id} "{goal.title}" successfully deleted'
    }



@goals_bp.route("/<goal_id>/tasks", methods=["POST"])
def post_tasks_ids_with_goals(goal_id):
    goal = validate_model(Goal, goal_id)
    request_body = request.get_json()
    task_ids = request_body.get("task_ids")
    added_ids = []
    for id in task_ids:
        task_desde_db = Task.query.get(id)
        task_desde_db.goal = goal
        added_ids.append(task_desde_db.task_id)

    db.session.commit()
    
    return jsonify({
        "id": goal.goal_id,
        "task_ids": added_ids
    })
    


@goals_bp.route("/<goal_id>/tasks", methods=["GET"])
def get_task_from_goal(goal_id):
    response = []
    goal = validate_model(Goal, goal_id)
    task_by_goal = Task.query.get(goal_id)

    if task_by_goal is None:
        return jsonify({
            "id": goal.goal_id,
            "title": goal.title,
            "tasks": response
        })
    else:
        task_by_goal.goal = goal
        for task in goal.tasks:
            response.append(
                task.to_dict()
            )

    return jsonify({
        "id": goal.goal_id,
        "title": goal.title,
        "tasks": response
    })



