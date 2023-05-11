from app import db
from app.models.goal import Goal
from app.models.task import Task
from flask import Blueprint, jsonify, abort, make_response, request
from app.tasks_routes import validate_model

goals_bp = Blueprint("goals_bp", __name__, url_prefix="/goals")


# Gets all Goals and returns 200 
@goals_bp.route("", methods = ["GET"])
def handle_goals():
    goal_response = []
    goals = Goal.query.all()

    for goal in goals:
        goal_response.append(goal.to_dict())

    return jsonify(goal_response), 200

# Gets one goal by goal_id and returns 200 if found
@goals_bp.route("/<goal_id>", methods = ["GET"])
def handle_goal(goal_id):
    goal = validate_model(Goal, goal_id)

    response_body = goal.as_goal_dict()

    return jsonify(response_body), 200



# Creates a Goal and returns 201 
@goals_bp.route("", methods = ["POST"])
def create_goal():
    request_body = request.get_json()

    if "title" not in request_body: 
        return make_response(jsonify({"details" : "Invalid data"}), 400)
    
    new_goal = Goal.from_dict(request_body)

    db.session.add(new_goal)
    db.session.commit()

    response_body = new_goal.as_goal_dict()

    return make_response(response_body, 201)

# Update a Goal and returns 200
@goals_bp.route("/<goal_id>", methods = ["PUT"])
def update_goal(goal_id):
    goal = validate_model(Goal, goal_id)

    request_body = request.get_json()
    goal.title = request_body["title"]

    db.session.commit()

    response_body = goal.as_goal_dict()

    return make_response(jsonify(response_body), 200)

# Deletes a goal by goal_id and returns 200
@goals_bp.route("/<goal_id>", methods = ["DELETE"])
def delete_goal(goal_id):
    goal = validate_model(Goal, goal_id)

    db.session.delete(goal)
    db.session.commit()

    return make_response(jsonify({"details": f"Goal {goal_id} \"{goal.title}\" successfully deleted"}), 200)

# Sends a list of task ids to a Goal 
@goals_bp.route("/<goal_id>/tasks", methods = ["POST"])
def create_goal_with_task_ids(goal_id):

    goal = validate_model(Goal, goal_id)

    request_body = request.get_json()
    task_ids = request_body.get("task_ids")

    goal.add_tasks_to_goal(task_ids)
    db.session.commit()

    response_body = goal.get_task_ids()

    return make_response(response_body, 200)

# Gets tasks of a goal
@goals_bp.route("/<goal_id>/tasks", methods = ["GET"])
def get_tasks_of_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    
    response_body = goal.to_dict(with_tasks=True)

    return make_response(response_body, 200)




    