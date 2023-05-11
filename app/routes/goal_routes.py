from flask import Blueprint, jsonify, request, abort, make_response
from app import db
from app.models.goal import Goal

goal_bp = Blueprint("goals", __name__, url_prefix="/goals")

def validate_item(model, item_id):
    try:
        item_id = int(item_id)
    except ValueError:
        return abort(make_response({"details": "Invalid data"}, 400))
    
    return model.query.get_or_404(item_id)


@goal_bp.route("", methods=["POST"])
def create_goal():
    request_body = request.get_json()

    if "title" not in request_body:
        abort(make_response({"details": "Invalid data"}, 400))

    new_goal = Goal.from_goals_dict(request_body)

    db.session.add(new_goal)
    db.session.commit()

    return {"goal": new_goal.to_goals_dict()}, 201

@goal_bp.route("", methods=["GET"])
def get_goals():
    response = []

    all_goals = Goal.query.all()

    for goal in all_goals:
        response.append(goal.to_goals_dict())

    return jsonify(response), 200

@goal_bp.route("/<goal_id>", methods=["GET"])
def get_one_goal(goal_id):
    goal = validate_item(Goal, goal_id)

    return {"goal": goal.to_goals_dict()}, 200

@goal_bp.route("/<goal_id>", methods=["PUT"])
def update_goal(goal_id):
    goal = validate_item(Goal, goal_id)

    request_data = request.get_json()

    goal.title = request_data["title"]

    db.session.commit()

    return {"goal": goal.to_goals_dict()}, 200

@goal_bp.route("/<goal_id>", methods=["DELETE"])
def delete_goal(goal_id):
    goal = validate_item(Goal, goal_id)

    db.session.delete(goal)
    db.session.commit()

    return {"details": f'Goal {goal_id} "{goal.title}" successfully deleted'}, 200