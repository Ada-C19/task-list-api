from .helper_functions import create_instance, get_all_instances, get_one_instance, get_one_instance, delete_instance, update_instance,  add_tasks_to_class
from app.models.goal import Goal
from flask import Blueprint


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


@goals_bp.route("/<goal_id>/tasks", methods=["GET"])
def get_tasks_for_goal(goal_id):
    return get_all_instances(Goal, goal_id)

@goals_bp.route("/<goal_id>/tasks", methods=["POST"])
def add_tasks_to_goal(goal_id):
    return add_tasks_to_class(Goal, goal_id)

