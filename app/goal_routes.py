from flask import Blueprint, jsonify, abort, make_response, request
from app import db
from app.models.task import Task
from app.models.goal import Goal
from app.routes import validate_model
from datetime import datetime
import requests
import os


goals_bp = Blueprint("goals_bp",__name__, url_prefix="/goals")

@goals_bp.route("/goals", methods=["POST"])
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
    }