from app import db
from app.models.task import Task
from flask import Blueprint, current_app, jsonify, abort, make_response, request
from sqlalchemy import desc
import requests

tasks_bp = Blueprint("tasks", __name__, url_prefix = "/tasks")

def validate_model(cls, model_id):
    try:
        model_id = int(model_id)
    except:
        abort(make_response({"message":f"{cls.__name__} {model_id} invalid"}, 400))

    model = cls.query.get(model_id)

    if not model:
        abort(make_response({"message":f"{cls.__name__} {model_id} not found"}, 404))

    return model

def send_slack_message_for_completed_task(task_title):    
    slack_api_token = current_app.config["SLACK_API_TOKEN"]
    # slack_api_url = current_app.config["SLACK_API_URL"]
    # slack_channel = current_app.config["SLACK_CHANNEL"]
    slack_api_url = "https://slack.com/api/chat.postMessage"
    slack_channel = "task-notifications"

    headers = {
        "Authorization": f"Bearer {slack_api_token}",
        "Content-type": "application/json"
    }

    request_body = {
        "channel": slack_channel,
        "text" : f"Someone just completed the task {task_title}"
    }

    response_body = requests.post(slack_api_url, headers=headers, json=request_body)
    return response_body


# Gets all Tasks and returns 200
@tasks_bp.route("", methods = ["GET"])
def handle_tasks():

    sort_query = request.args.get("sort")
    tasks = []

    if not sort_query:
        tasks = Task.query.all()    
    elif sort_query == "asc":
        # .order_by by default will sort in asc order
        tasks = Task.query.order_by(Task.title).all()
    elif sort_query == "desc":
        tasks = Task.query.order_by(desc(Task.title)).all()

    task_response = []
    for task in tasks:
        task_response.append(task.to_dict())
    
    return jsonify(task_response), 200

# Gets one task by task_id and returns 200 if found
@tasks_bp.route("/<task_id>", methods = ["GET"])
def handle_task(task_id):
    task = validate_model(Task, task_id)
    
    response_body = task.as_task_dict()

    return jsonify(response_body), 200


# Creates a Task and returns 201 
@tasks_bp.route("", methods = ["POST"])
def create_task():
    request_body = request.get_json()

    if "title" not in request_body or "description" not in request_body:
        return make_response(jsonify({"details" : "Invalid data"}), 400)

    
    new_task = Task.from_dict(request_body)

    db.session.add(new_task)
    db.session.commit()

    response_body = new_task.as_task_dict()

    return make_response(response_body, 201)

# Updates task by task_id and returns 200 
@tasks_bp.route("/<task_id>", methods = ["PUT"])
def update_task(task_id):
    task = validate_model(Task, task_id)

    request_body = request.get_json()

    task.title = request_body["title"]
    task.description = request_body["description"]

    db.session.commit()

    response_body = task.as_task_dict()

    return make_response(jsonify(response_body), 200)

# Deletes a task by task_id and returns 200 
@tasks_bp.route("/<task_id>", methods = ["DELETE"])
def delete_task(task_id):
    task = validate_model(Task, task_id) 

    db.session.delete(task)
    db.session.commit()

    return make_response(jsonify({"details": f"Task {task_id} \"{task.title}\" successfully deleted"}), 200)

# Marks complete on an incompleted or completed task and returns 200
@tasks_bp.route("/<task_id>/mark_complete", methods = ["PATCH"])
def mark_task_complete_on_incompleted_or_completed(task_id):
    task = validate_model(Task, task_id)

    if task.completed_at or not task.completed_at:
        task.mark_as_completed()

    db.session.commit()

    send_slack_message_for_completed_task(task.title)

    response_body = task.as_task_dict()
    return make_response(jsonify(response_body), 200)

# Marks incomplete on a completed task or incompleted task and returns 200
@tasks_bp.route("/<task_id>/mark_incomplete", methods = ["PATCH"])
def mark_task_incomplete_on_completed_or_incompleted(task_id):
    task = validate_model(Task, task_id)
    
    if task.completed_at or not task.completed_at:
        task.completed_at = None
    
    db.session.commit()

    response_body = task.as_task_dict()
    return make_response(jsonify(response_body), 200)



