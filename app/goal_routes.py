from flask import Blueprint
from app import db
from app.models.goal import Goal
from app.models.task import Task
from flask import Blueprint, jsonify, make_response, request, abort
from app.task_routes import validate_model
import pdb
# from sqlalchemy import asc, desc
# from datetime import datetime
# import requests
# import os
# import json


goals_bp = Blueprint("goals", __name__, url_prefix="/goals")


#goals routes:


@goals_bp.route("", methods=["POST"])
def create_goal():
    request_body = request.get_json()
    if not request_body.get("title"):
        abort(make_response({
            "details": "Invalid data"
        }, 400))

    new_goal = Goal.from_dict(request_body)

    db.session.add(new_goal)
    db.session.commit()

    return {
        "goal": new_goal.to_dict()
    }, 201

#este no tiene tests --> get all goals
@goals_bp.route("", methods=["GET"])
def get_goals():
    goals_response = []
    goals = Goal.query.all()

    for goal in goals:
        goals_response.append(goal.to_dict())
    return jsonify(goals_response)


#get goal by id
@goals_bp.route("/<goal_id>", methods=["GET"])
def get_goal_by_id(goal_id):
    goal = validate_model(Goal, goal_id)
    return {
        "goal": goal.to_dict()
    }, 200


#Update goal by id:
@goals_bp.route("/<goal_id>", methods=["PUT"])
def update_goal_by_id(goal_id):
    goal = validate_model(Goal, goal_id)

    request_body = request.get_json()
    goal.title = request_body["title"]

    db.session.commit()

    return {
        "goal": goal.to_dict()
    }

#Delete goal
@goals_bp.route("/<goal_id>", methods=["DELETE"])
def delete_goal(goal_id):
    goal = validate_model(Goal, goal_id)

    db.session.delete(goal)
    db.session.commit()

    return {
        "details": f'Goal {goal_id} "{goal.title}" successfully deleted'
    }


#nested routes:#####################################

# POST request to /goals/1/tasks
#asociando una lista de tasks to a goal. 
@goals_bp.route("/<goal_id>/tasks", methods=["POST"])
def post_tasks_ids_with_goals(goal_id):
    goal = validate_model(Goal, goal_id)
    request_body = request.get_json()
    task_ids = request_body.get("task_ids")
    added_ids = []
    for id in task_ids:
        #buscar en la base de datos el task --> 
        # task_desde_db = (buscar la task en DB en base al id)
        # puede suceder que el id no exista
        # si quer´s podes validar que task.goal sea None
        task_desde_db = Task.query.get(id)
        # task_desde_db.goal_id = goal.goal_id
        task_desde_db.goal = goal
        added_ids.append(task_desde_db.task_id)

    
    db.session.commit()
    
    return jsonify({
        "id": goal.goal_id,
        "task_ids": added_ids
    })
    

# author = validate_model(Author, author_id)

# request_body = request.get_json()
# new_book = Book(
#     title=request_body["title"],
#     description=request_body["description"],
#     author=author
# )



#getting all tasks of one goal:
@goals_bp.route("/<goal_id>/tasks", methods=["GET"])
def get_task_from_goal(goal_id):
    response = []
    goal = validate_model(Goal, goal_id)
    #ir a la task table i tomar todas las task  goal_id
    task_by_goal = Task.query.get(goal_id)

    if task_by_goal is None:
        return jsonify({
            "id": goal.goal_id,
            "title": goal.title,
            "tasks": response
        })
    else:
        #relationship
        task_by_goal.goal = goal
        for task in goal.tasks:
            response.append(
                task.to_dict()
            )
            
    return jsonify({
        "id": goal.goal_id,
        "title": goal.title,
        "tasks": response
    })



