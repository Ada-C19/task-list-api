from flask import Blueprint
from app import db
from app.models.task import Task
from app.models.goal import Goal
from flask import Blueprint, jsonify, make_response, request, abort
from sqlalchemy import asc, desc
from datetime import datetime
import requests
import os
import json


tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")


#helper function
def validate_model(cls,model_id):
    try:
        model_id = int(model_id)
    except:
        abort(make_response(
            {"message": f"{cls.__name__} {model_id} invalid"}, 400))

    task = cls.query.get(model_id)

    if not task:
        abort(make_response(
            {"message": f"{cls.__name__} {model_id} not found"}, 404))

    return task


def get_external_task_representation(task):
    return {
        "task": task.to_dict()
    }


#POST request
@tasks_bp.route("", methods=["POST"])
def create_task():
    request_body = request.get_json()
    if not request_body.get("description") or not request_body.get("title"):
            abort(make_response({
                    "details": "Invalid data"
                }, 400))

    # new_task = Task(title=request_body["title"],
    #                 description=request_body["description"],
    #                 completed_at=request_body.get("completed_at"))
    
    new_task = Task.from_dict(request_body)

    db.session.add(new_task)
    db.session.commit()
    # if new_task.completed_at is None:
    #     calculated_is_complete = False
    # else:
    #     calculated_is_complete = True
    # calculated_is_complete = not new_task.completed_at is None
    return get_external_task_representation(new_task), 201


#Get all request, take sort as params
@tasks_bp.route("", methods=["GET"])
def get_all_tasks():
    response = []
    sort_order = request.args.get("sort")

    if sort_order == "asc":
        all_tasks = Task.query.order_by(asc(Task.title)).all()
    elif sort_order == "desc":
        all_tasks = Task.query.order_by(desc(Task.title)).all()

    else:
        all_tasks = Task.query.all()
    
    for task in all_tasks:
        response.append(task.to_dict())

    return jsonify(response), 200


#Get one task by id:
@tasks_bp.route("/<task_id>", methods=["GET"])
def get_task_by_id(task_id):
    task = validate_model(Task,task_id)
    return get_external_task_representation(task), 200


#Update task by id
@tasks_bp.route("/<task_id>", methods=["PUT"])
def update_task_by_id(task_id):
    task = validate_model(Task,task_id)

    request_body = request.get_json()
    task.title = request_body["title"]
    task.description = request_body["description"]

    db.session.commit()

    return get_external_task_representation(task), 200


#Delete task 
@tasks_bp.route("/<task_id>", methods=["DELETE"])
def delete_task(task_id):
    task = validate_model(Task,task_id)

    db.session.delete(task)
    db.session.commit()

    return {
        "details": f'Task {task_id} "{task.title}" successfully deleted'
    }


def send_post_to_slack(task):
    slack_bot_token = os.environ['SLACK_BOT_TOKEN']
    slack_channel = 'task-notifications'
    text = f"Task {task.description} completed"
    headers = {'Authorization': slack_bot_token}
    data = {
        'channel': slack_channel,
        'text': text
    }
    response = requests.post(
        'https://slack.com/api/chat.postMessage', headers=headers, json=data)

    # if response.status_code == 200:
    #     return 'Message sent to Slack successfully.'
    # else:
    #     return 'Failed to send message to Slack.'


#responsability: to change (to completed) completed_at in the database with the time stamp 
# and return the response with is_complete: True:
@tasks_bp.route("/<task_id>/mark_complete", methods=["PATCH"])
def turn_complete(task_id):
    task = validate_model(Task, task_id)
    
    task.completed_at = datetime.utcnow()
    db.session.commit()

    #send a message to slack with request:
    send_post_to_slack(task)


    #esto queda:
    return get_external_task_representation(task), 200


#responsability: to change (to incomplete) completed_at in the database removing the time stamp
# and return the response with is_complete: False:
@tasks_bp.route("/<task_id>/mark_incomplete", methods=["PATCH"])
def turn_incomplete(task_id):
    task = validate_model(Task, task_id)

    task.completed_at = None
    db.session.commit()

    return get_external_task_representation(task), 200

