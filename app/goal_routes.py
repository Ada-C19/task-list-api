from app import db
from app.models.goal import Goal
from flask import Blueprint, abort, make_response, request

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

@goals_bp.route("", methods=["POST"])
def create_goal():
    request_body = request.get_json()
    
    if "title" not in request_body:
        abort(make_response({"details": "missing title"}, 400))
    
    new_goal = Goal(title=request_body["title"])
    
    db.session.add(new_goal)
    db.session.commit()
    
    return {
        "goal": {
            "id": new_goal.goal_id,
            "title": new_goal.title
        }
    }, 201