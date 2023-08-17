from flask import abort, Blueprint, jsonify, make_response, request
from sqlalchemy import desc, asc
from app import db
from app.models.task import Task
from app.models.goal import Goal
from datetime import datetime, timezone
import requests
import os

SLACK_API_TOKEN = os.environ.get("SLACK_API_TOKEN")
task_bp = Blueprint("task", __name__, url_prefix="/tasks")
goal_bp = Blueprint("goal", __name__, url_prefix="/goals")



def call_slack_API(title):
    r = requests.post('https://slack.com/api/chat.postMessage', 
                        data={
                            'channel': 'C05N61M2JHG',
                            'text': f'Task {title} was marked complete!'},
                        headers={'Authorization': SLACK_API_TOKEN})
    return None


''' TASK ROUTES '''

@task_bp.route("", methods=["GET"])
def get_all_tasks():
    sort_query = request.args.get("sort")
    if sort_query == "asc":
        tasks = Task.query.order_by(asc(Task.title))
    elif sort_query == "desc":
        tasks = Task.query.order_by(desc(Task.title))
    else:
        tasks = Task.query.all()

    response = []
    for task in tasks:
        response.append(task.to_dict())

    return jsonify(response), 200


@task_bp.route("/<task_id>", methods=["GET"])
def get_one_task(task_id):
    task = Task.query.get_or_404(task_id)
    return {"task": task.to_dict()}, 200


@task_bp.route("", methods=["POST"])
def create_new_task():
    request_body = request.get_json()
    try:
        new_task = Task(
            title=request_body["title"],
            description=request_body["description"]
        )
    except KeyError:
        return {"details": "Invalid data"}, 400
    
    db.session.add(new_task)
    db.session.commit()

    return {"task": new_task.to_dict()}, 201


@task_bp.route("/<task_id>", methods=["PUT"])
def update_one_task(task_id):
    task = Task.query.get_or_404(task_id)
    request_body = request.get_json()

    task.title = request_body["title"]
    task.description = request_body["description"]

    db.session.commit()

    return {"task": task.to_dict()}, 200


@task_bp.route("/<task_id>/mark_complete", methods=["PATCH"])
def mark_complete_one_task(task_id):
    task = Task.query.get_or_404(task_id)

    task.completed_at = datetime.now(timezone.utc)
    call_slack_API(task.title)
    
    db.session.commit()

    return {"task": task.to_dict()}, 200


@task_bp.route("/<task_id>/mark_incomplete", methods=["PATCH"])
def mark_incomplete_one_task(task_id):
    task = Task.query.get_or_404(task_id)

    task.completed_at = None

    db.session.commit()

    return {"task": task.to_dict()}, 200


@task_bp.route("/<task_id>", methods=["DELETE"])
def delete_one_task(task_id):
    task = Task.query.get_or_404(task_id)

    db.session.delete(task)
    db.session.commit()

    return {"details": (f'Task {task.task_id} "{task.title}" '
                        'successfully deleted')}, 200


''' GOAL ROUTES '''
@goal_bp.route("", methods=["POST"])
def create_new_goal():
    request_body = request.get_json()
    try:
        new_goal = Goal(
            title=request_body["title"],
        )
    except KeyError:
        return {"details": "Invalid data"}, 400
    
    db.session.add(new_goal)
    db.session.commit()

    return {"goal": new_goal.to_dict()}, 201


@goal_bp.route("", methods=["GET"])
def get_all_goals():
    sort_query = request.args.get("sort")
    if sort_query == "asc":
        goals = Goal.query.order_by(asc(Goal.title))
    elif sort_query == "desc":
        goals = Goal.query.order_by(desc(Goal.title))
    else:
        goals = Goal.query.all()

    response = []
    for goal in goals:
        response.append(goal.to_dict())

    return jsonify(response), 200


@goal_bp.route("/<goal_id>", methods=["GET"])
def get_one_task(goal_id):
    goal = Goal.query.get_or_404(goal_id)
    return {"goal": goal.to_dict()}, 200