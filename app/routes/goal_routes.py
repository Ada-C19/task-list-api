from flask import Blueprint, jsonify, abort, make_response, request
from app import db
from app.models.goal import Goal
from app.models.task import Task
from app.routes.routes_helpers import validate_model
import datetime

goals_bp = Blueprint("goals", __name__, url_prefix="/goals")




#POST endpoint CREATES A NEW Goal
@goals_bp.route("", methods=["POST"])
def create_Goal():
        request_body = request.get_json()
        try:
            new_goal = Goal(title=request_body["title"])
        except KeyError:
            return {
                "details": "Invalid data"
            }, 400
        db.session.add(new_goal)
        db.session.commit()

        return {f"goal": new_goal.to_dict()}, 201

#GET ALL goals endpoint
@goals_bp.route("", methods=["GET"])
def read_all_goals():
    goals = Goal.query.all()

    goal_post = [goal.to_dict() for goal in goals]
    return jsonify(goal_post), 200
#GETS A Goal
@goals_bp.route("/<goal_id>", methods=["GET"])
def handle_Goal(goal_id):
    goal = validate_model(Goal, goal_id)
    
    return {f"goal": goal.to_dict()}, 200

#Update a Goal
@goals_bp.route("/<goal_id>", methods=["PUT"])
def update_Goal(goal_id):
    goal = validate_model(Goal, goal_id)

    request_body = request.get_json()
    goal.title = request_body["title"]


    db.session.commit()

    return {"goal": goal.to_dict()}

#DELETES A Goal
@goals_bp.route("/<goal_id>", methods=["DELETE"])
def delete_goal(goal_id):
    goal = validate_model(Goal, goal_id)

    db.session.delete(goal)
    db.session.commit()

    return make_response({'details': f'Goal {goal.goal_id} "{goal.title}" successfully deleted'}, 200)

#Connecting relationships
@goals_bp.route("/<goal_id>/tasks", methods=["GET"])
def read_all_tasks_in_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    goal_response = goal.to_dict_tasks()

    return make_response(goal_response), 200

@goals_bp.route("/<goal_id>/tasks", methods=["POST"])
def add_tasks_to_goal(goal_id):
    request_body = request.get_json()
    task_ids = request_body.get("task_ids")
    #task_ids = request.json.get("task_ids", [])

    for id in task_ids:
        task = validate_model(Task, id)
        task.goal_id = goal_id

    db.session.commit()

    return make_response({"id": int(goal_id), "task_ids": task_ids}, 200)
