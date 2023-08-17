from flask import abort, Blueprint, jsonify, make_response, request
from sqlalchemy import desc, asc
from app import db
from app.models.goal import Goal
from app.models.task import Task
from app.routes.goal_routes import goal_bp
from datetime import datetime, timezone
import requests
import os


@goal_bp.route("/<goal_id>/tasks", methods=["POST"])
def post_task_ids_to_goal(goal_id):
    request_body = request.get_json()
    goal = Goal.query.get_or_404(goal_id)
    
    db.session.commit()

    return {"id": goal_id, "task_ids": "goal.tasks"}, 200
