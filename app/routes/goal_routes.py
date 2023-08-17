from flask import abort, Blueprint, jsonify, make_response, request
from sqlalchemy import desc, asc
from app import db
from app.models.goal import Goal


goal_bp = Blueprint("goal", __name__, url_prefix="/goals")


@goal_bp.route("", methods=["POST"])
def create_new_goal():
    request_body = request.get_json()
    try:
        new_goal = Goal(
            title=request_body["title"],
        )
    except KeyError:
        return {"details": "Invalid data"}, 400
    
    db.session.add(new_goal)
    db.session.commit()

    return {"goal": new_goal.to_dict()}, 201


@goal_bp.route("", methods=["GET"])
def get_all_goals():
    sort_query = request.args.get("sort")
    if sort_query == "asc":
        goals = Goal.query.order_by(asc(Goal.title))
    elif sort_query == "desc":
        goals = Goal.query.order_by(desc(Goal.title))
    else:
        goals = Goal.query.all()

    response = []
    for goal in goals:
        response.append(goal.to_dict())

    return jsonify(response), 200


@goal_bp.route("/<goal_id>", methods=["GET"])
def get_one_goal(goal_id):
    goal = Goal.query.get_or_404(goal_id)
    return {"goal": goal.to_dict()}, 200


@goal_bp.route("/<goal_id>", methods=["PUT"])
def update_one_goal(goal_id):
    goal = Goal.query.get_or_404(goal_id)
    request_body = request.get_json()

    goal.title = request_body["title"]

    db.session.commit()

    return {"goal": goal.to_dict()}, 200


@goal_bp.route("/<goal_id>", methods=["DELETE"])
def delete_one_goal(goal_id):
    goal = Goal.query.get_or_404(goal_id)

    db.session.delete(goal)
    db.session.commit()

    return {"details": (f'Goal {goal.goal_id} "{goal.title}" '
                        'successfully deleted')}, 200