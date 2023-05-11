from app import db
from app.util import validate_object
from app.models.task import Task
from flask import Blueprint, jsonify, make_response, request, abort
from datetime import datetime
import os
import requests


task_bp = Blueprint("tasks", __name__, url_prefix="/tasks")

@task_bp.route("", methods=["POST"])
def create_tasks():
    
    request_body = request.get_json()
    try:
        new_task = Task.from_dict(request_body)
    except:
        abort(make_response({"details": "Invalid data"},400))
        
    db.session.add(new_task)
    db.session.commit()
    
    response_body = {"task": new_task.to_dict()}
    
    return make_response(jsonify(response_body), 201)


@task_bp.route("", methods=["GET"])
def read_all_tasks():
    sort = request.args.get("sort")
    tasks_query = Task.query
    if sort == "desc":
        tasks_query = tasks_query.order_by(Task.title.desc())
    elif sort == "asc":
        tasks_query = tasks_query.order_by(Task.title.asc())


    title = request.args.get("title")
    if title:
        tasks = tasks_query.filter_by(title=title)
    else:
        tasks = tasks_query.all()


    task_response = []
    for task in tasks:
        task_response.append(task.to_dict())

    return jsonify(task_response)


@task_bp.route("/<task_id>", methods=["GET"])
def read_one_task(task_id):
    task = validate_object(Task,task_id)
    return make_response(jsonify({"task":task.to_dict()}))


@task_bp.route("/<task_id>", methods=["DELETE"])
def delete_task(task_id):

    task = validate_object(Task,task_id)
    db.session.delete(task)
    db.session.commit()

    return make_response(jsonify({"details": f"Task {task_id} \"{task.title}\" successfully deleted"}), 200)


@task_bp.route("/<task_id>", methods=["PUT"])
def update_task(task_id):
    task = validate_object(Task,task_id)

    request_body = request.get_json()

    task.title = request_body["title"]
    task.description = request_body["description"]

    db.session.commit()

    return make_response(jsonify({"task":task.to_dict()}),200)

@task_bp.route("/<task_id>/mark_complete", methods=["PATCH"])
def update_task_completion(task_id):

    task = validate_object(Task,task_id)
    task.completed_at = datetime.now()
    db.session.commit()

    url = "https://slack.com/app.client.chat_postMessage"
    slack_token = os.environ.get("SLACK_API_TOKEN")
    data = {
        "channel": "task-notifcations",
        "text": f"string taesk {task.title}",
        "token" : slack_token
    }
    reponse = requests.post(url, data=data)
    
    return make_response(jsonify({"task":task.to_dict()}),200)

@task_bp.route("/<task_id>/mark_incomplete", methods=["PATCH"])
def update_task_inecompletion(task_id):

    task = validate_object(Task,task_id)
    task.completed_at = None
    db.session.commit()
    
    return make_response(jsonify({"task":task.to_dict()}))