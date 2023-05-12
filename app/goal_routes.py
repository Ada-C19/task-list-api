from app import db
from app.models.goal import Goal
from app.models.task import Task
from flask import Blueprint, jsonify, abort, make_response, request
from app.routes import validate_model

goals_bp = Blueprint("goals_bp", __name__, url_prefix="/goals")


# GET ALL goalS
@goals_bp.route("", methods=["GET"])
def handle_goal():
    
    goals = Goal.query.all()
    
    goals_response = []
    for goal in goals:
        goals_response.append(goal.to_dict())


    return jsonify(goals_response)


# GET ONE goal
@goals_bp.route("/<goal_id>", methods = ["GET"])
def get_one_goal(goal_id):

    goal = validate_model(Goal, goal_id)

    return {"goal": goal.to_dict()}



#PUT METHOD, UPDATE
@goals_bp.route("/<goal_id>", methods=["PUT"])
def update_goal(goal_id):
    goal = validate_model(Goal, goal_id)

    request_body = request.get_json()

    goal.title = request_body["title"]

    db.session.commit()

    return make_response(jsonify({"goal": goal.to_dict()}), 200)


#DELETE METHOD
@goals_bp.route("/<goal_id>", methods=["DELETE"])
def delete_goal(goal_id):
    goal = validate_model(Goal, goal_id)

    db.session.delete(goal)
    db.session.commit()

    return make_response(jsonify({"details": f"Goal {goal.goal_id} \"{goal.title}\" successfully deleted"}), 200)

#POST METHOD, CREATE NEW ROW OF DATA
@goals_bp.route("", methods=["POST"],strict_slashes=False)
def create_goals():
    request_body = request.get_json()

    if "title" not in request_body:
        return make_response(jsonify({"details": "Invalid data"}), 400)
    new_goal= Goal.from_dict(request_body)

    
    db.session.add(new_goal)
    db.session.commit()

    return make_response(jsonify({"goal": new_goal.to_dict()}), 201)


#Set tasks to a goal
@goals_bp.route("/<goal_id>/tasks", methods = ["POST"])
def post_all_tasks_for_one_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    
    request_body = request.get_json()
    task_id_list = request_body["task_ids"]
    
    for task_id in task_id_list:
        task = validate_model(Task, task_id)
        task.goal_id = goal_id 
    db.session.commit()
    return jsonify({"id": goal.goal_id, "task_ids": task_id_list})
    
#get all taks for one goal
@goals_bp.route("/<goal_id>/tasks", methods = ["GET"])
def get_one_goal_with_tasks(goal_id):
    goal = validate_model(Goal, goal_id)
    return jsonify(goal.to_dict_with_tasks())
    