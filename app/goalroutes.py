from flask import abort, Blueprint, jsonify, make_response, request
from app import db
from app.models.goal import Goal

goal_bp = Blueprint("goals", __name__, url_prefix="/goals")

@goal_bp.route("", methods=["POST"])
def add_goal():
    request_body = request.get_json()
    try:
        new_goal = Goal.from_dict(request_body)
        # (
        #     title = request_body["title"]
        # )
    except KeyError:
        return  {
            "details": "Invalid data"
        }, 400

    db.session.add(new_goal)
    db.session.commit()

    return {"goal": {"id": new_goal.goal_id, "title": new_goal.title}}, 201
            
            # new_goal.to_dict()}, 201
