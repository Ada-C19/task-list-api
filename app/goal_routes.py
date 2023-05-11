from flask import Blueprint, jsonify, abort, request,make_response
from app.models.goal import Goal
from app import db
from app.helpers import validate_model

goals_bp = Blueprint("goals", __name__, url_prefix="/goals")


@goals_bp.route("", methods=["GET"])
def get_goals():

    goals = Goal.query.all()

    response_body = []
    for goal in goals:
        response_body.append(goal.to_dict())

    return make_response(jsonify(response_body), 200)


@goals_bp.route("/<goal_id>", methods=["GET"])
def get_one_goal(goal_id):

    goal = validate_model(Goal, goal_id)
    return make_response({"goal": goal.to_dict()}, 200)
    

@goals_bp.route("", methods=["POST"])
def post_goal():
    request_data = request.get_json()

    try:
        new_goal = Goal.from_dict(request_data)
        db.session.add(new_goal)
        db.session.commit()
        return make_response({"goal": new_goal.to_dict()}, 201)
    except KeyError:
        abort(make_response({"details": "Invalid data"}, 400))



@goals_bp.route("/<goal_id>", methods=["PUT"])
def update_goal(goal_id):

    request_data = request.get_json()
    goal_to_update = validate_model(Goal, goal_id)

    try:
        goal_to_update.title = request_data["title"]
        db.session.commit()
        return make_response({"title":"Updated Goal Title"}, 200)
    except:
        abort(make_response({"details": "Invalid data"}, 400))


@goals_bp.route("/<goal_id>", methods=["DELETE"])
def delete_goal(goal_id):

    goal = validate_model(Goal, goal_id)

    db.session.delete(goal)
    db.session.commit()
    
    message = f'Goal {goal.id} \"Build a habit of going outside daily\" successfully deleted'
    return make_response({"details": message}, 200)
    

