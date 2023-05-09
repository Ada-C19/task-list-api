from flask import Blueprint, jsonify, abort, make_response, request
from app import db
from app.models.goal import Goal

goals_bp = Blueprint("goals", __name__, url_prefix="/goals")

@goals_bp.route("", methods=["POST"])
def create_goal():
    request_body = request.get_json()

    try:
        new_goal = Goal.from_dict(request_body)
    except:
        abort(make_response({"details": "Invalid data"}, 400))

    db.session.add(new_goal)
    db.session.commit()

    return {"goal":new_goal.to_dict()}, 201

@goals_bp.route("", methods=['GET'])
def handle_goals():
    title_query = request.args.get("sort")

    if title_query:
        if title_query == "asc":
            goals = Goal.query.order_by(Goal.title.asc())
        elif title_query == "desc":
            goals = Goal.query.order_by(Goal.title.desc())
    else:
        goals = Goal.query.all()
    goals_response = [goal.to_dict() for goal in goals]

    return jsonify(goals_response), 200

def get_valid_item_by_id(model, id):
    try:
        id = int(id)
    except:
        abort(make_response({"message":f"Goal {id} invalid"}, 400))

    item = model.query.get(id)

    return item if item else abort(make_response({"message":f"Goal {id} not found"}, 404))

@goals_bp.route("/<goal_id>", methods=["GET"])
def handle_goal(goal_id):
    goal = get_valid_item_by_id(Goal, goal_id)
    # may not need line below, has worked for others as it's already
    # returned in get_valid_item_by_id
    goal.query.get(goal_id)

    return {"goal":{
        "id": goal.goal_id,
        "title": goal.title}}, 200

@goals_bp.route("/<goal_id>", methods=["PUT"])
def update_goal(goal_id):
    goal = get_valid_item_by_id(Goal, goal_id)
    request_body = request.get_json()

    goal.title = request_body["title"]
    # replace code below with id instead of description or just delete since we don't get id for tasks so why would we for goals
    # goal.description = request_body["description"]

    db.session.commit()

    return {"goal":goal.to_dict()},200

@goals_bp.route("/<goal_id>", methods=["DELETE"])
def delete_goal(goal_id):
    goal = get_valid_item_by_id(Goal, goal_id)
    db.session.delete(goal)
    db.session.commit()

    return {"details": f"goal {goal_id} \"{goal.title}\" successfully deleted"}