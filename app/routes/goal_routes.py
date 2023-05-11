from flask import Blueprint, jsonify, abort, make_response, request
from app import db
from app.models.goal import Goal
from .routes_helpers import validate_model

goal_bp = Blueprint("goals", __name__, url_prefix="/goals")


# CREATE ENDPOINT
@goal_bp.route("", methods=["POST"])
def create_goal():
    req_body = request.get_json()

    if "title" in req_body:
        new_goal = Goal(title=req_body["title"])
    else:
        abort(make_response({"details": "Invalid data"}, 400))

    db.session.add(new_goal)
    db.session.commit()

    return make_response(jsonify({"goal": new_goal.to_dict()}), 201)


# GET ALL ENDPOINT
@goal_bp.route("", methods=["GET"])
def handle_goals():
    goal_query = Goal.query.all()

    goals_response = [goal.to_dict() for goal in goal_query]

    return jsonify(goals_response)


# GET ONE ENDPOINT
@goal_bp.route("/<id>")
def handle_goal(id):
    goal = validate_model(Goal, id)

    return make_response(jsonify({"goal": goal.to_dict()}), 200)


# UPDATE ONE ENDPOINT
@goal_bp.route("/<id>", methods=["PUT"])
def update_goal(id):
    goal = validate_model(Goal, id)

    req_body = request.get_json()

    goal.title = req_body["title"]

    db.session.commit()

    return make_response(jsonify({"goal": goal.to_dict()}), 200)


# DELETE ONE ENDPOINT
@goal_bp.route("/<id>", methods=["DELETE"])
def delete_task(id):
    goal = validate_model(Goal, id)

    db.session.delete(goal)
    db.session.commit()

    return make_response({"details": f"Goal {goal.goal_id} \"{goal.title}\" successfully deleted"}, 200)
