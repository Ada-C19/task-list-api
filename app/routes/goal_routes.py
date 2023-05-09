from flask import Blueprint, jsonify, abort, make_response, request
from app.models.goal import Goal
from app import db

goals_bp = Blueprint("goals_bp", __name__, url_prefix="/goals")

def validate_object(cls, goal_id):
    #handle invalid goal id, return 400
    try:
        goal_id = int(goal_id)
    except: 
        abort(make_response({"msg": f"{cls.__name__} {goal_id} is invalid."}, 400))
    
    goal = Goal.query.get(goal_id)
    if goal is None:
        abort(make_response({"msg": "goal not found."}, 404))

    return goal 

@goals_bp.route("", methods=["GET"])
def get_all_goals():
    
    sort_query = request.args.get("sort")

    if sort_query == "asc":
        goals = Goal.query.order_by(Goal.title.asc())
    
    elif sort_query == "desc":
        goals = Goal.query.order_by(Goal.title.desc())
    else:
        goals = Goal.query.all()
        
    goal_dict = [goal.to_dict() for goal in goals]
    return jsonify(goal_dict), 200

@goals_bp.route("/<goal_id>", methods=["GET"])
def single_goal(goal_id):
    goal = validate_object(Goal,goal_id)
    return jsonify({"goal": goal.to_dict()}), 200

@goals_bp.route("/<goal_id>", methods=["PUT"])
def update_goal(goal_id):
    goal = validate_object(Goal, goal_id)

    request_body = request.get_json()

    goal.title = request_body["title"]

    db.session.commit()
    
    return jsonify({"goal":goal.to_dict()}), 200

@goals_bp.route("/<goal_id>", methods=["DELETE"])
def delete_single_goal(goal_id):
    goal = validate_object(Goal, goal_id)

    db.session.delete(goal)    
    db.session.commit()

    success_message = f"goal {goal.goal_id} \"{goal.title}\" successfully deleted"
    return jsonify({"details": success_message}), 200


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