from flask import Blueprint, request, jsonify, make_response, abort
from app import db
from app.models.task import Task
from app.models.goal import Goal
import datetime

from dotenv import load_dotenv
import requests 
import os
load_dotenv()


task_bp = Blueprint("tasks", __name__, url_prefix="/tasks")
goal_bp = Blueprint("goals", __name__, url_prefix="/goals")


@task_bp.route("", methods=["POST"])
def add_task():
    request_body = request.get_json()

    if not "title" in request_body or not "description" in request_body:
        abort(make_response({"details": "Invalid data"},400))

    new_task = Task(
        title = request_body["title"],
        description = request_body["description"]
        # completed_at = request_body["completed_at"]
    )
    

    db.session.add(new_task)
    db.session.commit()

    return {"task": new_task.to_result()}, 201


@task_bp.route("", methods=["GET"])
def get_tasks():
    sort = request.args.get("sort")

    if sort == "asc":
        all_tasks = Task.query.order_by(Task.title.asc()).all()
    elif sort == "desc":
        all_tasks = Task.query.order_by(Task.title.desc()).all()
    else:
        all_tasks = Task.query.all()


    response = []
    for task in all_tasks:
        response.append(task.to_result())

    return jsonify(response), 200 


@task_bp.route("/<task_id>", methods=["GET"])
def get_one_task(task_id):
    one_task = validate_item(Task, task_id)

    return make_response({"task": one_task.to_result()})


@task_bp.route("/<task_id>", methods=["PUT"])
def update_task(task_id):
    task = validate_item(Task, task_id)

    request_body = request.get_json()

    task.title = request_body["title"]
    task.description = request_body["description"]

    db.session.commit()

    return make_response({"task": task.to_result()})


@task_bp.route("/<task_id>", methods=["DELETE"])
def delete_task(task_id):
    task = validate_item(Task, task_id)

    db.session.delete(task)
    db.session.commit()

    return make_response({"details": f'Task {task_id} "{task.title}" successfully deleted'})


def validate_item(model, item_id):
    try:
        item_id= int(item_id)
    except ValueError:
        abort(make_response({"message": f"invalid id: {item_id}"}, 400))
    
    task = Task.query.get(item_id)

    if not task:
        abort(make_response({"message": f"Task {item_id} not found."}, 404))

    return task.query.get(item_id)


@task_bp.route("/<task_id>/mark_complete", methods=["PATCH"])
def mark_complete(task_id):
    task = validate_item(Task, task_id)

    task.completed_at = datetime.datetime.now() 

    db.session.commit()

    slack_path = "https://slack.com/api/chat.postMessage"

    bot_info = {
        "token": os.environ.get("SLACK_PERSONAL_TOKEN"),
        "channel": "task-notifications",
        "text": f"Someone just completed the task {task.title}."
    }

    requests.post(slack_path, data=bot_info)


    return make_response({"task": task.to_result()})


@task_bp.route("/<task_id>/mark_incomplete", methods=["PATCH"])
def mark_incomplete(task_id):
    task = validate_item(Task, task_id) 

    task.completed_at = None

    db.session.commit()

    return make_response({"task": task.to_result()})


@goal_bp.route("", methods=["POST"])
def add_goal():
    request_body = request.get_json()

    if not "title" in request_body:
        abort(make_response({"details": "Invalid data"},400))

    new_goal = Goal(
        title = request_body["title"]
    )

    db.session.add(new_goal)
    db.session.commit()

    return {"goal": new_goal.to_result()}, 201

@goal_bp.route("", methods=["GET"])
def get_goals():
    all_goals = Goal.query.all()
    
    response = []

    for goal in all_goals:
        response.append(goal.to_result())
    
    return jsonify(response), 200

