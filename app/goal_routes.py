import os
import requests
from flask import Blueprint, jsonify, make_response, request
from app import db
from app.models.goal import Goal 
from app.models.task import Task
from app.helper import validate_goal, validate_task

#CREATE BP/ENDPOINT
goals_bp = Blueprint("goals", __name__, url_prefix="/goals")

# GET all goals - GET[READ] - /goals
@goals_bp.route("", methods =["GET"])
def get_all_goals():
    # if request.args.get("sort") == "asc":
    #     goals = Goal.query.order_by(Goal.title.asc())
    # elif request.args.get("sort") == "desc":
    #     goals = Goal.query.order_by(Goal.title.desc())
    # else:
    goals = Goal.query.all()
    goals_response = []
    for goal in goals:
        goals_response.append(goal.to_json())

    return jsonify(goals_response), 200

# GET one goal - /goals/<id>  - [READ]
@goals_bp.route("/<id>", methods=["GET"])
def get_one_goal(id):
    goal = validate_goal(id)
    return jsonify({"goal":goal.to_json()}), 200

#POST  - /goals - [CREATE]
@goals_bp.route("", methods= ["POST"])
def create_goal():
    request_body = request.get_json()
    new_goal = Goal.create_dict(request_body)
    db.session.add(new_goal)
    db.session.commit()
    return make_response({"goal":new_goal.to_json()}), 201

#UPDATE one goal- PUT /goals/<id>  [UPDATE]
@goals_bp.route("/<id>",methods=["PUT"])
def update_goal(id):
    goal = validate_goal(id)
    request_body = request.get_json()
    goal.update_dict(request_body)
    db.session.commit()

    return jsonify({"goal":goal.to_json()}), 200

#DELETE one goal -DELETE /goals/<id> [DELETE]
@goals_bp.route("/<id>", methods=["DELETE"])
def delete_goal(id):
    goal_to_delete = validate_goal(id)

    db.session.delete(goal_to_delete)
    db.session.commit()

    message = {"details": f'Goal 1 "{goal_to_delete.title}" successfully deleted'}
    return make_response(message, 200)

#POST tasks ids to goal  /goals/1/tasks [CREATE]
@goals_bp.route("/<id>/tasks", methods=["POST"])
def post_task_ids_to_goal(id):
    goal = validate_goal(id)
    request_body = request.get_json()
    
    validated_task = []
    [validated_task.append(validate_task(task_id)) for task_id in request_body["task_ids"]]
    # for task_id in request_body["task_ids"]:
    #     task = validate_task(task_id)
    #     validated_task.append(task)

    [goal.tasks.append(task) for task in validated_task if task not in goal.tasks]
    # for task in validated_task:
    #     if task not in goal.tasks:
    #         goal.tasks.append(task)

    db.session.commit()


    return make_response({"id" : goal.goal_id, "task_ids":request_body["task_ids"]}), 200

# GET one goal - /goals/<id>  - [READ]
@goals_bp.route("/<id>/tasks", methods=["GET"])
def get_tasks_in_one_goal(id):
    goal = validate_goal(id)
    goal_with_tasks = [Task.to_json(task) for task in goal.tasks]
    return jsonify({"id":goal.goal_id, "title":goal.title, "tasks":goal_with_tasks}), 200