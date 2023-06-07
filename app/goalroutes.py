from flask import Blueprint, jsonify, make_response, request, abort
from app.models.goal import Goal
from app import db

goals_bp = Blueprint("goals", __name__, url_prefix="/goals")

@goals_bp.route("", methods=["POST"])
def create_goal():
    request_data = request.get_json()
    goal = Goal(title=request_data["title"])

    db.session.add(goal)
    db.session.commit()

    response_body = {"goal": goal.to_dict()}

    return make_response(jsonify(response_body), 201)



@goals_bp.route("", methods=["GET"])
def get_goals():
    goals = Goal.query.all()
    response_body = []

    for goal in goals:
       response_body.append(goal.to_dict())

    return make_response(jsonify(response_body), 200)


@goals_bp.route("/<goal_id>", methods=["GET"])
def get_goal(goal_id):
    goal = Goal.query.get(goal_id)

    if not goal:
        abort(make_response(jsonify({"message": f"Goal {goal_id} was not found."}), 404))

    response_body = {"goal": goal.to_dict()}

    return make_response(jsonify(response_body), 200)



@goals_bp.route("/<goal_id>", methods=["PUT"])
def update_goal(goal_id):
    goal = Goal.query.get(goal_id)

    if goal is None:
        abort(make_response(jsonify({"message": f"Goal {goal_id} was not found."}), 404))

    request_data = request.get_json()
    goal.title = request_data["title"]

    db.session.commit()

    response_body = {"goal": goal.to_dict()}

    return make_response(jsonify(response_body), 200)



@goals_bp.route("/<goal_id>", methods=["DELETE"])
def delete_goal(goal_id):
    goal = Goal.query.get(goal_id)

    if goal is None:
        abort(make_response(jsonify({"message": f"Goal {goal_id} was not found."}), 404))

    db.session.delete(goal)
    db.session.commit()

    response_body = {
        "details": f"Goal {goal_id} \"{goal.title}\" successfully deleted"
    }

    return make_response(jsonify(response_body), 200)


