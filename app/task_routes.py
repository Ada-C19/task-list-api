from flask import Blueprint, jsonify, abort, make_response, request
from app import db
from app.models.task import Task
from app.models.goal import Goal
from datetime import datetime
import requests
import os

tasks_bp = Blueprint("tasks",__name__,url_prefix="/tasks")

@tasks_bp.route("", methods=["POST"])
def create_task():

    request_body = request.get_json()

    try:
        new_task = Task(title=request_body["title"],
        description=request_body["description"])

    except:
        abort(make_response({
        "details": "Invalid data"
    }, 400)) 

    db.session.add(new_task)
    db.session.commit()

    return make_response(jsonify({"task":{
        "id" : new_task.task_id,
        "title" : new_task.title,
        "description" : new_task.description,
        "is_complete" : False
        }}),201)

@tasks_bp.route("", methods=["GET"])
def get_tasks():

    sort_query = request.args.get("sort")

    if sort_query == "asc":
        tasks = Task.query.order_by(Task.title.asc()).all()
    elif sort_query == "desc":
        tasks = Task.query.order_by(Task.title.desc()).all()
    else:
        tasks = Task.query.all()

    tasks_response = [] 

    for task in tasks:
        tasks_response.append(
            task.to_dict()
        )
    
    return jsonify(tasks_response)

def validate_model(cls, model_id):
    try:
        model_id = int(model_id)
    except: 
        abort(make_response({"message":f"{model_id} is not valid type ({type(model_id)}) invalid. Please use integer."}, 400))
    
    model = cls.query.get(model_id)

    if not model:
        abort(make_response({"message":f"{cls.__name__} {model_id} does not exist"}, 404))
    
    return model

@tasks_bp.route("/<task_id>", methods=["GET"])
def get_one_task(task_id):
    
    task = validate_model(Task, task_id)
    
    if task.goal_id:
        return {
        "task": {
            "id": task.task_id,
            "goal_id": task.goal_id,
            "title": task.title,
            "description": task.description,
            "is_complete": False
        }
    }

    return {"task":task.to_dict()}, 200

@tasks_bp.route("/<task_id>", methods=["PUT"])
def update_one_task(task_id):
    task = validate_model(Task, task_id)
    
    request_body = request.get_json()

    task.title = request_body["title"]
    task.description = request_body["description"]
    
    db.session.commit()

    return make_response(jsonify({"task":task.to_dict()}),200)

def send_slack_message(task_title):
    
    path = 'https://slack.com/api/chat.postMessage'

    slack_key = os.environ.get("SLACK_API_KEY")

    params = {
        "channel":"general",
        "text":f"Someone just completed the task {task_title}"
    }
    headers = {
        "Authorization":slack_key
    }

    requests.get(path, headers=headers, params=params)

@tasks_bp.route("<task_id>/mark_complete", methods=["PATCH"])
def mark_complete(task_id):

    task = validate_model(Task, task_id)

    send_slack_message(task.title)
    
    task.completed_at = datetime.utcnow()

    db.session.commit()

    return make_response(jsonify({"task":task.to_dict()}),200)
    

@tasks_bp.route("<task_id>/mark_incomplete", methods=["PATCH"])
def mark_incomplete(task_id):

    task = validate_model(Task, task_id)

    task.completed_at = None

    db.session.commit()

    return make_response(jsonify({"task":task.to_dict()}),200)

@tasks_bp.route("/<task_id>", methods=["DELETE"])
def remove_one_task(task_id):

    task = validate_model(Task, task_id)

    db.session.delete(task)
    db.session.commit()

    return make_response({
        "details": f'{Task.__name__} {task_id} "{task.title}" successfully deleted'
    }), 200