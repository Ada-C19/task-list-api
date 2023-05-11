from flask import Blueprint, jsonify, abort, make_response, request
from app.models.task import Task
from app import db
from sqlalchemy import asc, desc
# from .helper_functions import get_task_instance, get_task_by_id, update_task_from_request
from datetime import timezone, datetime
import os
from dotenv import load_dotenv
import requests

from .helper_functions import create_instance, get_all_instances, get_one_instance


load_dotenv()

NOWTIME = datetime.now(timezone.utc)
SLACK_TOKEN = os.environ.get("SLACK_TOKEN")

tasks_bp = Blueprint('tasks', __name__, url_prefix='/tasks')

@tasks_bp.route("", methods=['POST'])
def create_task():
    return create_instance(Task)

# @tasks_bp.route("", methods=['POST'])
# def create_task():
#     new_task = get_task_instance(request)

#     db.session.add(new_task)
#     db.session.commit()

#     task = new_task.to_json()

#     return make_response(jsonify(task=task)), 201





@tasks_bp.route("", methods=['GET'])
def get_tasks():
    return get_all_instances(Task)

# @tasks_bp.route("", methods=['GET'])
# def get_tasks():
#     sort_order = request.args.get("sort", None)

#     tasks = Task.query

#     title_query = request.args.get("title")
#     if title_query:
#         tasks = tasks.filter_by(title=title_query)

#     if sort_order == "asc":
#         tasks = tasks.order_by(asc(Task.title))
#     elif sort_order == "desc":
#         tasks = tasks.order_by(desc(Task.title))

#     tasks = tasks.all()

#     task_list = [task.to_json() for task in tasks]

#     return jsonify(task_list), 200





@tasks_bp.route("/<task_id>", methods=['GET'])
def get_one_task(task_id):
    return get_one_instance(Task, task_id)

# @tasks_bp.route("/<task_id>", methods=['GET'])
# def get_one_task(task_id):
#     task = get_task_by_id(task_id)
#     return make_response(jsonify({"task": task.to_json()})), 200

# @tasks_bp.route("/<task_id>", methods=['PUT'])
# def update_task(task_id):
#     task = get_task_by_id(task_id)
#     updated_task = update_task_from_request(task, request)

#     db.session.commit()

#     task = updated_task.to_json()

#     return make_response(jsonify(task=task)), 200

# @tasks_bp.route("/<task_id>", methods=['DELETE'])
# def delete_task(task_id):
#     task = get_task_by_id(task_id)

#     db.session.delete(task)
#     db.session.commit()

#     message = f'Task {task_id} "{task.title}" successfully deleted'

#     return make_response({"details" : message}), 200

# # @tasks_bp.route("/<task_id>/mark_complete", methods=['PATCH'])
# # def mark_task_completed(task_id):
# #     task = get_task_by_id(task_id)

# #     task.completed_at = NOWTIME

# #     db.session.commit()

# #     task = task.to_json()
# #     task["is_complete"] = True

# #     return make_response(jsonify(task=task)), 200


# @tasks_bp.route("/<task_id>/mark_complete", methods=['PATCH'])
# def mark_task_completed(task_id):
#     task = get_task_by_id(task_id)

#     task.completed_at = NOWTIME

#     db.session.commit()


#     path = "https://slack.com/api/chat.postMessage"

#     request_body = {
#         "channel": "C0561UUDX4K",
#         "text": f"Someone just completed the task {task.title}"
#     }
#     request_headers = {
#         "Authorization": f"Bearer " + SLACK_TOKEN
#     }

#     response = requests.post(path, json=request_body, headers=request_headers)
    
#     task = task.to_json()
#     task["is_complete"] = True

#     return make_response(jsonify(task=task)), 200



# @tasks_bp.route("/<task_id>/mark_incomplete", methods=['PATCH'])
# def mark_task_incomplete(task_id):
#     task = get_task_by_id(task_id)

#     task.completed_at = None

#     db.session.commit()

#     task = task.to_json()
#     task["is_complete"] = False

#     return make_response(jsonify(task=task)), 200
