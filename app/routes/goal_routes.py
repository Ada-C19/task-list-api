from flask import Blueprint, request, jsonify, abort, make_response
from app.models.goal import Goal
from app import db
from helper import validate_model
from sqlalchemy import asc, desc
from datetime import datetime
import requests
import json
import os


goals_bp = Blueprint("goals", __name__, url_prefix="/goals")


# POST
@goals_bp.route("", methods=["POST"])
def create_goal():
    goal_data = request.get_json()
    try:
        new_goal = Goal.from_dict(goal_data)
        db.session.add(new_goal)
        db.session.commit()

        message = {"goal": new_goal.to_dict()}
        return make_response(jsonify(message), 201)

    except KeyError:
        message = {"details": "Invalid data"}
        abort(make_response(jsonify(message), 400))


# GET
@goals_bp.route("", methods=["GET"])
def get_all_goals():
    all_goals = Goal.query.all()
    goals_reponse = [goal.to_dict() for goal in all_goals]

    return make_response(jsonify(goals_reponse), 200)


@goals_bp.route("/<goal_id>", methods=["GET"])
def get_one_goal(goal_id):
    goal = validate_model(Goal, goal_id)

    message = {"goal": goal.to_dict()}
    return make_response(jsonify(message), 200)


# PUT
@goals_bp.route("/<goal_id>", methods=["PUT"])
def update_goal(goal_id):
    goal_to_update = validate_model(Goal, goal_id)
    response = request.get_json()

    goal_to_update.title = response["title"]
    db.session.commit()

    message = {"goal": goal_to_update.to_dict()}
    return make_response(jsonify(message), 200)


# DELETE
@goals_bp.route("/<goal_id>", methods=["DELETE"])
def delete_goal(goal_id):
    goal_to_delete = validate_model(Goal, goal_id)
    db.session.delete(goal_to_delete)
    db.session.commit()

    message = {
        "details": f'Goal {goal_to_delete.goal_id} "{goal_to_delete.title}" successfully deleted'}
    return make_response(jsonify(message), 200)
