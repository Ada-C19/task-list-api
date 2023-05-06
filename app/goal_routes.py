from flask import Blueprint, jsonify, request, make_response, abort
from sqlalchemy import asc, desc
from app import db
from app.models.goal import Goal
from app.models.task import Task
from datetime import datetime
from slack_sdk import WebClient
import os
import requests
from slack_sdk.errors import SlackApiError

goal_bp = Blueprint("goals", __name__, url_prefix="/goals")

@goal_bp.route("", methods=["POST"])
def add_goals():
    request_body = request.get_json()
    
    # if "title" not in request_body:
    #     return {f"details": "Invalid data"}, 400
    
    new_goal = Goal(
        title = request_body["title"]
    )

    db.session.add(new_goal)
    db.session.commit()

    return {"goal": new_goal.goal_to_dict()}, 201