from app import db
from flask import Blueprint, request, make_response, abort, jsonify
from app.routes_helpers import validate_model
from app.models.goal import Goal


goals_bp = Blueprint("goals", __name__, url_prefix="/goals")


@goals_bp.route("", methods=["POST"])
def create_goal():
    request_body = request.get_json()

    if not request_body.get("title"):
        abort(make_response({"details": "Invalid data"}, 400))

    goal = Goal.from_dict(request_body)

    db.session.add(goal)
    db.session.commit()

    return make_response(goal.to_dict(), 201)


@goals_bp.route("", methods=["GET"])
def get_all_goals():
    goals = Goal.query.all()

    goals_response = [goal.to_dict()["goal"] for goal in goals]

    return make_response(jsonify(goals_response), 200)


@goals_bp.route("/<goal_id>", methods=["GET"])
def get_one_goal(goal_id):
    goal = validate_model(Goal, goal_id)

    return make_response(goal.to_dict(), 200)


@goals_bp.route("/<goal_id>", methods=["PUT"])
def update_goal(goal_id):
    request_body = request.get_json()
    goal = validate_model(Goal, goal_id)
 
    if request_body["title"]:
        goal.title = request_body["title"]
  
    return make_response(goal.to_dict(), 200)


@goals_bp.route("/<goal_id>", methods=["DELETE"])
def delete_goal(goal_id):
    goal = validate_model(Goal, goal_id)

    db.session.delete(goal)
    db.session.commit()

    return make_response({"details": f"Goal {goal.id} \"{goal.title}\""
                         " successfully deleted"}, 200)
