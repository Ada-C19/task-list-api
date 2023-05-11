from os import abort
from app import db
from app.models.goal import Goal
from flask import Blueprint, jsonify, abort, make_response, request
from datetime import datetime
import requests  
import os


goals_bp = Blueprint("goal", __name__, url_prefix="/goals")


@goals_bp.route("", methods=["POST"])
def create_goal():
    request_body = request.get_json()
    if "title" not in request_body:
        return make_response(jsonify({"details": "Invalid data"}), 400)
    
    new_goal = Goal.from_dict(request_body)
    db.session.add(new_goal)
    db.session.commit()

    return make_response(jsonify(new_goal.to_dict()), 201)


@goals_bp.route("", methods=["GET"])
def get_goals():
    goals = Goal.query.all()
    goal_list = [goal.to_dict()["goal"]for goal in goals]
    return make_response(jsonify(goal_list), 200)


@goals_bp.route("/<goal_id>", methods=["GET"])
def read_one_goal(goal_id):
    goal = Goal.validate_goal(goal_id)
    return make_response(jsonify(goal.to_dict()), 200)


@goals_bp.route("/<goal_id>", methods=["PUT"])
def update_goal(goal_id):
    goal = Goal.validate_goal(goal_id)
    request_body = request.get_json()
    goal.title = request_body["title"]
    db.session.commit()
    return make_response(jsonify(goal.to_dict()), 200)


@goals_bp.route("/<goal_id>", methods=["DELETE"])
def delete_goal(goal_id):
    goal = Goal.validate_goal(goal_id)
    db.session.delete(goal)
    db.session.commit()
    return make_response(jsonify({"details": f'Goal {goal_id} "{goal.title}" successfully deleted'}))


