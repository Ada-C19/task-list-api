from flask import Blueprint,make_response,request,jsonify,abort
from app import db
from app.models.task import Task
from app.helper import validate_task
import requests
import json
import os
from dotenv import load_dotenv


load_dotenv()

SLACK_API_KEY = os.getenv("SLACK_API_KEY")

#CREATE BP/ENDPOINT
tasks_bp = Blueprint("tasks",__name__, url_prefix="/tasks")

#GET ALL tasks [GET]/tasks :(CREATE)
@tasks_bp.route("",methods=["GET"])
def get_all_tasks():
    if request.args.get("sort") == "asc":
        tasks = Task.query.order_by(Task.title.asc())
    elif request.args.get("sort") == "desc":
        tasks = Task.query.order_by(Task.title.desc())
    else:
        tasks = Task.query.all()

    tasks_response = []
    for task in tasks:
        tasks_response.append(task.to_dict())

    return jsonify(tasks_response),200


#GET one task [GET]/tasks/<id> :(CREATE)
@tasks_bp.route("/<id>",methods=["GET"])
def get_one_task(id):
    task = validate_task(id)

    return jsonify({'task':task.to_dict()}),200

#CREATE one task/must contain title+description [POST]/tasks/<id> :(CREATE)
@tasks_bp.route("", methods = ["POST"])
def create_tasks():
    request_body = request.get_json()

    try:
        if request_body["title"] or request_body["description"]:
            new_task = Task.create_dict(request_body)
    except KeyError:
        return make_response({"details": "Invalid data"}), 400

    db.session.add(new_task)
    db.session.commit()

    return jsonify({"task":new_task.to_dict()}), 201

#UPDATE one task/RETURN msg not found [PUT]/tasks/<id> :(UPDATE)
@tasks_bp.route("/<id>",methods=["PUT"])
def update_task(id):
    task = Task.query.get(id)
    if task is None:
        return jsonify({'error': 'Task not found'}),404
    
    request_body = request.get_json()
    task.update_dict(request_body)
    db.session.commit()

    return jsonify({'task':task.to_dict()}),200


#DELETE one task [DELETE]/tasks/<id> :(DELETE)
@tasks_bp.route("/<id>",methods=["DELETE"])
def delete_task(id):
    task_to_delete = validate_task(id)

    db.session.delete(task_to_delete)
    db.session.commit()

    message = {'details': f'Task {id} "{task_to_delete.title}" successfully deleted'}

    return make_response(message,200)

#PATCH mark as complete on incomplete [PATCH]/tasks/<id>/mark_complete :(UPDATE)
@tasks_bp.route("/<id>/mark_complete",methods=["PATCH"])
def mark_completed(id):
    task_to_complete = validate_task(id)
    task_to_complete.patch_complete()
    
    db.session.commit()

    path = "https://slack.com/api/chat.postMessage"

    params = {
        "channel":"C056SMYR32B", 
        "text": f"Task\"{task_to_complete.title}\" has been completed!"
        }
    
    headers = {"Authorization": os.environ.get("SLACK_API_KEY")}
    response = requests.post(path,params=params,headers=headers)
    

    return jsonify({"task":task_to_complete.to_dict()}),200


#PATCH mark as incomplete on in/complete [PATCH]/tasks/<id>/mark_incomplete :(UPDATE)
@tasks_bp.route("/<id>/mark_incomplete",methods=["PATCH"])
def mark_incomplete(id):
    task = Task.query.get(id)
    if task is None:
        return jsonify({'error':'Task not found'}),404
    task_incomplete = validate_task(id)
    request_body = request.get_json()
    task_incomplete.patch_incomplete()
    db.session.commit()

    return jsonify({"task":task_incomplete.to_dict()}),200






