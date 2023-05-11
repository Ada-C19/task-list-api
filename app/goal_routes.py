from app import db
from app.models.goal import Goal
from flask import Blueprint, jsonify, make_response, abort, request

goals_bp = Blueprint("goals'", __name__, url_prefix = "/goals")

@goals_bp.route("", methods=["POST"])
def create_goal():
    request_body = request.get_json()

    if not request_body.get("title"):
        abort(make_response(
                {
                    "details": "Invalid data"
                }, 400
            ))

    goal = Goal(
        title = request_body["title"],
    )

    db.session.add(goal)
    db.session.commit()

    return make_response(
        {
            "goal": {
                "id": goal.goal_id,
                "title": goal.title,
            }
        }, 201
    )

@goals_bp.route("", methods=["GET"])
def read_goals():
    goals = Goal.query.all()

    goals_response = []
    for goal in goals:
        goals_response.append(
            {
                "id": goal.goal_id,
                "title": goal.title,
            }
        ), 200

    return jsonify(goals_response)

@goals_bp.route("/<goal_id>", methods=["GET"])
def read_one_saved_goal(goal_id):
    goal = validate_goal(goal_id)

    return {
        "goal": {
            "id": goal.goal_id,
            "title": goal.title,
        }
    }

@goals_bp.route("/<goal_id>", methods=["PUT"])
def update_goal(goal_id):
    goal = validate_goal(goal_id)

    request_body = request.get_json()

    goal.title = request_body["title"]

    db.session.commit()

    return make_response(
        {
            "goal": {
                "id": goal.goal_id,
                "title": goal.title,
            }
        }, 200
    )


def validate_goal(goal_id):
    goal = Goal.query.get(goal_id)

    if not goal:
        abort(make_response(
            {
                "details": "Goal ID not found"
            }, 404
        ))
    return goal