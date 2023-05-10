import os
import requests
from app import db
from app.models.task import Task
from flask import Blueprint, jsonify, abort, make_response, request
from datetime import datetime
from sqlalchemy.sql import func

tasks_bp = Blueprint("tasks_bp", __name__, url_prefix="/tasks")

def validate_model(cls, model_id):
    try:
        model_id = int(model_id)
    except:
        abort(make_response({"message":f"{cls.__name__} {model_id} invalid"}, 400))

    model = cls.query.get(model_id)

    if not model:
        abort(make_response({"message":f"{cls.__name__} {model_id} not found"}, 404))

    return model


'''
Task CRUD Routes
'''
@tasks_bp.route("", methods=["POST"])
def create_task():
    request_body = request.get_json()
    if ("title" not in request_body) or ("description" not in request_body):
        return make_response({"details": "Invalid data"}, 400)
    
    new_task = Task.from_dict(request_body)
        
    db.session.add(new_task)
    db.session.commit()

    return make_response({"task": new_task.response_dict()}, 201)


@tasks_bp.route("", methods=["GET"])
def read_all_tasks():
    title_query = request.args.get("title")
    sort_query = request.args.get("sort")

    if title_query:
        tasks = Task.query.filter(Task.title.ilike(title_query.strip()+'%'))
    elif sort_query == "asc":
        tasks = Task.query.order_by(Task.title.asc())
    elif sort_query == "desc":
        tasks = Task.query.order_by(Task.title.desc())
    else:
        tasks = Task.query.all()

    tasks_response = [task.response_dict() for task in tasks]

    return jsonify(tasks_response)


@tasks_bp.route("/<task_id>", methods=["GET"])
def get_task(task_id):
    task = validate_model(Task, task_id)
    return make_response({"task": task.response_dict()}, 200)


@tasks_bp.route("/<task_id>", methods=["PUT"])
def update_task(task_id):
    task = validate_model(Task, task_id)
    if task is None:
        return make_response({'message': f'Task {task.id} not found'}, 404)

    form_data = request.get_json()
    task.title = form_data["title"]
    task.description = form_data["description"]

    db.session.commit()
    return make_response({"task": task.response_dict()}, 200)

'''
Slack API - Message
'''
def slack_message_complete(message):
    url = 'https://slack.com/api/chat.postMessage'
    headers = {
        "Authorization": f"Bearer {os.environ.get('SLACK_TOKEN')}"
    }
    params = {'channel': "task-notifications",
              'text': message}

    print("sending message")
    message = requests.post(url, data=params, headers=headers)
    return message.json()

@tasks_bp.route("/<task_id>/mark_complete", methods=["PATCH"])
def mark_complete(task_id):
    task = validate_model(Task, task_id)
    
    if request.method == "PATCH":
        task = Task.query.get(task_id)

        if task is None:
            return make_response({"message":f"Task {task_id} not found"}, 404)
        
        # task.completed_at = datetime.today()
        task.completed_at = func.now()
        slack_message_complete(f"Congratulations! You've just completed the task '{task.title}'!")

        db.session.commit()

        return make_response({"task": task.response_dict()}, 200)
    
@tasks_bp.route("/<task_id>/mark_incomplete", methods=["PATCH"])
def mark_incomplete(task_id):
    task = validate_model(Task, task_id)

    if request.method == "PATCH":
        task = Task.query.get(task_id)

        if task is None:
            return make_response({"message":f"Task {task_id} not found"}, 404)
        
        task.completed_at = None

        db.session.commit()
        return make_response({"task": task.response_dict()}, 200)
    

@tasks_bp.route("/<task_id>", methods=["DELETE"])
def delete_task(task_id):
    task = Task.query.get(task_id)
    if task is None:
        return make_response({"message":f"Task {task_id} not found"}, 404)
    task = validate_model(Task, task_id)

    db.session.delete(task)
    db.session.commit()

    return make_response({'details' : f'Task {task.id} "{task.title}" successfully deleted'})