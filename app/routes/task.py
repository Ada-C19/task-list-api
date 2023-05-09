from flask import Blueprint, jsonify, abort, make_response, request
from app.models.task import Task
from app import db
from datetime import date
import requests
import os


SLACK_ENDPOINT = "https://slack.com/api/chat.postMessage"
SLACK_OATH_TOKEN = os.environ.get('SLACK_BOT_USER_OATH_TOKEN')
SLACK_HEADERS = {
    "Authorization": f"Bearer {SLACK_OATH_TOKEN}"
}

tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")


def send_slack_msg(new_data):

    slack_response = requests.post(SLACK_ENDPOINT, headers=SLACK_HEADERS, json=new_data)


# Routes
@tasks_bp.route("", methods=['POST'])
def create_task():
    request_body = request.get_json()
    try:
        new_task = Task(title=request_body["title"], description=request_body["description"], completed_at=None)
    except KeyError:
        return {
            "details": "Invalid data"
            }, 400

    db.session.add(new_task)
    db.session.commit()

    return {"task": new_task.to_dict()}, 201


@tasks_bp.route("", methods=['GET'])
def handle_tasks():
    title_query = request.args.get("title")
    sort_query = request.args.get("sort")
    
    if title_query:
        tasks = Task.query.filter_by(title=title_query)
    elif sort_query == "asc":
        tasks = Task.query.order_by(Task.title)
    elif sort_query == "desc":
        tasks = Task.query.order_by(Task.title.desc())
    else:
        tasks = Task.query.all()
    
    tasks_response = [task.to_dict() for task in tasks]
    return jsonify(tasks_response), 200


@tasks_bp.route("/<task_id>", methods=['GET'])
def handle_task(task_id):
    task = validate_task(task_id)
    return {"task": task.to_dict()}, 200


@tasks_bp.route("/<task_id>", methods=['PUT'])
def update_one_task(task_id):
    request_body = request.get_json()

    task_to_update = validate_task(task_id)

    task_to_update.title = request_body["title"]
    task_to_update.description = request_body["description"]

    db.session.commit()

    return {"task": task_to_update.to_dict()}, 200


@tasks_bp.route("/<task_id>", methods=['DELETE'])
def delete_one_task(task_id):
    task_to_delete = validate_task(task_id)

    db.session.delete(task_to_delete)
    db.session.commit()

    return {
        "details": 
            f'Task {task_to_delete.task_id} "{task_to_delete.title}" successfully deleted'
        }, 200


@tasks_bp.route("/<task_id>/<mark_status>", methods=['PATCH'])
def mark_task(task_id, mark_status):
    task_to_mark = validate_task(task_id)
    
    if mark_status == "mark_complete":
        task_to_mark.completed_at = date.today()
        # Send notification in Slack
        send_slack_msg(
            {
                "channel": "task-notifications",
                "text": f"Someone just completed the task {task_to_mark.title}"
        }
        )
    elif mark_status == "mark_incomplete":
        task_to_mark.completed_at = None

    db.session.commit()

    return {"task": task_to_mark.to_dict()}, 200