from app import db
from flask import Blueprint, request, make_response, jsonify
from app.models.goal import Goal
from .routes_helpers import validate_model, slack_call
from sqlalchemy import text
from datetime import datetime

goals_bp = Blueprint("goals", __name__, url_prefix="/goals")

@goals_bp.route("", methods=["POST"])
def create_goal():
    request_body = request.get_json()
    new_goal = Goal(title=request_body["title"])

    db.session.add(new_goal)
    db.session.commit()

    new_goal = dict(id=new_goal.goal_id,title=new_goal.title)

    
    return make_response({"goal":new_goal}, 201)

@goals_bp.route("/<id>", methods=["PUT"])
def update_goal(id):
    goal = validate_model(Goal, id)
    request_body = request.get_json()

    goal.title = request_body['title'],
    
    db.session.commit()

    goal = dict(id=goal.goal_id,title=goal.title)

    return make_response({"goal":goal}, 200)