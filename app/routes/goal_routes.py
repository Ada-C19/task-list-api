from .helper_functions import create_instance, get_all_instances, get_one_instance, get_one_instance, delete_instance, update_instance, get_model_by_id  #get_instances_for_instance, add_instances_to_instance,
from app.models.goal import Goal
from app.models.task import Task
from flask import Blueprint, make_response, request
from app import db

goals_bp = Blueprint('goals', __name__, url_prefix='/goals')

@goals_bp.route("", methods=['POST'])
def create_goal():
    return create_instance(Goal)


@goals_bp.route("", methods=['GET'])
def get_goals():
    return get_all_instances(Goal)


@goals_bp.route("/<goal_id>", methods=['GET'])
def get_one_goal(goal_id):
    return get_one_instance(Goal, goal_id)


@goals_bp.route("/<goal_id>", methods=['PUT'])
def update_goal(goal_id):
    return update_instance(Goal, goal_id)


@goals_bp.route("/<goal_id>", methods=['DELETE'])
def delete_goal(goal_id):
    return delete_instance(Goal, goal_id)


# @goals_bp.route("/<goal_id>/tasks", methods=["GET"])
# def get_tasks_for_goal(goal_id):
#     return get_instances_for_instance(Goal, goal_id)


# @goals_bp.route("/<goal_id>/tasks", methods=["POST"])
# def add_tasks_to_goal(goal_id):
#     return add_instances_to_instance(Goal, goal_id)

@goals_bp.route("/<goal_id>/tasks", methods=["POST"])
def add_tasks_to_goal(goal_id):
    goal = get_model_by_id(Goal, goal_id)
    request_body = request.get_json()
    task_ids = request_body["task_ids"]

    for task in goal.tasks:
        task.goal_id = None

    for task_id in task_ids:
        task = get_model_by_id(Task, task_id)
        task.goal_id = goal.goal_id
    
    goal.title = request.args.get("title", goal.title)

    db.session.commit()

    return make_response({"id": goal.goal_id, "task_ids": task_ids}, 200)

@goals_bp.route("/<goal_id>/tasks", methods=["GET"])
def get_tasks_for_goal(goal_id):
    goal = get_model_by_id(Goal, goal_id)
    return make_response(goal.to_json(tasks=True), 200)