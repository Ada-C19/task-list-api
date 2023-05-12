from flask import Blueprint, request, abort, make_response, jsonify
from app.models.goal import Goal
from app.models.task import Task
from app import db
from app.helper_functions import validate_model, create_model, sort_items, update_model


goals_bp = Blueprint("goals_bp", __name__, url_prefix="/goals")

# Create
@goals_bp.route("", methods=["POST"])
def post_goal():
    request_body = request.get_json()
    new_goal = create_model(Goal, request_body)
    db.session.add(new_goal)
    db.session.commit()
    return make_response({"goal": new_goal.to_dict()}, 201)


@goals_bp.route("/<goal_id>/tasks", methods=["POST"])
def post_tasks_to_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    task_ids = request.json.get("task_ids")

    tasks = Task.query.filter(Task.id.in_(task_ids)).all()
    goal.tasks = [task for task in tasks]
    db.session.commit()

    return make_response({
                            "id": int(goal_id),
                            "task_ids": task_ids
                        })


# Read
@goals_bp.route("", methods=["GET"])
def get_all_goals():
    sort_query = request.args.get("sort")
    goals = sort_items(Goal, sort_query)
    goals_response = [goal.to_dict() for goal in goals]
    return jsonify(goals_response)


@goals_bp.route("/<goal_id>", methods=["GET"])
def get_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    return make_response({"goal": goal.to_dict()})


@goals_bp.route("<goal_id>/tasks", methods=["GET"])
def get_tasks_for_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    task_list = [task.to_dict() for task in goal.tasks]
    return make_response({
                            "id": goal.id,
                            "title": goal.title,
                            "tasks": task_list
                        })


# Update
@goals_bp.route("<goal_id>", methods=["PUT"])
def update_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    request_body = request.get_json()
    update_model(goal, request_body)
    db.session.commit()
    return make_response({"goal": goal.to_dict()})


# Delete
@goals_bp.route("/<goal_id>", methods=["DELETE"])
def delete_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    db.session.delete(goal)
    db.session.commit()
    return make_response({"details": f"Goal {goal.id} \"{goal.title}\" successfully deleted"})
