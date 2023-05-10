from flask import Blueprint, abort, jsonify, make_response, request
from app import db
from app.models.task import Task
from datetime import datetime
import requests

task_bp = Blueprint("task", __name__, url_prefix="/tasks")

@task_bp.route("", methods=["POST"])
def add_task():
    request_body = request.get_json()
    if "completed_at" not in request_body:
        request_body["completed_at"] = None
    try:
        new_task = Task(
            title = request_body["title"],
            description = request_body["description"],
            completed_at = request_body["completed_at"]
        )
    except KeyError:
        return {"details": "Invalid data"}, 400

    db.session.add(new_task)
    db.session.commit()

    return jsonify(new_task.to_dict_task()), 201


def validate_task(task_id):
    try:
        task_id = int(task_id)
    except ValueError:
        return abort(make_response({"msg": f"invalid task id: {task_id}"}, 400))
    
    return Task.query.get_or_404(task_id)


@task_bp.route("", methods=["GET"])
def get_tasks():
    response = []
    sort_order = request.args.get("sort", None)
    all_tasks = Task.query.all()
    for task in all_tasks:
        response.append(task.to_dict())

    if sort_order == 'asc':
        tasks_sorted = sorted(response, key=lambda d: d['title'])
    elif sort_order == 'desc':
        tasks_sorted = sorted(response, key=lambda d: d['title'], reverse=True)
    else:
        tasks_sorted = response

    return jsonify(tasks_sorted), 200


@task_bp.route("/<task_id>", methods=["GET"])
def get_one_task(task_id):
    task = validate_task(task_id)

    return task.to_dict_task(), 200


@task_bp.route("/<task_id>", methods=["PUT"])
def update_task(task_id):
    task = validate_task(task_id)
    request_data = request.get_json()

    task.title = request_data["title"]
    task.description = request_data["description"]

    db.session.commit()

    return task.to_dict_task()


@task_bp.route("/<task_id>", methods=["DELETE"])
def delete_task(task_id):
    task = validate_task(task_id)

    db.session.delete(task)
    db.session.commit()

    return {"details": f'Task {task_id} "{task.title}" successfully deleted'}


@task_bp.errorhandler(404)
def not_found(error):
    message_body = {
        "status": 404,
        "error": "Not Found",
        "message": "The requested task id could not be found."
    }
    return jsonify(message_body), 404


@task_bp.route("/<task_id>/<action>", methods=["PATCH"])
def complete_or_incomplete(task_id, action):
    task = validate_task(task_id)
    current_datetime = datetime.utcnow()
    task_status = action
    if task_status == "mark_complete":
        task.completed_at = current_datetime
        #send a message to the slack api here
        message = f"Someone just completed the task {task.title}"
        header = {
            "Authorization": "Bearer xoxb-5239032091394-5224524979687-wJSHhKH8K99Wtofamg4TtaAW"
        }
        data_to_send = {
            "channel": "task-notifications",
            "text": message
        }
        response = requests.post("https://slack.com/api/chat.postMessage", headers=header, json=data_to_send)   

    elif task_status == "mark_incomplete":
        task.completed_at = None
    db.session.commit()

    return task.to_dict_task(), 200
