from flask import Blueprint, jsonify, abort, make_response, request
from app.models.task import Task
from app.models.goal import Goal
from app import db
from app.helpers import validate_model
from datetime import datetime


goals_bp = Blueprint("goals", __name__, url_prefix="/goals")

#ROUTE 1
@goals_bp.route("", methods=["POST"])
def create_new_goal():
    request_body = request.get_json()
    try:
        new_goal = Goal.from_dict(request_body)

        db.session.add(new_goal)
        db.session.commit()

        return make_response({"goal":new_goal.to_dict()}, 201)
    except KeyError:
        abort(make_response({"details": "Invalid data"}, 400))

#ROUTE 2
@goals_bp.route("", methods=["GET"])
def get_saved_goals():
    goals = Goal.query.all()

    goals_response = []
    for goal in goals:
        goals_response.append(goal.to_dict())

    return jsonify(goals_response)



#ROUTE 3
@goals_bp.route("/<goal_id>", methods=["GET"])
def get_one_goal(goal_id):
    try:
        goal = validate_model(Goal, goal_id)

        return make_response({"goal": goal.to_dict()}, 200)
    except KeyError:
        abort(make_response({'details': f"Goal {goal_id} not found"}, 404))


#ROUTE 4
@goals_bp.route("/<goal_id>", methods=["PUT"])
def update_one_goal(goal_id):
    try:
        goal_data = request.get_json()
        goal_to_update = validate_model(Goal, goal_id)

        goal_to_update.title = goal_data["title"]

        db.session.commit()

        return make_response({"Goal": goal_to_update.to_dict()}, 200)
    except KeyError:
        abort(make_response({'details': f"Goal{goal_id} not found"}, 404))

#ROUTE 5
@goals_bp.route("/<goal_id>", methods=["DELETE"])
def delete_one_goal(goal_id):
    try:
        goal = validate_model(Goal, goal_id)

        db.session.delete(goal)
        db.session.commit()


        message = {"details": f'Goal {goal_id} "{goal.title}" successfully deleted'}
        return make_response(message, 200)
    
    except KeyError:
        abort(make_response({'details': f"Goal {goal_id} not found"}, 404))

