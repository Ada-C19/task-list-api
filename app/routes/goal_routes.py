from flask import Blueprint, jsonify, abort, make_response, request
from app import db
from app.models.goal import Goal
from app.routes.routes_helpers import validate_model
import datetime

goals_bp = Blueprint("goals", __name__, url_prefix="/goals")




#POST endpoint CREATES A NEW Goal
@goals_bp.route("", methods=["POST"])
def create_Goal():
        request_body = request.get_json()
        try:
            new_goal = Goal.from_dict(request_body)
        except KeyError:
            return {
                "details": "Invalid data"
            }, 400
        db.session.add(new_goal)
        db.session.commit()

        return {f"Goal": new_goal.to_dict()}, 201

#GET ALL goals endpoint
@goals_bp.route("", methods=["GET"])
def read_all_goals():
    goals = Goal.query.all()

    goal_post = [goal.to_dict() for goal in goals]
    return jsonify(goal_post), 200
#GETS A Goal
@goals_bp.route("/<goal_id>", methods=["GET"])
def handle_Goal(Goal_id):
    goal = validate_model(Goal, Goal_id)
    
    return {f"goal": goal.to_dict()}, 200

#Update a Goal
@goals_bp.route("/<goal_id>", methods=["PUT"])
def update_Goal(goal_id):
    goal = validate_model(Goal, goal_id)

    request_body = request.get_json()
    goal.title = request_body["title"]


    db.session.commit()

    return {"goal": goal.to_dict()}

#MARK AS COMPLETE PATCH
# @goals_bp.route("/<Goal_id>/mark_complete", methods=["PATCH"])
# def mark_complete(Goal_id):
#     goal = validate_model(Goal, Goal_id)

#     #goal.completed_at = datetime.datetime.now()

#     db.session.commit()
#     #create_msg_slack(Goal)

#     return {"goal": goal.to_dict()}, 200

#MARK AS INCOMPLETE PATCH endpoint
# @goals_bp.route("/<Goal_id>/mark_incomplete", methods=["PATCH"])
# def mark_incomplete(Goal_id):
#     Goal = validate_model(Goal, Goal_id)

#     Goal.completed_at = None

#     db.session.commit()

#     return {"Goal": Goal.to_dict()}, 200

#DELETES A Goal
@goals_bp.route("/<goal_id>", methods=["DELETE"])
def delete_goal(goal_id):
    goal = validate_model(Goal, goal_id)

    db.session.delete(goal)
    db.session.commit()

    return make_response({'details': f'Goal {goal.Goal_id} "{goal.title}" successfully deleted'}, 200)