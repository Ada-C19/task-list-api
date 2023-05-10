from flask import Blueprint, jsonify, abort, make_response, request
from app import db
from app.models.task import Task
from app.models.goal import Goal
from datetime import datetime
import requests
import os

tasks_bp = Blueprint("tasks_bp", __name__, url_prefix="/tasks")

def validate_model(cls, model_id):
    try: 
        model_id = int(model_id)
    except:
        abort(make_response({"details": "Invalid data"}, 400))
    
    model = cls.query.get(model_id)

    if not model: 
        abort(make_response({"details": f"{cls.__name__} id {model_id} not found"}, 404))
        
    return model 

@tasks_bp.route("", methods=['POST'])
def create_task():
    request_body = request.get_json()

    if not request_body.get("title") or not request_body.get("description"):
        return jsonify({"details": "Invalid data"}), 400

    new_task = Task.from_dict(request_body)

    db.session.add(new_task)
    db.session.commit()

    return new_task.to_dic(), 201


@tasks_bp.route("", methods=['GET'])
def read_all_tasks():
    sort_query = request.args.get("sort")

    if sort_query == 'asc':
        tasks = Task.query.order_by(Task.title.asc()).all()
    elif sort_query == 'desc':
        tasks = Task.query.order_by(Task.title.desc()).all()
    else:
        tasks = Task.query.all()
    task_response = [task.to_dic()["task"] for task in tasks]
    return jsonify(task_response), 200

@tasks_bp.route("/<task_id>", methods=['GET'])
def read_task_by_id(task_id):
    task = validate_model(Task, task_id)
    return task.to_dic(), 200

@tasks_bp.route("/<task_id>", methods=['PUT'])
def update_task(task_id):
    task = validate_model(Task, task_id)
    request_body = request.get_json()

    task.title = request_body["title"]
    task.description = request_body["description"]

    db.session.commit()

    return task.to_dic(), 200

@tasks_bp.route("/<task_id>/mark_complete", methods=['PATCH'])
def mark_complete_task(task_id):
    task = validate_model(Task, task_id)

    task.completed_at = datetime.utcnow()
    db.session.commit()
    
    message_to_slack = f"Someone just completed the task {task.title}"
    header = {"Authorization": f"Bearer " + os.environ.get('SLACK_BOT_TOKEN')}
    json_response = {
        "channel": "C056ASC5SPQ",
        "text": message_to_slack
        }
    response = requests.post("https://slack.com/api/chat.postMessage", headers=header, json=json_response)
    if response.status_code != 200:
        return make_response({"details": "Failed to send message to Slack"}, 500)

    return task.to_dic(), 200

@tasks_bp.route("/<task_id>/mark_incomplete", methods=['PATCH'])
def mark_incomplete_task(task_id):
    task = validate_model(Task, task_id)

    task.completed_at = None

    db.session.commit()
    return task.to_dic(), 200

@tasks_bp.route("/<task_id>", methods=['DELETE'])
def delete_task(task_id):
    task = validate_model(Task, task_id)

    db.session.delete(task)
    db.session.commit()
    
    return make_response({'details': f'Task {task.task_id} "{task.title}" successfully deleted'}, 200)
