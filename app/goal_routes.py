import os
import requests
from flask import Blueprint, jsonify, make_response, request
from app import db
from app.models.goal import Goal
from app.helper import validate_goal

#CREATE BP/ENDPOINT
goals_bp = Blueprint("goals", __name__, url_prefix="/goals")

# GET all goals - GET[READ] - /goals
@goals_bp.route("", methods =["GET"])
def get_all_goals():
    # if request.args.get("sort") == "asc":
    #     goals = Goal.query.order_by(Goal.title.asc())
    # elif request.args.get("sort") == "desc":
    #     goals = Goal.query.order_by(Goal.title.desc())
    # else:
    goals = Goal.query.all()
    goals_response = []
    for goal in goals:
        goals_response.append(goal.to_json())

    return jsonify(goals_response), 200


#POST  - /goals - [CREATE]
@goals_bp.route("", methods= ["POST"])
def create_goal():
    request_body = request.get_json()
    new_goal = Goal.create_dict(request_body)
    db.session.add(new_goal)
    db.session.commit()
    return make_response({"goal":new_goal.to_json()}), 201

# GET one goal - /goals/<id>  - [READ]
@goals_bp.route("/<id>", methods=["GET"])
def get_one_goal(id):
    goal = validate_goal(id)
    return jsonify({"goal":goal.to_json()}), 200

#UPDATE one goal- PUT /goals/<id>  (UPDATE)
@goals_bp.route("/<id>",methods=["PUT"])
def update_goal(id):
    goal = validate_goal(id)
    request_body = request.get_json()
    goal.update_dict(request_body)
    db.session.commit()

    return jsonify({"goal":goal.to_json()}), 200

#DELETE one goal -DELETE /goals/<id> (DELETE)
@goals_bp.route("/<id>", methods=["DELETE"])
def delete_goal(id):
    goal_to_delete = validate_goal(id)

    db.session.delete(goal_to_delete)
    db.session.commit()

    message = {"details": f'Goal 1 "{goal_to_delete.title}" successfully deleted'}
    return make_response(message, 200)

#POST request/response [POST] / one goal  (CREATE)
