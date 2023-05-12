from flask import Blueprint, jsonify, abort, make_response, request
from app.models.task import Task
from app import db
# from .helper_functions import get_task_instance, get_task_by_id, update_task_from_request
from datetime import timezone, datetime
import os
from dotenv import load_dotenv
import requests

from .helper_functions import create_instance, get_all_instances, get_one_instance, update_instance, delete_instance, make_instance_complete, make_instance_incomplete

load_dotenv()



tasks_bp = Blueprint('tasks', __name__, url_prefix='/tasks')

@tasks_bp.route("", methods=['POST'])
def create_task():
    return create_instance(Task)


@tasks_bp.route("", methods=['GET'])
def get_tasks():
    return get_all_instances(Task)


@tasks_bp.route("/<task_id>", methods=['GET'])
def get_one_task(task_id):
    return get_one_instance(Task, task_id)


@tasks_bp.route("/<task_id>", methods=['PUT'])
def update_task(task_id):
    return update_instance(Task, task_id)


@tasks_bp.route("/<task_id>", methods=['DELETE'])
def delete_task(task_id):
    return delete_instance(Task, task_id)


@tasks_bp.route("/<task_id>/mark_complete", methods=['PATCH'])
def mark_task_completed(task_id):
    return make_instance_complete(Task, task_id)


@tasks_bp.route("/<task_id>/mark_incomplete", methods=['PATCH'])
def mark_task_incomplete(task_id):
    return make_instance_incomplete(Task, task_id)





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




