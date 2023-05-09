from flask import Blueprint, request, jsonify, make_response, abort
from app import db
from app.models.goal import Goal

goal_bp = Blueprint("goals", __name__, url_prefix="/goals")

# @goal_bp.route("", methods=["POST"])
# def add_goal():
#     request_body = request.get_json()

#     new_goal = Goal(
#         title = request_body["title"]
#     )

#     db.session.add(new_goal)
#     db.session.commit()

    # return {"goal": }