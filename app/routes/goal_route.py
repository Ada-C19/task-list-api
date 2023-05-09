from flask import Blueprint, jsonify, abort, make_response, request
from app.models.goal import Goal
from app import db
from app.routes.task_route import validate_model

goals_bp = Blueprint("goals", __name__, url_prefix="/goals")

# route to get all goals

@goals_bp.route("", methods=["GET"])
def read_all_goals():

    goals = Goal.query.all()

    goal_response = []
    for goal in goals:
        goal_response.append(goal.to_dict())
    return jsonify(goal_response), 200

# route to create a new goal

@goals_bp.route("", methods=["POST"])
def create_goal():
    request_body = request.get_json()

    if request_body.get("title"):
        new_goal = Goal(title=request_body["title"])

        db.session.add(new_goal)
        db.session.commit()

        return {"goal": new_goal.to_dict()}, 201
    
    return jsonify({"details": "Invalid data"}), 400

# route to get a goal by id

@goals_bp.route("/<goal_id>", methods=["GET"])
def read_one_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    return {
        "goal": {
            "id": goal.goal_id,
            "title": f"{goal.title}",
        }
    }, 200

# route to update a goal by id

@goals_bp.route("/<goal_id>", methods=["PUT"])
def update_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    request_body = request.get_json()
    goal.title = request_body["title"]

    db.session.commit()

    return {
        "goal": {
            "id": goal.goal_id,
            "title": f"{goal.title}",
        }
    }, 200

# route to delete a goal by id

@goals_bp.route("/<goal_id>", methods=["DELETE"])
def delete_goal(goal_id):
    goal = validate_model(Goal, goal_id)

    db.session.delete(goal)
    db.session.commit()

    return jsonify({"details": f'Goal {goal_id} "{goal.title}" successfully deleted'}), 200