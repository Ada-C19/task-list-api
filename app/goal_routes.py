from app import db
from app.models.goal import Goal
from flask import Blueprint, abort, make_response

goals_bp = Blueprint("goals_bp", __name__, url_prefix="/goals")

def validate_goal(goal_id):
    try:
        goal_id = int(goal_id)
    except:
        abort(make_response({"message": f"goal {goal_id} is invalid"}, 400))
    
    goal = Goal.query.get(goal_id)
    
    if not goal:
        abort(make_response({"details": f"Goal {goal_id} not found"}, 404))
    
    return goal