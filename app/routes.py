from app import db
from app.models.task import Task
from app.models.goal import Goal
from flask import Blueprint, jsonify, make_response, request, abort
import datetime
import requests
import os

tasks_bp = Blueprint("task", __name__, url_prefix="/tasks")
goals_bp = Blueprint("goal", __name__, url_prefix="/goals")

def validate_task(model, task_id):
    """Validate that task exists in database before using route."""
    try:
        task_id = int(task_id)
    except:
        abort(make_response({"message": f"Task '{task_id}' invalid"}, 400))

    task = model.query.get(task_id)
    if not task:
        abort(make_response({"message": f"Task '{task_id}' not found"}, 404))

    return task


@tasks_bp.route("", methods=["POST"])
def create_task():
    """Create and add task to database."""
    request_body = request.get_json()

    if "title" not in request_body or "description" not in request_body:
        return {"details": f"Invalid data"}, 400

    new_task = Task.from_dict(request_body)

    db.session.add(new_task)
    db.session.commit()

    return {"task": new_task.to_dict()}, 201

@tasks_bp.route("")


@tasks_bp.route("", methods=["GET"])
def get_all_tasks():
    """Get all tasks and sort by title if specifed."""
    sort_query = request.args.get("sort")

    # Retrieve all tasks, and order by asc or desc if specifed
    if sort_query == "asc":
        all_tasks = Task.query.order_by(Task.title.asc()).all()
    elif sort_query == "desc":
        all_tasks = Task.query.order_by(Task.title.desc()).all()
    else:
        all_tasks = Task.query.all()

    response = [task.to_dict() for task in all_tasks]

    return jsonify(response), 200


@tasks_bp.route("/<task_id>", methods=["GET"])
def get_one_task(task_id):
    """Get one task by id."""
    return {"task": validate_task(Task, task_id).to_dict()}, 200


@tasks_bp.route("/<task_id>", methods=["PUT"])
def update_task(task_id):
    """Updates task specifed by id."""
    task = validate_task(Task, task_id)

    request_body = request.get_json()
    task.title = request_body["title"]
    task.description = request_body["description"]

    db.session.commit()

    return {"task": task.to_dict()}, 200


@tasks_bp.route("/<task_id>/mark_complete", methods=["PATCH"])
def mark_task_as_complete(task_id):
    """Mark task specifed by id as completed and send bot message on Slack."""
    task = validate_task(Task, task_id)

    task.completed_at = datetime.datetime.now()
    task.is_complete = True

    db.session.commit()

    bot_data = {
        "token": os.environ.get("SLACKBOT_API_KEY"),
        "channel": "task-notifications",
        "text": f"'{task.title}' has just been completed! 🥳"
    }

    response = requests.post(url="https://slack.com/api/chat.postMessage", data=bot_data)

    return {"task": task.to_dict()}, 200


@tasks_bp.route("/<task_id>/mark_incomplete", methods=["PATCH"])
def mark_task_as_incomplete(task_id):
    """Mark task specifed by id as incomplete."""
    task = validate_task(Task, task_id)

    task.completed_at = None
    task.is_complete = False

    db.session.commit()

    return {"task": task.to_dict()}, 200


@tasks_bp.route("/<task_id>", methods=["DELETE"])
def delete_task(task_id):
    """Delete task specifed by id."""
    task = validate_task(Task, task_id)

    db.session.delete(task)
    db.session.commit()

    return {"details": f'Task {task.task_id} "{task.title}" successfully deleted'}, 200




################# Goal Routes #################
def validate_goal(model, goal_id):
    """Validate that goal exists in database before using route."""
    try:
        goal_id = int(goal_id)
    except:
        abort(make_response({"message": f"Goal '{goal_id}' invalid"}, 400))

    goal = model.query.get(goal_id)
    if not goal:
        abort(make_response({"message": f"Goal '{goal_id}' not found"}, 404))

    return goal


@goals_bp.route("", methods=["POST"])
def create_goal():
    """Create and add goal to database."""
    request_body = request.get_json()

    if "title" not in request_body:
        return {"details": f"Invalid data"}, 400

    new_goal = Goal.from_dict(request_body)

    db.session.add(new_goal)
    db.session.commit()

    return {"goal": new_goal.to_dict()}, 201


@goals_bp.route("", methods=["GET"])
def get_all_goals():
    """Get all goals."""
    # sort_query = request.args.get("sort")

    # Retrieve all tasks, and order by asc or desc if specifed
    # if sort_query == "asc":
    #     all_tasks = Task.query.order_by(Task.title.asc()).all()
    # elif sort_query == "desc":
    #     all_tasks = Task.query.order_by(Task.title.desc()).all()
    # else:
    #     all_tasks = Task.query.all()
    all_goals = Goal.query.all()

    response = [goal.to_dict() for goal in all_goals]

    return jsonify(response), 200


@goals_bp.route("/<goal_id>", methods=["GET"])
def get_one_goal(goal_id):
    """Get one goal by id."""
    return {"goal": validate_goal(Goal, goal_id).to_dict()}, 200


# @tasks_bp.route("/<task_id>", methods=["PUT"])
# def update_task(task_id):
#     """Updates task specifed by id."""
#     task = validate_model(Task, task_id)

#     request_body = request.get_json()
#     task.title = request_body["title"]
#     task.description = request_body["description"]

#     db.session.commit()

#     return {"task": task.to_dict()}, 200