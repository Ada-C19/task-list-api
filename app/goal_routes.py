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


# Routes
@goals_bp.route("", methods=['POST'])
def create_goal():
    request_body = request.get_json()
    try:
        new_goal = Goal(title=request_body["title"])
    except KeyError:
        return {
            "details": "Invalid data"
            }, 400

    db.session.add(new_goal)
    db.session.commit()

    return {"goal": new_goal.to_dict()}, 201