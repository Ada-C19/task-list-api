from flask import Blueprint, request, jsonify, abort, make_response
from app import db
from app.models.goal import Goal
from app.models.task import Task
from app.routes_helper import validate_item_by_id

# Blueprint for goals
goals_bp = Blueprint("goals", __name__, url_prefix="/goals")

# Create a new goal
@goals_bp.route("", methods=["POST"])
def create_a_goal():
    
    request_body = request.get_json()
    
    try:
        new_goal = Goal(title=request_body["title"])
        
    except KeyError:
        return {
            "details": "Invalid data"
        }, 400
    db.session.add(new_goal)
    db.session.commit()
    
    return {
        "goal": new_goal.to_dict()
    }, 201
    

# Get saved goals
@goals_bp.route("", methods=["GET"])
def get_saved_goals():
    goals = Goal.query.all()
    goal_response = []
    if goals:
        for goal in goals:
            goal_response.append(goal.to_dict())
    return jsonify(goal_response), 200


# Get one goal by goal_id
@goals_bp.route("/<goal_id>", methods=["GET"])
def get_one_goal(goal_id):
    goal = validate_item_by_id(Goal, goal_id)
    return {
        "goal": goal.to_dict()
    }, 200


# Update one goal by its goal_id    
@goals_bp.route("/<goal_id>", methods=["PUT"])
def update_one_goal(goal_id):
    request_body = request.get_json()
    goal = validate_item_by_id(Goal, goal_id)
    
    goal.title = request_body["title"] if "title" in request_body else None
    
    db.session.commit()
    
    return {"goal": goal.to_dict()}, 200


# Delete one goal
@goals_bp.route("/<goal_id>", methods=["DELETE"])
def delete_one_goal(goal_id):
    goal_to_delete = validate_item_by_id(Goal, goal_id)
    
    db.session.delete(goal_to_delete)
    db.session.commit()
    
    return {
        "details": f'Goal {goal_to_delete.goal_id} "{goal_to_delete.title}" successfully deleted'
    }, 200
    

@goals_bp.route("/<goal_id>/tasks", methods=['GET'])
def handle_all_tasks_of_one_goal(goal_id):
    goal = validate_item_by_id(Goal, goal_id)
    response_body = goal.to_dict()
    tasks_response = []
    for task in goal.tasks:
        tasks_response.append(task.to_dict())
    response_body["tasks"] = tasks_response
    return jsonify(response_body), 200


@goals_bp.route("/<goal_id>/tasks", methods=['POST'])
def send_a_list_of_task_ids_to_one_goal(goal_id):
    goal = validate_item_by_id(Goal, goal_id)
    request_body = request.get_json()
    for task_id in request_body["task_ids"]:
        task = validate_item_by_id(Task, task_id)
        task.goal_id = goal_id
    db.session.commit()
    request_body["id"] = goal.goal_id
    return jsonify(request_body), 200

