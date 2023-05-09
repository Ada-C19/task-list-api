from app import db
from app.models.goal import Goal
from app.routes.task_routes import validate_model
from flask import Blueprint, jsonify, abort, make_response, request

goal_bp = Blueprint("goals", __name__, url_prefix="/goals")

@goal_bp.route('', methods=['POST'])
def create_goal():
    request_body = request.get_json()
    try:
        new_goal = Goal(title=request_body["title"])
        db.session.add(new_goal)
        db.session.commit()
        response_dict = {}
        response_dict["goal"] = new_goal.to_dict()
        return make_response(response_dict, 201)
    except KeyError:
        details = {"details": "Invalid data"}
        abort(make_response(details, 400))

   
@goal_bp.route('', methods=['GET'])
def get_goals():
    goal_response = []
    goals = Goal.query.all()
    for goal in goals:
        goal_response.append(goal.to_dict())
    return jsonify(goal_response)


@goal_bp.route('/<goal_id>', methods=['GET'])
def get_one_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    response_dict = {}
    response_dict["goal"] = goal.to_dict()
    return response_dict

@goal_bp.route('/<goal_id>', methods=['PUT'])
def update_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    request_body = request.get_json()
    goal.title = request_body["title"]
    db.session.commit()
    response_dict = {}
    response_dict["goal"] = goal.to_dict()
    return make_response(response_dict, 200)

@goal_bp.route('/<goal_id>', methods=['DELETE'])
def delete_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    db.session.delete(goal)
    db.session.commit()
    response_body = {"details": f'Goal {goal_id} "{goal.title}" successfully deleted'}
    return make_response(response_body, 200)