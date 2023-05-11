from flask import Blueprint, jsonify, make_response, request
import os, requests
from app import db
from app.models.task import Task
from app.helper import validate_id

tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")

#get all tasks-"/tasks"-GET(read)
@tasks_bp.route("", methods=["GET"])
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
    return jsonify(tasks_response), 200


#get one tasks-"/tasks/1"-GET(read)
@tasks_bp.route("/<id>", methods=["GET"])
def get_task(id):
    task = validate_id(id)
    return jsonify({"task":task.to_dict()}), 200


#create task-"/tasks"-POST(create)
@tasks_bp.route("", methods=["POST"])
def create_task():
    request_body = request.get_json()
    try:
        new_task = Task.create(request_body)
    except KeyError:
        return make_response({"details": "Invalid data"}), 400
    
    db.session.add(new_task)
    db.session.commit()
    return jsonify({"task":new_task.to_dict()}), 201


#update task-"tasks/1"-PUT(update)
@tasks_bp.route("/<id>", methods=["PUT"])
def update_task(id):
    task = validate_id(id)
    request_body = request.get_json()
    task.update(request_body)
    db.session.commit()
    return jsonify({"task":task.to_dict()}), 200


#delete task-"tasks/1"-DELETE(delete)
@tasks_bp.route("/<id>", methods=["DELETE"])
def delete_task(id):
    task = validate_id(id)
    db.session.delete(task)
    db.session.commit()
    return jsonify({"details": f'Task {id} "{task.to_dict()["title"]}" successfully deleted'}), 200

SLACK_API_URL = "https://slack.com/api/chat.postMessage"
SLACKBOT_TOKEN = "xoxb-4680452269380-5269316188848-cgZRMqukeZCylI3G4FAOGG9p"

#patch task-"tasks/1/mark_complete"-PATCH(update)
@tasks_bp.route("/<id>/mark_complete", methods=["PATCH"])
def mark_complete(id):
    task = validate_id(id)
    request_body = request.get_json()
    task.patch_complete()
    db.session.commit()    
    slackbot_token = os.environ.get('SLACKBOT_TOKEN')
    if slackbot_token is None:
        return jsonify({'error': 'Slackbot token not set'}), 500
    message = f"Someone just completed the task {task.title}"
    channel = request_body.get('channel', 'task-notification')
    headers = {'Authorization': f'Bearer {slackbot_token}'}
    payload = {
    'channel': channel,
    'text': message,
    }
    response = requests.post(SLACK_API_URL, headers=headers, json=payload)
    if not response.ok:
        return jsonify({'error': 'Failed to send Slack message'}), 500

    return jsonify({"task":task.to_dict()}), 200


#patch task-"tasks/1/mark_incomplete"-PATCH(update)
@tasks_bp.route("/<id>/mark_incomplete", methods=["PATCH"])
def mark_incomplete(id):
    task = validate_id(id)
    request_body = request.get_json()
    task.patch_incomplete()
    db.session.commit()
    return jsonify({"task":task.to_dict()}), 200






