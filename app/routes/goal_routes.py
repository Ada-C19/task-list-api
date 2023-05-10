from app import db
from app.models.goal import Goal
from flask import Blueprint, jsonify, abort, make_response, request
from app.helpers.helpers import validate_model, send_message

goal_bp = Blueprint("goal_bp", __name__, url_prefix="/goals")

@goal_bp.route("", methods=["POST"])
def create_goal():
    request_body = request.get_json()
    try:
        new_goal = Goal.from_dict(request_body)

        db.session.add(new_goal)
        db.session.commit()
        
    
        return {"goal" : new_goal.to_dict()}, 201
    
    except KeyError as e:
        abort(make_response({"message": f"missing required value: {e}"}, 400))

    # except KeyError:
    #     abort(make_response({"details": "Invalid data"}, 400))

    db.session.add(new_goal)
    db.session.commit()


@goal_bp.route("", methods=["GET"])
def get_all_goals():
    goals = Goal.query.all()
    if not goals:
        return make_response(jsonify([]), 200)
    
    results = [goal.to_dict() for goal in goals]
    return jsonify(results)


@goal_bp.route("/<goal_id>", methods=["GET"])
def get_goal_by_id(goal_id):
    goal = validate_model(Goal, goal_id)
    
    results = {"goal" : goal.to_dict()}

    return make_response(jsonify(results), 200)

@goal_bp.route("/<goal_id>", methods=["PUT"])
def update_goal(goal_id):
    goal_data = request.get_json() #maybe change goal_data and task_data to request body
    goal_to_update = validate_model(Goal, goal_id)

    goal_to_update.title = goal_data["title"]

    db.session.commit()

    return {"goal" : goal_to_update.to_dict()}

@goal_bp.route("/<goal_id>", methods=["DELETE"])
def delete_goal(goal_id):
    goal = validate_model(Goal, goal_id)

    db.session.delete(goal)
    db.session.commit()

    return make_response({"details": f"Goal {goal_id} \"{goal.title}\" successfully deleted"})

