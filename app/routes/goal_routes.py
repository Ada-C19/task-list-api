from flask import Blueprint, request, jsonify, make_response, abort 
from app import db
from app.models.goal import Goal

goals_bp = Blueprint("goals_bp", __name__, url_prefix="/goals")

# VALIDATE MODEL
def validate_model(cls, model_id):
    try:
        model_id = int(model_id)
    except:
        abort(make_response({"message":f"{cls.__name__} {model_id} invalid"}, 400))

    model = cls.query.get(model_id)

    if not model:
        abort(make_response({"message":f"{cls.__name__} {model_id} not found"}, 404))

    return model

# CREATE GOAL
@goals_bp.route("", methods=["POST"])
def create_goal():
    request_body = request.get_json()

    try:
        new_goal = Goal.from_dict(request_body)
    except KeyError as err:
        abort(make_response({"details": "Invalid data"}, 400))

    db.session.add(new_goal)
    db.session.commit()

    goal_message = {}
    goal_message["goal"] = new_goal.to_dict()

    return jsonify(goal_message), 201


# GET ALL AND SORT GOALS BY TITLE 
@goals_bp.route("", methods=["GET"])
def sort_by_title():
    sort_query = request.args.get("sort")
    if sort_query == "asc":
        goals = Goal.query.order_by(Goal.title)
    elif sort_query == "desc":
        goals = Goal.query.order_by(Goal.title.desc())
    else:
        goals = Goal.query.all()
    
    goal_response = [goal.to_dict() for goal in goals]
    
    return jsonify(goal_response)


# GET ONE GOAL
@goals_bp.route("/<goal_id>", methods=["GET"])
def get_one_goal(goal_id):
    goal = validate_model(Goal, goal_id)

    goal_message = {"goal": goal.to_dict()}

    return jsonify(goal_message)


# UPDATE GOAL
@goals_bp.route("/<goal_id>", methods=["PUT"])
def update_goal(goal_id):
    goal = validate_model(Goal, goal_id)

    request_body = request.get_json()

    goal.title = request_body["title"]

    db.session.commit()

    goal_message = {"goal": goal.to_dict()}

    return jsonify(goal_message)


# DELETE GOAL
@goals_bp.route("/<goal_id>", methods=["DELETE"])
def delete_goal(goal_id):
    goal = validate_model(Goal, goal_id)

    db.session.delete(goal)
    db.session.commit()

    goal_message = {"details": f'Goal {goal.goal_id} \"{goal.title}\" successfully deleted'}

    return jsonify(goal_message)



