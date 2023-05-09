from flask import abort, Blueprint, jsonify, make_response, request
from app import db
from app.models.task import Task
from app.models.goal import Goal
from datetime import datetime, date
import logging
import os
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

task_bp = Blueprint("tasks", __name__, url_prefix="/tasks")
goal_bp = Blueprint("goals", __name__, url_prefix="/goals")

client = WebClient(token=os.environ.get("SLACK_BOT_TOKEN"))
logger = logging.getLogger(__name__)

@task_bp.route("", methods = ["GET"])
def get_tasks():
    response = []
    title_sort_query = request.args.get("sort")

    if title_sort_query is None:
        all_tasks = Task.query.all()
    elif "asc" in title_sort_query: 
        all_tasks = Task.query.order_by(Task.title.asc()).all()
    elif "desc" in title_sort_query:
        all_tasks = Task.query.order_by(Task.title.desc()).all()

    for task in all_tasks:
        response.append(task.to_dict())
    return jsonify(response), 200


@task_bp.route("", methods = ["POST"])
def create_new_task():
    request_body = request.get_json()
    try:
        new_task = Task(
            title = request_body["title"],
            description = request_body["description"]
        )
        db.session.add(new_task)
        db.session.commit()

        result = new_task.to_dict()
        return {"task": new_task.to_dict()}, 201
    except:
        return abort(make_response({"details": "Invalid data"}, 400))


@task_bp.route("/<task_id>", methods = ["GET"])
def get_task_by_id(task_id):
    task = validate_item(Task, task_id)
    if task.goal_id:
        return {"task": task.to_dict_with_goal()}, 200
    else: 
        return {"task": task.to_dict()}, 200


@task_bp.route("/<task_id>", methods = ["PUT"])
def update_one_task(task_id):
    updated_task = validate_item(Task, task_id)

    request_body = request.get_json()
    updated_task.title = request_body["title"],
    updated_task.description = request_body["description"]

    db.session.commit()
    return {"task": updated_task.to_dict()}, 200

@task_bp.route("/<task_id>", methods = ["DELETE"])
def delete_one_task(task_id):
    task = validate_item(Task, task_id)
    
    db.session.delete(task)
    db.session.commit()

    return {"details": f'Task {task_id} "{task.title}" successfully deleted'}, 200

def validate_item(Model, id):
    try:
        valid_id = int(id)
    except:
        return abort(make_response({"message": f"invalid id: {id}"}, 400))
    
    return Model.query.get_or_404(valid_id)
#passes wave one

@task_bp.route("/<task_id>/mark_complete", methods = ["PATCH"])
def mark_task_complete(task_id):
    updated_task = validate_item(Task, task_id)

    updated_task.completed_at = datetime.now()
    db.session.commit()
    
    channel_id = "C056SJEC9D0"
    try:
        # Call the chat.postMessage method using the WebClient
        result = client.chat_postMessage(
            channel=channel_id, 
            text=f"Someone just completed the task {updated_task.title}"
        )
        logger.info(result)

    except SlackApiError as e:
        logger.error(f"Error posting message: {e}")
    return {"task": updated_task.to_dict()}, 200

@task_bp.route("/<task_id>/mark_incomplete", methods = ["PATCH"])
def mark_task_incomplete(task_id):
    updated_task = validate_item(Task, task_id)

    updated_task.completed_at = None
    db.session.commit()
    return {"task": updated_task.to_dict()}, 200

@goal_bp.route("", methods = ["POST"])
def create_goal():
    request_body = request.get_json()
    try:
        new_goal = Goal(
            title = request_body["title"]
        )
        db.session.add(new_goal)
        db.session.commit()

        result = new_goal.to_dict()
        return {"goal": result}, 201
    except:
        return abort(make_response({"details": "Invalid data"}, 400))
    
@goal_bp.route("", methods = ["GET"])
def get_goals():
    response = []
    all_goals = Goal.query.all()
    for goal in all_goals:
        response.append(goal.to_dict())
    return jsonify(response), 200

@goal_bp.route("/<goal_id>", methods = ["GET"])
def get_task_by_id(goal_id):
    goal = validate_item(Goal, goal_id)
    return {"goal": goal.to_dict()}, 200

@goal_bp.route("/<goal_id>", methods = ["PUT"])
def update_one_goal(goal_id):
    updated_goal = validate_item(Goal, goal_id)

    request_body = request.get_json()
    updated_goal.title = request_body["title"]

    db.session.commit()
    return {"goal": updated_goal.to_dict()}, 200

@goal_bp.route("/<goal_id>", methods = ["DELETE"])
def delete_one_goal(goal_id):
    goal = validate_item(Goal, goal_id)
    
    db.session.delete(goal)
    db.session.commit()

    return {"details": f'Goal {goal_id} "{goal.title}" successfully deleted'}, 200

@goal_bp.route("/<goal_id>/tasks", methods= ["POST"])
def post_tasks_under_goal(goal_id):
    goal = validate_item(Goal, goal_id)

    request_body = request.get_json()
    try:
        new_tasks_for_goal = request_body["task_ids"]
        tasks = []
        for task_id in new_tasks_for_goal:
            tasks.append(validate_item(Task, task_id))

        goal.tasks = tasks
            
        db.session.commit()

        return {"id": goal.goal_id, "task_ids": new_tasks_for_goal}, 200
    except:
        return abort(make_response({"details": "Invalid data"}, 400))
# #RETURN TO THIS ROUTE LATER

@goal_bp.route("/<goal_id>/tasks", methods = ["GET"])
def get_tasks_of_one_goal(goal_id):
    goal = validate_item(Goal, goal_id)

    tasks = [task.to_dict_with_goal() for task in goal.tasks]
    return jsonify(goal.to_dict_with_tasks()), 200
