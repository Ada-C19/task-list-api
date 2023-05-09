from flask import Blueprint, make_response, request, jsonify, abort
from app.models.task import Task
from app import db
from sqlalchemy import asc, desc
from datetime import datetime, date
import requests
import json

import os
from dotenv import load_dotenv
load_dotenv()

token = os.environ.get("SLACK_BOT_TOKEN")



tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")

# helper function: validate task
def validate_task(task_id):
    try:
        task_id = int(task_id)
    except:
        abort(make_response({"message": f"{type(task_id)} is not a valid type"}, 400))

    task = Task.query.get(task_id)

    if not task:
        abort(make_response({"message": f"task #{task_id} not found"}, 404))
    
    return task



@tasks_bp.route("", methods=["POST"])
def create_task():
    try:
        request_body = request.get_json()
        new_task = Task(
            title = request_body["title"],
            description =  request_body["description"],
            # completed_at = request_body["completed_at"]
        )

        db.session.add(new_task)
        db.session.commit()

        return make_response({
"task": {
    "id": new_task.task_id,
    "title": new_task.title,
    "description": new_task.description,
    "is_complete": bool(new_task.completed_at)
}
}, 201)

    except KeyError as error:
        abort(make_response({"details": "Invalid data"}, 400))
        # abort(make_response(f"{error.__str__()} is missing", 400))

@tasks_bp.route("", methods=["GET"])
def get_all_tasks():
    # this is the query part
    sort_query = request.args.get("sort")
    # if the user typed in 'asc'
    if sort_query == "asc":
        tasks = Task.query.order_by(asc(Task.title)).all()
    elif sort_query == "desc":
        tasks = Task.query.order_by(desc(Task.title)).all()
    else:
        tasks = Task.query.all()
    
    tasks_response = []

    for task in tasks:
        tasks_response.append(
            {
                "id": task.task_id,
                "title": task.title,
                "description": task.description,
                "is_complete": bool(task.completed_at)
            }
        )
    return jsonify(tasks_response)

@tasks_bp.route("/<task_id>", methods=["GET"])
def get_one_task(task_id):
    task = validate_task(task_id)
    return { "task":{
                "id": task.task_id,
                "title": task.title,
                "description": task.description,
                "is_complete": bool(task.completed_at)}
            }


@tasks_bp.route("/<task_id>", methods=["PUT"])
def update_task(task_id):
    task = validate_task(task_id)

    request_body = request.get_json()

    task.title = request_body["title"]
    # if request_body["title"] else task.title
    task.description = request_body["description"] 
    # if request_body["description"] else task.description
    # task.completed_at = request_body["completed_at"] 
    # if request_body["completed_at"] else task.completed_at

    db.session.commit()
    return {"task": {
                "id": task.task_id,
                "title": task.title,
                "description": task.description,
                "is_complete": bool(task.completed_at)}
            }


@tasks_bp.route("/<task_id>", methods=["DELETE"])
def delete_one_task(task_id):
    task = validate_task(task_id)
    db.session.delete(task)
    db.session.commit()
    return make_response({
        "details": f"Task {task.task_id} \"{task.title}\" successfully deleted"
})

# helper function to send msg to slack
def post_message_to_slack(my_text, blocks = None):
    url = "https://slack.com/api/chat.postMessage"

    payload = json.dumps({
    "channel": "task-notifications",
    "text": my_text
    })
    headers = {
    'Authorization': 'Bearer ' + token,
    'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    print(response.text)


@tasks_bp.route("/<task_id>/mark_complete", methods=["PATCH"])
def mark_off_complete(task_id):
    task = validate_task(task_id)

    time_now = datetime.now()
    todays_date = date.today()
    task.completed_at = todays_date

    db.session.commit()

    # sending to slack???
    text_to_send = f"Someone just completed the task {task.title}"
    post_message_to_slack(text_to_send)

    return {"task": {
                "id": task.task_id,
                "title": task.title,
                "description": task.description,
                "is_complete": bool(task.completed_at)}
            }
        


@tasks_bp.route("/<task_id>/mark_incomplete", methods=["PATCH"])
def mark_incomplete(task_id):
    task = validate_task(task_id)
    task.completed_at = None

    db.session.commit()
    return {"task": {
                "id": task.task_id,
                "title": task.title,
                "description": task.description,
                "is_complete": bool(task.completed_at)}
            }



