from flask import Blueprint
from app import db
from app.models.task import Task
from flask import Blueprint, make_response, request, abort
from sqlalchemy import text
from datetime import datetime
import os
import requests
from .routes_helper import validate_model

tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")


@tasks_bp.post("")
def create_task():
    request_body = request.get_json()
    try:
        title = request_body["title"]
        description = request_body["description"]
    except KeyError:
        abort(make_response(dict(details="Invalid data"), 400))

    new_task = Task.from_dict(request_body)

    db.session.add(new_task)
    db.session.commit()

    response_body = dict(task=new_task.to_dict())

    return (response_body), 201

@tasks_bp.get("")
def get_all_tasks():
    sort_dir = request.args.get("sort")
    if sort_dir == "asc":
        query = db.select(Task).order_by(Task.title.asc())
    elif sort_dir == "desc":
        query = db.select(Task).order_by(Task.title.desc())
    else:
        query = db.select(Task)

    tasks = db.session.scalars(query)

    tasks_list = [task.to_dict() for task in tasks]

    return (tasks_list), 200


@tasks_bp.get("/<task_id>")
def get_one_task(task_id):
    # task = validate_model(Task, task_id)
    # SELECT * FROM task where task_id = 'task_id'
    query = db.select(Task).where(Task.task_id == task_id)
    task = db.session.scalar(query)
    # task = Task.query.get(task_id) replaced by the above two lines
    if not task:
        abort(make_response(dict(details=f"Unknown Task id: {task_id}"), 404))

    response_body = dict(task=task.to_dict())

    return (response_body), 200


@tasks_bp.put("/<task_id>")
def update_task(task_id):
    request_body = request.get_json()
    # task = Task.query.get(task_id)
    query = db.select(Task).where(Task.task_id == task_id)
    task = db.session.scalar(query)

    if not task:
        abort(make_response(dict(
            details=f"Unkown Task id: {task_id}"),404
        ))
    try:
        task.title = request_body["title"]
        task.description = request_body["description"]
    except KeyError:
        abort(make_response(dict(details="Invalid data"), 400))

    db.session.commit()

    response_body = dict(task=task.to_dict())

    return (response_body), 200


@tasks_bp.delete("/<task_id>")
def delete_task(task_id):
    # task = validate_model(Task, task_id)
    query = db.select(Task).where(Task.task_id == task_id)
    task = db.session.scalar(query)

    if not task:
        abort(make_response(dict(
            details=f"Unknown Task id: {task_id}"), 404
        ))

    db.session.delete(task)
    db.session.commit()

    return make_response({"details": f"Task {task.task_id} \"{task.title}\" successfully deleted"}, '200 OK')


@tasks_bp.patch("/<task_id>/mark_complete")
def mark_complete(task_id):
    # task = validate_model(Task, task_id)
    # task = Task.query.get(task_id)
    query = db.select(Task).where(Task.task_id == task_id)
    task = db.session.scalar(query)

    if not task:
        abort(make_response(dict(details=f"Unknown Task id: {task_id}"), 404))

    if task.completed_at == None:
        task.completed_at = datetime.utcnow()

    db.session.commit()

    URL = "https://slack.com/api/chat.postMessage"
    query_param = {"channel": "task-notification",
                "text": f"Someone just completed the task {task.title}"}
    headers = {"Authorization": os.environ.get("SLACK_BOT_TOKEN")}
    response_bot = requests.post(URL, params=query_param, headers=headers)

    response_body = dict(task=task.to_dict())
    return (response_body), 200


@tasks_bp.patch("/<task_id>/mark_incomplete")
def mark_incomplete(task_id):
    # task = validate_model(Task, task_id)
    # task = Task.query.get(task_id)
    query = db.select(Task).where(Task.task_id == task_id)
    task = db.session.scalar(query)

    if not task:
        abort(make_response(dict(details=f"Unknown Task id: {task_id}"), 404))
    if task.completed_at != None:
        task.completed_at = None

        db.session.commit()

    response_body = dict(task=task.to_dict())

    return (response_body), 200
