import os
import requests
from flask import Blueprint, jsonify, make_response, request
from app import db
from app.models.goal import Goal
from app.helper import validate_goal

#CREATE BP/ENDPOINT
goals_bp = Blueprint("goals", __name__, url_prefix="/goals")

#POST  - /goals - [CREATE]
@goals_bp.route("", methods= ["POST"])
def create_goal():
    request_body = request.get_json()
    new_goal = Goal.create_dict(request_body)
    db.session.add(new_goal)
    db.session.commit()
    return make_response({"goal":new_goal.to_json()}), 201

# GET one goal - /goals/<id>  - [READ]
@goals_bp.route("/<id>", methods=["GET"])
def get_one_goal(id):
    goal = validate_goal(id)
    return jsonify({"goal":goal.to_json()}), 200



#POST request/response [POST] / one goal  (CREATE)
