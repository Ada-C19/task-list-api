from app import db
from app.models.task import Task
from app.models.goal import Goal
from flask import Blueprint, jsonify, abort, make_response, request
import requests
from datetime import * 
import os


# register task bp
task_bp = Blueprint("task_bp", __name__, url_prefix="/tasks")
SLACK_BOT_TOKEN = os.environ.get('SLACK_BOT_TOKEN')

# validate task by id!
def validate_model(cls, model_id):
    try:
        model_id = int(model_id)
    except:
        abort(make_response({"message":f"{cls.__name__} {model_id} invalid"}, 400))

    model = cls.query.get(model_id)

    if not model:
        abort(make_response({"message":f"{cls.__name__} {model_id} not found"}, 404))

    return model

# create task as a post request 
@task_bp.route("",methods=["POST"])
def create_task():
    request_body = request.get_json()

    #try except
    try:
        task = Task.from_dict(request_body)
    except:
        return {"details": "Invalid data"}, 400

    db.session.add(task)
    db.session.commit()

    return {"task":{
            "id": task.task_id,
            "description": task.description,
            "is_complete": (task.completed_at != None),
            "title": task.title}}, 201


# read all tasks 
@task_bp.route("",methods=["GET"])
def read_all_tasks():
    tasks = Task.query.all()

    # ascending sort
    sorting_query = request.args.get("sort")
    if sorting_query == "asc":
        tasks = Task.query.order_by(Task.title.asc()).all()
    elif sorting_query == "desc":
        tasks = Task.query.order_by(Task.title.desc()).all()
    else:
        tasks = Task.query.all()

    tasks_response = []
    for task in tasks:
        tasks_response.append(task.to_dict())
    
    return jsonify(tasks_response), 200


# read one task
@task_bp.route("/<task_id>", methods=["GET"])
def read_one_task(task_id):
    task = validate_model(Task, task_id)
    if task.goal_id:
        return {
            "task":{
                "id": task.task_id,
                "title": task.title,
                "description": task.description,
                "goal_id": task.goal_id, 
                "is_complete": (task.completed_at != None)
            }
        }
    else:
        return {
            "task":{
                "id": task.task_id,
                "title": task.title,
                "description": task.description,
                "is_complete": (task.completed_at != None)
            }
        }


    # if task.goal_id != None:
    #     result["task"]["goal_id"] = task.goal_id
    # return result, 200


# update a task
@task_bp.route("/<task_id>", methods=["PUT"])
def update_task(task_id):
    task_to_update = validate_model(Task, task_id)

    request_body = request.get_json()

    task_to_update.title = request_body["title"]
    task_to_update.description = request_body["description"]

    db.session.commit()

    return jsonify({"task":task_to_update.to_dict()}), 200


# patch request to mark complete on incompleted task
@task_bp.route("/<task_id>/mark_complete", methods=["PATCH"])
def update_task_to_completed(task_id):
    task = validate_model(Task, task_id)

    if task.completed_at is None:
        task.completed_at = datetime.utcnow()

    slack_message = f"Someone just completed the task {task.title}"
    # add header
    header = {"Authorization": f"Bearer {SLACK_BOT_TOKEN}"}
    # add response
    json_body = {
        "channel": "C057EA9H4G7",
        "text": slack_message
    }
    response = requests.post("https://slack.com/api/chat.postMessage", headers=header, json=json_body)

    # if the status code from response does not indicate successful action
    # if response.status_code != 200:
    # # send failure message 
    #     abort(make_response({"details": "Failed to send message to Slack"}, 500))

    db.session.commit()

    return jsonify({"task": task.to_dict()}), 200

@task_bp.route("/<task_id>/mark_incomplete", methods=["PATCH"])
def update_task_incomplete(task_id):
    task = validate_model(Task, task_id)

    if task.completed_at != None:
        task.completed_at = None

    db.session.commit()

    return jsonify({"task":task.to_dict()}), 200

# delete a task
@task_bp.route("/<task_id>", methods=["DELETE"])
def delete_task(task_id):
    
    task = validate_model(Task, task_id)

    db.session.delete(task)
    db.session.commit()

    return abort(make_response({"details":f"Task {task_id} \"{task.title}\" successfully deleted"}, 200))

