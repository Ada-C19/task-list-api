from flask import Blueprint, jsonify, abort, make_response, request
from app.models.goal import Goal
from app import db


goals_bp = Blueprint("goals", __name__, url_prefix="/goals")


# Helper function
def validate_goal(goal_id):
    try:
        goal_id = int(goal_id)
    except:
        abort(make_response({"details": "Invalid data"}, 400))

    goal = Goal.query.get(goal_id)

    return goal if goal else abort(make_response({'msg': f"No goal with id {goal_id}"}, 404))