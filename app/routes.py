from app import db 
from app.models.task import Task
from app.models.goal import Goal
from flask import Blueprint, jsonify, abort, make_response, request
from sqlalchemy import asc, desc
from datetime import datetime
import requests
import os

tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")
goals_bp = Blueprint("goals", __name__, url_prefix="/goals")

#helper functions
def validate_model(cls, model_id):
    try:
        model_id = int(model_id)
    except:
        abort(make_response({"{message":f"{cls.__name__} {model_id} invalid"}, 400))
            
    model = cls.query.get(model_id)
    
    if not model: 
        abort(make_response({"message":f"{cls.__name__} {model_id} not found"}, 404))

    return model

#route functions 

#POST /tasks
@tasks_bp.route("", methods=["POST"])
def create_task():
    request_body = request.get_json()
    if ("title" not in request_body or "description" not in request_body):
        abort(make_response({"details": "Invalid data"},400))

    new_task = Task(
        title=request_body["title"],
        description=request_body["description"],
        # completed_at=request_body["completed_at"]
    )

    db.session.add(new_task)
    db.session.commit()

    return jsonify({"task":new_task.to_dict()}),201

#GET /tasks 
@tasks_bp.route("", methods=["GET"])
def get_all_tasks():
    # tasks= Task.query.all()
    sort_query=request.args.get("sort")
    tasks_query= Task.query

    if sort_query== "asc":
        tasks_query= Task.query.order_by(asc("title"))
    if sort_query == "desc":
        tasks_query= Task.query.order_by(desc("title"))

    tasks = tasks_query.all()
        
    tasks_response = [task.to_dict() for task in tasks]

    return jsonify(tasks_response)

#GET /tasks/1
@tasks_bp.route("/<task_id>", methods=["GET"])
def get_one_task(task_id):
    task = validate_model(Task, task_id)
    
    return jsonify({"task":task.to_dict()})

#PUT /tasks/1
@tasks_bp.route("/<task_id>", methods=["PUT"])
def update_task(task_id):
    task = validate_model(Task, task_id)
    request_body=request.get_json()
    task.title=request_body["title"]
    task.description=request_body["description"]
    db.session.commit()
    return jsonify({"task":task.to_dict()}),200

#DELETE /tasks/1
@tasks_bp.route("/<task_id>", methods=["DELETE"])
def delete_task(task_id):
    task = validate_model(Task, task_id)
    db.session.delete(task)
    db.session.commit()

    return jsonify({"details": f'Task {task_id} "{task.title}" successfully deleted'}),200

#Wave 3 
@tasks_bp.route("/<task_id>/mark_complete", methods=["PATCH"])
def mark_task_complete(task_id):
    task = validate_model(Task, task_id)
    task.completed_at = datetime.now()
    db.session.commit()

#Wave 4: send_slack_notification
    HEADER = {"AUTHORIZATION":os.getenv('SLACK_BOT_TOKEN')}
    DATA = {"channel":"task-notifications","text":"The task has been marked complete"}
    requests.post("https://slack.com/api/chat.postMessage",headers=HEADER, data=DATA)
    
    return jsonify({"task":task.to_dict()}),200

@tasks_bp.route("/<task_id>/mark_incomplete", methods=["PATCH"])
def mark_task_incomplete(task_id):
    task = validate_model(Task, task_id)
    task.completed_at = None 
    db.session.commit()

    return jsonify({"task":task.to_dict()}),200

#Wave 5
@goals_bp.route("", methods=["POST"])
def create_goal():
    request_body = request.get_json()
    if "title" not in request_body:
        abort(make_response({"details": "Invalid data"},400))
    
    new_goal=Goal.from_dict(request_body)
    db.session.add(new_goal)
    db.session.commit()

    return jsonify({"goal":new_goal.to_dict()}),201

@goals_bp.route("", methods=["GET"])
def get_all_goals():
    goals = Goal.query.all()
    goals_response = [goal.to_dict() for goal in goals]

    return jsonify(goals_response), 200

@goals_bp.route("/<goal_id>", methods=["GET"])
def get_one_goal(goal_id):
    goal= validate_model(Goal, goal_id)

    return jsonify({"goal":goal.to_dict()}),200

@goals_bp.route("/<goal_id>", methods=["PUT"])
def update_goal(goal_id):
    goal= validate_model(Goal, goal_id)
    request_body= request.get_json()
    goal.title=request_body["title"]
    db.session.commit()
    
    return jsonify({"goal":goal.to_dict()}),200

@goals_bp.route("/<goal_id>", methods=["DELETE"])
def delete_goal(goal_id):
    goal= validate_model(Goal, goal_id)
    
    db.session.delete(goal)
    db.session.commit()

    return jsonify({"details": f'Goal {goal_id} "{goal.title}" successfully deleted'}),200

### Wave 6 
#POST /goals/1/tasks
@goals_bp.route("/<goal_id>/tasks", methods=["POST"])
def create_task(goal_id):
    goal = validate_model(Goal, goal_id)
    tasks_to_add = request.get_json()
    new_tasks_to_add_goal = []

    for task_id in tasks_to_add["task_ids"]:
        new_task = validate_model(Task, task_id)
        new_tasks_to_add_goal.append(new_task)
    
    goal.tasks= new_tasks_to_add_goal
    db.session.commit()

    return make_response({
        "id": goal.goal_id,
        "task_ids": [task.task_id for task in goal.tasks]
    },200)


#GET /goals/1/tasks
@goals_bp.route("/<goal_id>/tasks", methods=["GET"])
def get_task_for_specific(goal_id): 
        goal = validate_model(Goal, goal_id)
        response_body=goal.to_dict()
        response_body["tasks"] = [task.to_dict() for task in goal.tasks]

        for task in response_body["tasks"]:
            task["goal_id"] = goal.goal_id

        return jsonify(response_body),200 



























    




