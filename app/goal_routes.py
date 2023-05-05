from flask import Blueprint, request, jsonify, make_response, abort
from app.models.goal import Goal
from app import db

goals_bp = Blueprint("goals", __name__, url_prefix="/goals")

# CREATE GOAL ENDPOINT
@goals_bp.route("", methods=["POST"])
def create_goal():
    request_body = request.get_json()

    if not request_body.get("title"):
        abort(make_response({"details": "Invalid data"}, 400))
    else:
        new_goal = Goal(title=request_body["title"])

    db.session.add(new_goal)
    db.session.commit()

    return make_response(jsonify({"goal": response_body(new_goal)}), 201)

# GET GOALS ENDPOINT
@goals_bp.route("", methods=["GET"])
def read_goals():
    goals = Goal.query.all()

    goals_response = []

    for goal in goals:
        goals_response.append(response_body(goal))

    return jsonify(goals_response)

# GET ONE GOAL ENDPOINT
@goals_bp.route("/<goal_id>", methods=["GET"])
def read_one_goal(goal_id):
    goal = validate_goal(goal_id)

    return {"goal": response_body(goal)}

# UPDATE GOAL ENDPOINT
@goals_bp.route("/<goal_id>", methods=["PUT"])
def update_goal(goal_id):
    request_body = request.get_json()

    goal = validate_goal(goal_id)

    goal.title = request_body["title"]

    db.session.commit()

    return {"goal": response_body(goal)}

# DELETE GOAL ENDPOINT
@goals_bp.route("/<goal_id>", methods=["DELETE"])
def delete_goal(goal_id):
    goal = validate_goal(goal_id)

    db.session.delete(goal)
    db.session.commit()

    return make_response({"details": f"Goal {goal.goal_id} \"{goal.title}\" successfully deleted"})


# HELPER FUNCTIONS
def response_body(goal):
    return {
        "id": goal.goal_id,
        "title": goal.title
    }

def validate_goal(goal_id):
    try:
        goal_id = int(goal_id)
    except:
        abort(make_response({"message": f"Goal {goal_id} invalid"}, 400))

    goal = Goal.query.get(goal_id)

    if not goal:
        abort(make_response({"message": f"Goal {goal_id} not found"}, 404))

    return goal