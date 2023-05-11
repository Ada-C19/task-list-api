from flask import Blueprint, jsonify, abort, make_response, request
from app.models.goal import Goal
from app import db
from sqlalchemy import asc, desc
from .helper_functions import get_goal_instance, validate_goal_id, get_goal_by_id, update_goal_from_request
from datetime import timezone, datetime

goals_bp = Blueprint('goals', __name__, url_prefix='/goals')

@goals_bp.route("", methods=['POST'])
def create_goal():
    new_goal = get_goal_instance(request)

    db.session.add(new_goal)
    db.session.commit()

    goal = new_goal.to_json()

    return make_response(jsonify(goal=goal)), 201

@goals_bp.route("", methods=['GET'])
def get_goals():
    sort_order = request.args.get("sort", None)

    goals = Goal.query

    title_query = request.args.get("title")
    if title_query:
        goals = goals.filter_by(title=title_query)

    if sort_order == "asc":
        goals = goals.order_by(asc(Goal.title))
    elif sort_order == "desc":
        goals = goals.order_by(desc(Goal.title))

    goals = goals.all()

    goal_list = [goal.to_json() for goal in goals]

    return jsonify(goal_list), 200

@goals_bp.route("/<goal_id>", methods=['GET'])
def get_one_goal(goal_id):
    goal = get_goal_by_id(goal_id)
    return make_response(jsonify({"goal": goal.to_json()})), 200

@goals_bp.route("/<goal_id>", methods=['PUT'])
def update_goal(goal_id):
    goal = get_goal_by_id(goal_id)
    updated_goal = update_goal_from_request(goal, request)

    db.session.commit()

    goal = updated_goal.to_json()

    return make_response(jsonify(goal=goal)), 200

@goals_bp.route("/<goal_id>", methods=['DELETE'])
def delete_goal(goal_id):
    goal = get_goal_by_id(goal_id)

    db.session.delete(goal)
    db.session.commit()

    message = f'Goal {goal_id} "{goal.title}" successfully deleted'

    return make_response({"details": message}), 200

@goals_bp.route("/<goal_id>/mark_complete", methods=['PATCH'])
def mark_goal_completed(goal_id):
    goal = get_goal_by_id(goal_id)

    goal.completed_at = datetime.now(timezone.utc)

    db.session.commit()

    goal = goal.to_json()
    goal["is_complete"] = True

    return make_response(jsonify(goal=goal)), 200

@goals_bp.route("/<goal_id>/mark_incomplete", methods=['PATCH'])
def mark_goal_incomplete(goal_id):
    goal = get_goal_by_id(goal_id)

    goal.completed_at = None

    db.session.commit()

    goal = goal.to_json()
    goal["is_complete"] = False

    return make_response(jsonify(goal=goal)), 200
