from flask import Blueprint, jsonify, abort, make_response, request
from app import db
from app.models.task import Task
from app.models.goal import Goal
from app.routes import validate_model
from datetime import datetime
import requests
import os


goals_bp = Blueprint("goals_bp",__name__, url_prefix="/goals")

@goals_bp.route("", methods=["POST"])
def post_goal():
    request_body = request.get_json()
    
    if not request_body.get("title"):
        return jsonify({"details": "Invalid data"}), 400
    
    new_goal = Goal(
        title=request_body["title"]
        )

    db.session.add(new_goal)
    db.session.commit()

    return {
            "goal": {
            "id": new_goal.goal_id,
            "title": new_goal.title
        }
    }, 201

@goals_bp.route("", methods=["GET"])
def read_all_goals():
    goals = Goal.query.all()

    goal_response = []

    for goal in goals:
        goal_response.append({
            "title": goal.title
        })
    
    return jsonify(goal_response), 200