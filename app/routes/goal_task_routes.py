from flask import Blueprint, jsonify, request
from app import db
from app.models.goal import Goal
from app.models.task import Task


goal_task_bp = Blueprint("goal_task", __name__, url_prefix="/goals")


@goal_task_bp.route("/<goal_id>/tasks", methods=["POST"])
def post_task_ids_to_goal(goal_id):
    request_body = request.get_json()
    goal = Goal.query.get_or_404(goal_id)

    for id in request_body["task_ids"]:
        task = Task.query.get_or_404(id)
        task.goal = goal

    db.session.commit()

    return {"id": int(goal_id), "task_ids": request_body["task_ids"]}, 200


@goal_task_bp.route("/<goal_id>/tasks", methods=["GET"])
def get_tasks_for_goal(goal_id):
    request_body = request.get_json()
    goal = Goal.query.get_or_404(goal_id)

    response = goal.to_dict()
    response["tasks"] = []
    for task in goal.tasks:
        response["tasks"].append(task.to_dict())

    db.session.commit()

    return jsonify(response), 200
