from flask import Blueprint, request, jsonify, abort, make_response
from datetime import datetime
import requests, os
from app.models.goal import Goal
from app import db

#Blueprint for goals, all routes have url prefix (/goals)
goals_bp = Blueprint("goals_bp", __name__, url_prefix="/goals")

@goals_bp.route("", methods=["POST"])
def create_goal():
    request_body = request.get_json()
    if 'title' not in request_body:
        return {"details": "Invalid data"}, 400
    
    new_goal = Goal(title=request_body["title"])

    db.session.add(new_goal)
    db.session.commit()

    return {
        "goal":{
            "id":new_goal.goal_id,
            "title":new_goal.title
        }
    }, 201