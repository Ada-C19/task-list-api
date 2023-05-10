from app import db
from app.models.task import Task, validate_item
from app.models.goal import Goal
from flask import Blueprint, jsonify, request

goals_bp = Blueprint("goal", __name__, url_prefix="/goals")

@goals_bp.route("", methods=["POST"])
def add_goal():
    """Create and add goal to database."""
    request_body = request.get_json()

    if "title" not in request_body:
        return {"details": "Invalid data"}, 400

    new_goal = Goal.from_dict(request_body)

    db.session.add(new_goal)
    db.session.commit()

    return {"goal": new_goal.to_dict()}, 201


@goals_bp.route("", methods=["GET"])
def get_all_goals():
    """Get all goals."""
    all_goals = Goal.query.all()

    response = [goal.to_dict() for goal in all_goals]

    return jsonify(response), 200


@goals_bp.route("/<goal_id>", methods=["GET"])
def get_one_goal(goal_id):
    """Get one goal by id."""
    return {"goal": validate_item(Goal, goal_id).to_dict()}, 200


@goals_bp.route("/<goal_id>", methods=["PUT"])
def update_goal(goal_id):
    """Updates goal specifed by id."""
    goal = validate_item(Goal, goal_id)

    request_body = request.get_json()
    goal.title = request_body["title"]

    db.session.commit()

    return {"goal": goal.to_dict()}, 200


@goals_bp.route("/<goal_id>", methods=["DELETE"])
def delete_goal(goal_id):
    """Delete goal specifed by id."""
    goal = validate_item(Goal, goal_id)

    db.session.delete(goal)
    db.session.commit()

    return {"details": f'Goal {goal.goal_id} "{goal.title}" successfully deleted'}, 200


@goals_bp.route("/<goal_id>/tasks", methods=["GET"])
def get_all_tasks_of_goal(goal_id):
    """Get all tasks of a goal via goal id."""
    goal = validate_item(Goal, goal_id)

    response = [task.to_dict() for task in goal.tasks]

    return jsonify({
        "id": goal.goal_id,
        "title": goal.title,
        "tasks": response
    }), 200


@goals_bp.route("/<goal_id>/tasks", methods=["POST"])
def associate_tasks_to_goal(goal_id):
    """Associate goal to tasks."""
    goal = validate_item(Goal, goal_id)

    request_body = request.get_json()

    task_ids = request_body.get("task_ids")
    for task_id in task_ids:
        task = validate_item(Task, task_id)
        task.goal = goal

    db.session.commit()

    return {
        "id": goal.goal_id,
        "task_ids": task_ids
    }, 200