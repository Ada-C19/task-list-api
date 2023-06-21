from flask import Blueprint, jsonify, abort, make_response, request
from app.models.goal import Goal
from app.models.task import Task
from app.routes.helper_routes import validate_object
from app import db

goals_bp = Blueprint("goals_bp", __name__, url_prefix="/goals")

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

@goals_bp.route("/<goal_id>/tasks", methods=["GET"])
def get_one_goals_tasks(goal_id):
    goal=validate_object(Goal, goal_id)
    goal_response = goal.tasks_to_dict()

    return make_response(goal_response,200)

@goals_bp.route("/<goal_id>/tasks", methods=["POST"])
def post_tasks_to_goal(goal_id):
    goal = validate_object(Goal, goal_id)
    task_ids = request.json.get("task_ids")
 
    for task_id in task_ids:
        task = validate_object(Task, task_id)
        task.goal_id = goal_id

    db.session.commit()

    return make_response({"id": int(goal_id), "task_ids": task_ids}, 200)