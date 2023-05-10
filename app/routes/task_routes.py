from app import db
from app.models.task import Task
from flask import Blueprint, jsonify, make_response, request, abort
from datetime import datetime
import os
from slack_sdk import WebClient
import requests

tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")

#validates task
def validate_model_by_id(model, id):
    #handle invalid task id, return 400
    try:
        id = int(id)
    except: 
        abort(make_response(jsonify({"msg": f"{model.__name__}{id} is invalid."}), 400))
    
    model_object = model.query.get(id)
    
    if model_object is None:
        abort(make_response(jsonify({"msg": "task not found"}), 404))

    return model_object 

#creates one task
@tasks_bp.route ("", methods=["POST"])
def create_task():
    request_body = request.get_json()
    title = request_body.get("title")
    description = request_body.get("description")

    if not description or not title:
        return {"details": "Invalid data"}, 400
    
    new_task = Task(title=title, description=description)
    db.session.add(new_task)
    db.session.commit()

    return {"task": {
        "id": new_task.task_id,
        "title": new_task.title,
        "description": new_task.description,
        "is_complete": new_task.completed_at is not None}
    }, 201

#reads one task as long as at least one is saved   
@tasks_bp.route("", methods=["GET"])
def get_all_tasks():
    sorting_query = request.args.get("sort")
    if sorting_query == "asc":
        tasks=Task.query.order_by(Task.title.asc())
    elif sorting_query=="desc":
        tasks=Task.query.order_by(Task.title.desc())
    else:
        tasks = Task.query.all()
    
    tasks_response = []
    for task in tasks:
        tasks_response.append(task.to_dict())
    
    return make_response(jsonify(tasks_response), 200)

#gets one task by id
@tasks_bp.route("/<task_id>", methods=["GET"])
def single_task(task_id):
    task = validate_model_by_id(Task, task_id)
    return jsonify({"task": task.to_dict()}), 200

#update task by id 
@tasks_bp.route("/<task_id>", methods=["PUT"])
def update_task(task_id):
    get_task = Task.query.get(task_id)
    task = validate_model_by_id(Task, task_id)

    request_body = request.get_json()
    task.title = request_body["title"]
    task.description = request_body["description"]


    db.session.commit()
    
    return jsonify({"task": task.to_dict()}), 200

#deletes single task by id
@tasks_bp.route("/<task_id>", methods=["DELETE"])
def delete_single_task(task_id):
    task = validate_model_by_id(Task, task_id)
    db.session.delete(task)
    db.session.commit()
    success_message = f"Task {task.task_id} \"{task.title}\" successfully deleted"
    return jsonify({"details": success_message}), 200

#mark incomplete on an completed task
@tasks_bp.route("/<task_id>/mark_incomplete", methods=["PATCH"])
def mark_task_incomplete(task_id):
    task = validate_model_by_id(Task, task_id)

    if task.completed_at is None:
        # The task is already complete, no need to update it
        return {"task": task.to_dict()}, 200
    
    task.completed_at = None
    db.session.commit()

    return {"task": task.to_dict()}, 200

#marks complete on incompleted task 
@tasks_bp.route("/<task_id>/mark_complete", methods=["PATCH"])
def mark_task_complete(task_id):
    print("1111111111111111111111111")
    task = validate_model_by_id(Task, task_id)
    print("222222222222222222222")
    if task.completed_at is not None:
        # The task is already complete, no need to update it
        return {"task": task.to_dict()}, 200
    
    task.completed_at = datetime.utcnow()
    print("3**************************")
    db.session.commit()

    print("4**************************")
    #integrate slack
    slack_token= os.environ["SLACK_TOKEN"]
    client = WebClient(token=slack_token)
    result = client.chat_postMessage(channel="task-notifications",
        text=f"Someone just completed the task {task.title}")
    print("5**************************")

    return {"task": task.to_dict()}, 200
############

