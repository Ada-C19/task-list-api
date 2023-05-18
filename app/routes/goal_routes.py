from flask import Blueprint, make_response, jsonify, request, abort
from app.models.task import Task
from app.models.goal import Goal
from app import db
from .route_helpers import validate_model

bp = Blueprint("goals", __name__, url_prefix="/goals")


@bp.route("", methods=["GET"])
def get_all_goals():
    goals = Goal.query.all()
    goals_list = [goal.to_dict() for goal in goals]

    return jsonify(goals_list), 200


@bp.route("", methods=["POST"])
def create_a_goal():
    request_body = request.get_json()
    if "title" not in request_body or not request_body["title"]:
        abort(make_response({"details": "Invalid data"}, 400))
    new_goal = Goal(
        title=request_body["title"]
    )
    db.session.add(new_goal)
    db.session.commit()

    return {"goal": new_goal.to_dict()}, 201


@bp.route("/<id>", methods=["GET"])
def get_one_goal(id):
    goal = validate_model(Goal, id)

    return {"goal": goal.to_dict()}, 200


@bp.route("/<id>", methods=["PUT"])
def update_a_goal(id):
    goal = validate_model(Goal, id)
    request_body = request.get_json()
    goal.title = request_body["title"]

    db.session.commit()

    return {"goal": goal.to_dict()}, 200


@bp.route("/<id>", methods=["DELETE"])
def delete_a_goal(id):
    goal = validate_model(Goal, id)
    db.session.delete(goal)
    db.session.commit()

    return make_response({'details': f'Goal {goal.id} "{goal.title}" successfully deleted'}), 200


@bp.route("/<id>/tasks", methods=["GET"])
def get_all_tasks_for_one_goal(id):
    goal = validate_model(Goal, id)
    tasks_list = [(dict(id=task.id, title=task.title, description=task.description,
                        is_complete=False if task.completed_at is None else True, goal_id=goal.id)) for task in goal.tasks]

    return {"id": goal.id, "title": goal.title, "tasks": tasks_list}, 200


@bp.route("/<id>/tasks", methods=["POST"])
def post_task_ids_to_goal(id):
    goal = validate_model(Goal, id)
    request_body = request.get_json()
    if "task_ids" not in request_body:
        abort(make_response({"details": "Invalid data"}, 400))

    task_ids = request_body["task_ids"]
    tasks_list = [Task.query.get(task_id) for task_id in task_ids]
    goal.tasks = tasks_list

    db.session.commit()

    return {"id": goal.id, "task_ids": task_ids}, 200
