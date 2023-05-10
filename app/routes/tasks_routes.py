from app import db
from app.models.task import Task
from app.models.goal import Goal
from flask import Blueprint, jsonify, abort, make_response, request
from datetime import *
import requests
import os


tasks_bp = Blueprint("tasks_bp",__name__, url_prefix="/tasks")


def validate_model(cls, model_id):
    try:
        model_id = int(model_id)
    except:
        abort(make_response({"message":f"{cls.__name__} {model_id} invalid"}, 400))

    model = cls.query.get(model_id)

    if not model:
        abort(make_response({"message":f"{cls.__name__} {model_id} not found"}, 404))

    return model
    

@tasks_bp.route("",methods=["POST"])
def create_task():
    request_body = request.get_json()

    try:
        new_task = Task.from_dict(request_body)
    except:
        return {"details": "Invalid data"} , 400
    
    db.session.add(new_task)
    db.session.commit()

    return {"task": {"id":new_task.id,
            "title": new_task.title,
            "description": new_task.description,
            "is_complete": (new_task.completed_at != None)}}, 201

@tasks_bp.route("",methods=["GET"])
def read_all_tasks():

    sort_query = request.args.get("sort")

    if sort_query == "asc":
        tasks = Task.query.order_by(Task.title.asc()).all()
    elif sort_query == "desc":
        tasks = Task.query.order_by(Task.title.desc()).all()
    else:
        tasks = Task.query.all()

    tasks_response = []
    for task in tasks:
        tasks_response.append(task.to_dict())
    return jsonify(tasks_response), 200


@tasks_bp.route("/<task_id>", methods=["GET"])
def read_one_task(task_id):
    task = validate_model(Task, task_id)
    result = {
        "task":{
            "id": task.id,
            "title": task.title,
            "description": task.description,
            "is_complete": (task.completed_at != None)}
        }
    if task.goal_id != None:
        result["task"]["goal_id"] = task.goal_id
    return result, 200


@tasks_bp.route("/<task_id>", methods=["PUT"])
def update_task(task_id):
    task_to_update = validate_model(Task, task_id)

    request_body = request.get_json()

    task_to_update.title = request_body["title"]
    task_to_update.description = request_body["description"]

    db.session.commit()

    return jsonify({"task":task_to_update.to_dict()}), 200


@tasks_bp.route("/<task_id>", methods=["DELETE"])
def delete_task(task_id):
    task = validate_model(Task, task_id)

    db.session.delete(task)
    db.session.commit()

    return abort(make_response({"details":f"Task {task_id} \"{task.title}\" successfully deleted"}, 200))


@tasks_bp.route("/<task_id>/mark_complete", methods=["PATCH"])
def update_task_complete_status(task_id):
    task = validate_model(Task, task_id)
    
    if task.completed_at is None:
        task.completed_at = datetime.utcnow()
    
        text_str = "Someone just completed the task " + task.title  
        
        url = 'https://slack.com/api/chat.postMessage'
        payload = {
                'token': os.environ.get("SLACK_API_TOKEN"),
                'channel': '#task-notifications',
                'text': text_str
            }
        
        response = requests.post(url, data=payload)
        return_response = response.status_code
        db.session.commit()

    return jsonify({"task":task.to_dict()}), 200

@tasks_bp.route("/<task_id>/mark_incomplete", methods=["PATCH"])
def update_task_incomplete_status(task_id):
    task = validate_model(Task, task_id)

    if task.completed_at != None:
        task.completed_at = None

    db.session.commit()

    return jsonify({"task":task.to_dict()}), 200


