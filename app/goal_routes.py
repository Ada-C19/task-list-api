from flask import Blueprint, request, abort, make_response, jsonify
from app.models.goal import Goal
from app import db

goals_bp = Blueprint("goals_bp", __name__, url_prefix="/goals")

# Create
@goals_bp.route("", methods=["POST"])
def create_goal():
    request_body = request.get_json()
    check_goal_data(request_body)

    new_goal = Goal.from_dict(request_body)

    db.session.add(new_goal)
    db.session.commit()

    return make_response({"goal": new_goal.to_dict()}, 201)
    

# Read
@goals_bp.route("", methods=["GET"])
def list_all_goals():
    goals_response = []
    goals = Goal.query.all()
    for goal in goals:
        goals_response.append(goal.to_dict())

    return jsonify(goals_response)




# Helper Functions
def check_goal_data(request):
    if "title" not in request:
        return abort(make_response({"details": "Invalid data"}, 400))