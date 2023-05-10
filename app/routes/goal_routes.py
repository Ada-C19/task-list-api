from flask import abort, Blueprint, jsonify, make_response, request
from app import db
from app.models.task import Task
from app.models.goal import Goal
from app.routes.task_routes import verify_item
from datetime import datetime
import requests

goal_bp = Blueprint("goal", __name__, url_prefix="/goals")

@goal_bp.route("", methods=["POST"])
def add_goal():
    request_body = request.get_json()

    new_goal = Goal.from_dict(request_body)

    db.session.add(new_goal)
    db.session.commit()

    response_dict = message_for_only_one_goal(new_goal)

    return make_response(response_dict, 201)

@goal_bp.route("", methods=["GET"])
def get_goals():
    response_list = []
    all_goals = Goal.query.all()

    for goal in all_goals:
        response_list.append(goal.to_dict())

    return jsonify(response_list), 200

@goal_bp.route("/<goal_id>", methods=["GET"])
def get_one_goal(goal_id):
    response_list = []
    goal = verify_item(Goal, goal_id)

    response_dict = message_for_only_one_goal(goal)

    return jsonify(response_dict), 200

def message_for_only_one_goal(goal):
    return {"goal": goal.to_dict()}