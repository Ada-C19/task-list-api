from flask import Blueprint, abort, jsonify, make_response, request
from app import db
from app.models.task import Task
from app.models.goal import Goal
from datetime import datetime
from dotenv import load_dotenv
import requests
import os


task_bp = Blueprint("task", __name__, url_prefix="/tasks")
goal_bp = Blueprint("goal", __name__, url_prefix="/goals")

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
        slack_bot_token = os.environ.get("SLACK_BOT_TOKEN")
        message = f"Someone just completed the task {task.title}"
        header = {
            "Authorization": f"Bearer {slack_bot_token}"
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

# Goal routes --------------------------------


@goal_bp.route("", methods=["POST"])
def add_goal():
    request_body = request.get_json()
    try:
        new_goal = Goal(
            title = request_body["title"]
        )
    except KeyError:
        return {"details": "Invalid data"}, 400

    db.session.add(new_goal)
    db.session.commit()

    return jsonify(new_goal.to_dict_goal()), 201


def validate_goal(goal_id):
    try:
        goal_id = int(goal_id)
    except ValueError:
        return abort(make_response({"msg": f"invalid goal id: {goal_id}"}, 400))

    return Goal.query.get_or_404(goal_id)

@goal_bp.errorhandler(404)
def not_found(error):
    message_body = {
        "status": 404,
        "error": "Not Found",
        "message": "The requested goal id could not be found."
    }
    return jsonify(message_body), 404


@goal_bp.route("", methods=["GET"])
def get_goals():
    response = []
    all_goals = Goal.query.all()
    for goal in all_goals:
        response.append(goal.to_dict())

    return jsonify(response), 200


@goal_bp.route("/<goal_id>", methods=["GET"])
def get_one_goal(goal_id):
    goal = validate_goal(goal_id)

    return goal.to_dict_goal(), 200


@goal_bp.route("/<goal_id>", methods=["PUT"])
def update_goal(goal_id):
    goal = validate_goal(goal_id)
    request_data = request.get_json()
    goal.title = request_data["title"]

    db.session.commit()

    return goal.to_dict_goal()


@goal_bp.route("/<goal_id>", methods=["DELETE"])
def delete_goal(goal_id):
    goal = validate_goal(goal_id)

    db.session.delete(goal)
    db.session.commit()

    return {"details": f'Goal {goal_id} "{goal.title}" successfully deleted'}, 200