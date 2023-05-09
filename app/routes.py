from app import db
from app.models.task import Task
from app.models.goal import Goal
from flask import Blueprint, jsonify, make_response, request, abort
import datetime
import requests
import os

tasks_bp = Blueprint("task", __name__, url_prefix="/tasks")
goals_bp = Blueprint("goal", __name__, url_prefix="/goals")

def validate_item(model, item_id):
    """Validate that item of model exists in database before using route."""
    try:
        item_id = int(item_id)
    except:
        abort(make_response({"message": f"ID '{item_id}' invalid"}, 400))

    item = model.query.get(item_id)
    if not item:
        abort(make_response({"message": f"ID '{item_id}' not found"}, 404))

    return item


@tasks_bp.route("", methods=["POST"])
def create_task():
    """Create and add task to database."""
    request_body = request.get_json()

    if "title" not in request_body or "description" not in request_body:
        return {"details": "Invalid data"}, 400

    new_task = Task.from_dict(request_body)

    db.session.add(new_task)
    db.session.commit()

    return {"task": new_task.to_dict()}, 201


@tasks_bp.route("", methods=["GET"])
def get_all_tasks():
    """Get all tasks and sort by title if specifed."""
    sort_query = request.args.get("sort")

    # Order by asc or desc if specifed
    if sort_query == "asc":
        all_tasks = Task.query.order_by(Task.title.asc())
    elif sort_query == "desc":
        all_tasks = Task.query.order_by(Task.title.desc())
    else:
        all_tasks = Task.query.all()

    response = [task.to_dict() for task in all_tasks]

    return jsonify(response), 200


@tasks_bp.route("/<task_id>", methods=["GET"])
def get_one_task(task_id):
    """Get one task by id."""
    task = validate_item(Task, task_id)

    if task.goal_id:
        return {"task": task.to_dict_with_goal()}, 200

    return {"task": task.to_dict()}, 200


@tasks_bp.route("/<task_id>", methods=["PUT"])
def update_task(task_id):
    """Updates task specifed by id."""
    task = validate_item(Task, task_id)

    request_body = request.get_json()
    task.title = request_body["title"]
    task.description = request_body["description"]

    db.session.commit()

    return {"task": task.to_dict()}, 200


@tasks_bp.route("/<task_id>/mark_complete", methods=["PATCH"])
def mark_task_as_complete(task_id):
    """Mark task specifed by id as completed and send bot message on Slack."""
    task = validate_item(Task, task_id)

    task.completed_at = datetime.datetime.now()

    db.session.commit()

    bot_data = {
        "token": os.environ.get("SLACKBOT_API_KEY"),
        "channel": "task-notifications",
        "text": f"'{task.title}' has just been completed! 🥳"
    }

    requests.post(url="https://slack.com/api/chat.postMessage", data=bot_data)

    return {"task": task.to_dict()}, 200


@tasks_bp.route("/<task_id>/mark_incomplete", methods=["PATCH"])
def mark_task_as_incomplete(task_id):
    """Mark task specifed by id as incomplete."""
    task = validate_item(Task, task_id)

    task.completed_at = None

    db.session.commit()

    return {"task": task.to_dict()}, 200


@tasks_bp.route("/<task_id>", methods=["DELETE"])
def delete_task(task_id):
    """Delete task specifed by id."""
    task = validate_item(Task, task_id)

    db.session.delete(task)
    db.session.commit()

    return {"details": f'Task {task.task_id} "{task.title}" successfully deleted'}, 200


################# Goal Routes #################
@goals_bp.route("", methods=["POST"])
def add_goal():
    """Create and add goal to database."""
    request_body = request.get_json()

    if "title" not in request_body:
        return {"details": "Invalid data"}, 400

    new_goal = Goal.from_dict(request_body)

    db.session.add(new_goal)
    db.session.commit()

    return {"goal": new_goal.to_dict()}, 201


@goals_bp.route("", methods=["GET"])
def get_all_goals():
    """Get all goals."""
    all_goals = Goal.query.all()

    response = [goal.to_dict() for goal in all_goals]

    return jsonify(response), 200


@goals_bp.route("/<goal_id>", methods=["GET"])
def get_one_goal(goal_id):
    """Get one goal by id."""
    return {"goal": validate_item(Goal, goal_id).to_dict()}, 200


@goals_bp.route("/<goal_id>", methods=["PUT"])
def update_goal(goal_id):
    """Updates goal specifed by id."""
    goal = validate_item(Goal, goal_id)

    request_body = request.get_json()
    goal.title = request_body["title"]

    db.session.commit()

    return {"goal": goal.to_dict()}, 200


@goals_bp.route("/<goal_id>", methods=["DELETE"])
def delete_goal(goal_id):
    """Delete goal specifed by id."""
    goal = validate_item(Goal, goal_id)

    db.session.delete(goal)
    db.session.commit()

    return {"details": f'Goal {goal.goal_id} "{goal.title}" successfully deleted'}, 200


@goals_bp.route("/<goal_id>/tasks", methods=["GET"])
def get_all_tasks_of_goal(goal_id):
    """Get all tasks of a goal via goal id."""
    goal = validate_item(Goal, goal_id)

    response = [task.to_dict_with_goal() for task in goal.tasks]

    return jsonify({
        "id": goal.goal_id,
        "title": goal.title,
        "tasks": response
    }), 200


@goals_bp.route("/<goal_id>/tasks", methods=["POST"])
def associate_goal_to_tasks(goal_id):
    """Associate goal to tasks."""
    goal = validate_item(Goal, goal_id)

    request_body = request.get_json()

    task_ids = request_body.get("task_ids")
    for task_id in task_ids:
        task = Task.query.get(task_id)
        task.goal = goal

    db.session.commit()

    return {
        "id": goal.goal_id,
        "task_ids": task_ids
    }, 200
