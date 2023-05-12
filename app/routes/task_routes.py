from flask import abort, Blueprint, jsonify, make_response, request
from app import db
from app.models.task import Task
from datetime import datetime
import requests
import logging
import os
slack_token = os.environ.get("SLACK_BOT_TOKEN")
logger = logging.getLogger(__name__)

task_bp = Blueprint("task", __name__, url_prefix="/tasks")

# Add a task
@task_bp.route("", methods=["POST"])
def add_task():
    request_body = request.get_json()
    verify_task_inputs(request_body)
    new_task = Task.from_dict(request_body)

    db.session.add(new_task)
    db.session.commit()

    response_dict = message_for_only_one_task(new_task)

    return make_response(response_dict, 201)

# Get all tasks and the user can determine what the tasks
# should be sorted by using the query params. Accepted sort
# by functions is by ID and by title
@task_bp.route("", methods=["GET"])
def get_tasks():
    sort_query = request.args.get("sort", default=None)
    sort_by_query = request.args.get("sort_by", default="title")

    all_tasks = Task.query.all()

    response_list = [task.to_dict() for task in all_tasks]

    if sort_by_query == "title":
        sort_key = get_title 
    elif sort_by_query == "id":
        sort_key = get_id
    elif sort_by_query:
        abort(make_response({"details": "sort type is not accepted"}, 400))
    if sort_query == "asc":
        response_list.sort(key=sort_key)
    elif sort_query == "desc":
        response_list.sort(reverse=True, key=sort_key)
    elif sort_query:
        abort(make_response({"details": "sort must be ascending or descending"}, 400))

    return jsonify(response_list), 200

# Get the information associated with one task. The User
# identifies the specific task with the id in the URL.
@task_bp.route("/<task_id>", methods=["GET"])
def get_one_task(task_id):
    task = verify_item(Task, task_id)

    response_dict = message_for_only_one_task(task)

    return make_response(response_dict, 200)

# Update the title and description of a task. The User
# identifies the specific task with the id in the URL.
@task_bp.route("/<task_id>", methods=["PUT"])
def update_one_task(task_id):
    task = verify_item(Task, task_id)

    request_body = request.get_json()
    verify_task_inputs(request_body)

    task.title = request_body["title"]
    task.description = request_body["description"]

    db.session.commit()

    response_dict = message_for_only_one_task(task)
    return make_response(response_dict, 200)

# Delete the task completely. The User
# identifies the specific task with the id in the URL.
@task_bp.route("/<task_id>", methods=["DELETE"])
def delete_one_task(task_id):
    task = verify_item(Task, task_id)

    db.session.delete(task)
    db.session.commit()

    return make_response({"details": f"Task {task.task_id} \"{task.title}\" successfully deleted"})

# Update the task, marking it as complete and changing the 
# completed at date to today. The User
# identifies the specific task with the id in the URL.
@task_bp.route("/<task_id>/mark_complete", methods=["PATCH"])
def mark_task_complete(task_id):
    task = verify_item(Task, task_id)
    
    task.completed_at = datetime.now()

    db.session.commit()

    slack_path = "https://slack.com/api/chat.postMessage"
    channel_id = "task-notifications"
    response_text = f"Someone just completed the task {task.title}"

    slack_bot = {"channel": channel_id, "token": slack_token, "text": response_text}

    requests.post(slack_path, data = slack_bot)
    
    response_dict = message_for_only_one_task(task)
    return make_response(response_dict, 200)

# Update the task, marking it as incomplete and changing the 
# completed at date None. The User
# identifies the specific task with the id in the URL.
@task_bp.route("/<task_id>/mark_incomplete", methods=["PATCH"])
def mark_task_incomplete(task_id):
    task = verify_item(Task, task_id)
    
    task.completed_at = None

    db.session.commit()

    response_dict = message_for_only_one_task(task)
    return make_response(response_dict, 200)

# Helper function to verify that the item exists in our database.
def verify_item(model, item_id):
    try: 
        item_id = int(item_id)
    except ValueError:
        abort(make_response({"message": f"Invalid id: {item_id}"}, 400))
    item = model.query.get(item_id)
    if item:
        return item 
    else:
        abort(make_response({"message": f"Item ID not found: {item_id}"}, 404))

# Helper function to verify that the title and description are both included
# in the request body when adding or updating a task.
def verify_task_inputs(request_body):
    if "title" in request_body and "description" in request_body:
        return request_body
    abort(make_response({"details": "Invalid data"}, 400))

# Adding task as a dictionary key and the task (in dictionary form) as
# the value to return back to the vendor. 
def message_for_only_one_task(task):
    if not task.goal_id:
        return {"task": task.to_dict()}
    else:
        return {"task": task.to_dict_with_goal()}

# Get the title for the task
def get_title(task):
    return task["title"]

# Get the id for the task
def get_id(task):
    return task["id"]