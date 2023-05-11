from flask import Blueprint, jsonify, abort, make_response, request
from datetime import date
from app import db
import requests
import os

from app.models.task import Task
from app.models.goal import Goal

def validate_model(cls, model_id):
    try:
        model_id = int(model_id)
    except:
        abort(make_response({"details": f"Invalid data"}, 400))

    model = cls.query.get(model_id)

    if not model:
        abort(make_response({"message": f"Sorry, {cls.__name__} {model_id} does not exist"}, 404))

    return model

# - - - - - - - - - - - - - - - - - #
###~~~--- task model routes ---~~~###
# - - - - - - - - - - - - - - - - - #

task_bp = Blueprint("tasks", __name__, url_prefix="/tasks")

@task_bp.route("", methods=['POST'])

# define a route for creating a task
def create_task():
    request_body = request.get_json()

    try:
        new_task = Task(
            title = request_body["title"],
            description = request_body["description"],
        )
    except:
        abort(make_response({"details": f"Invalid data"}, 400))

    db.session.add(new_task)
    db.session.commit()

    return {"task": new_task.to_dict()}, 201

# define a route for getting all tasks
@task_bp.route("", methods=["GET"])
def read_all_tasks():
    # querries
    title_query = request.args.get("title")
    description_query = request.args.get("description")
    completed_at_query = request.args.get("completed_at")
    sort_query = request.args.get("sort")

    if title_query:
        tasks = Task.query.filter_by(title=title_query)
    
    elif description_query:
        tasks = Task.query.filter_by(description=description_query)
    
    elif completed_at_query:
        tasks = Task.query.filter_by(completed_at=completed_at_query)
    
    elif sort_query:
        if sort_query == 'asc':
            tasks = Task.query.order_by(Task.title).all()
        elif sort_query == 'desc':
            tasks = Task.query.order_by(Task.title.desc()).all()
    
    else:
        tasks = Task.query.all()

    tasks_response = []

    for task in tasks:
        tasks_response.append(task.to_dict())

    return jsonify(tasks_response), 200

@task_bp.route("/<task_id>", methods=["GET"])
def read_one_task(task_id):
    task = validate_model(Task, task_id)

    if task.goal_id:
        return {
        "task": {
            "id": task.task_id,
            "goal_id": task.goal_id,
            "title": task.title,
            "description": task.description,
            "is_complete": True if task.completed_at else False
        }
    }, 200

    return {"task": task.to_dict()}, 200

@task_bp.route("/<task_id>", methods=["PUT"])
def update_task(task_id):
    task = validate_model(Task, task_id)

    request_body = request.get_json()

    task.title = request_body["title"]
    task.description = request_body["description"]

    db.session.commit()

    return {"task": task.to_dict()}, 200


@task_bp.route("/<task_id>/mark_complete", methods=["PATCH"])
def task_mark_complete(task_id):
    task = validate_model(Task, task_id) 

    task.completed_at = date.today()

    db.session.commit()

    key = os.environ.get("key")
    url_path = "https://slack.com/api/chat.postMessage"
    body = {
        "channel": "C056W45DVEH",
        "text": f"Someone just completed the task {task.title}"
    }

    header = {"Authorization": f"Bearer {key}"}

    slack = requests.post(url_path, headers=header, json=body)

    return {"task": task.to_dict()}, 200

@task_bp.route("/<task_id>/mark_incomplete", methods=["PATCH"])
def task_mark_incomplete(task_id):
    task = validate_model(Task, task_id)

    task.completed_at = None

    db.session.commit()

    return {"task": task.to_dict()}, 200

@task_bp.route("/<task_id>", methods=["DELETE"])
def delete_task(task_id):
    task = validate_model(Task, task_id)

    db.session.delete(task)
    db.session.commit()

    return jsonify({"details":f'Task {task.task_id} "{task.title}" successfully deleted'}), 200

# - - - - - - - - - - - - - - - - - #
###~~~--- goal model routes ---~~~###
# - - - - - - - - - - - - - - - - - #

goal_bp = Blueprint("goals", __name__, url_prefix="/goals")

@goal_bp.route("", methods=['POST'])
def create_goal():
    request_body = request.get_json()

    try:
        new_goal = Goal(
            title = request_body["title"])
    except:
        abort(make_response({"details": f"Invalid data"}, 400))

    db.session.add(new_goal)
    db.session.commit()

    return {
        "goal": {
            "id": new_goal.goal_id,
            "title": new_goal.title
            }}, 201

@goal_bp.route("/<goal_id>/tasks", methods=['POST'])
def assign_tasks_to_goal(goal_id):
    request_body = request.get_json()
    response_tasklist = request_body["task_ids"]
    print(response_tasklist)

    goal = validate_model(Goal, goal_id)

    for task_id in response_tasklist:
        single_task = validate_model(Task, task_id)
        
        if single_task:
            goal.tasks.append(single_task)

    db.session.commit()

    return {
        "id": goal.goal_id,
        "task_ids": response_tasklist
        }, 200

@goal_bp.route("/<goal_id>/tasks", methods=['GET'])
def read_goal_tasks(goal_id):
    goal = validate_model(Goal, goal_id)
    tasklist = []

    for task in goal.tasks:
        tasklist.append({
            "id": task.task_id,
            "goal_id": goal.goal_id,
            "title": task.title,
            "description": task.description,
            "is_complete": True if task.completed_at else False
        })
    
    print({
        "id": goal.goal_id,
        "title": goal.title,
        "tasks": tasklist
        })

    return {
        "id": goal.goal_id,
        "title": goal.title,
        "tasks": tasklist
        }, 200

@goal_bp.route("", methods=["GET"])
def read_all_goals():
    # querries
    title_query = request.args.get("title")
    sort_query = request.args.get("sort")

    if title_query:
        goals = Goal.query.filter_by(title=title_query)
    
    elif sort_query:
        if sort_query == 'asc':
            goals = Goal.query.order_by(Goal.title).all()
        elif sort_query == 'desc':
            goals = Goal.query.order_by(Goal.title.desc()).all()
    
    else:
        goals = Goal.query.all()

    goals_response = []

    for goal in goals:
        goals_response.append({
            "id": goal.goal_id,
            "title": goal.title
            })

    return jsonify(goals_response), 200

@goal_bp.route("/<goal_id>", methods=["GET"])
def read_one_goal(goal_id):
    goal = validate_model(Goal, goal_id)

    return {
        "goal": {
            "id": goal.goal_id,
            "title": goal.title
            }}, 200

@goal_bp.route("/<goal_id>", methods=["PUT"])
def update_goal(goal_id):
    goal = validate_model(Goal, goal_id)

    request_body = request.get_json()

    goal.title = request_body["title"]

    db.session.commit()

    return {
        "goal": {
            "id": goal.goal_id,
            "title": goal.title
            }}, 200

@goal_bp.route("/<goal_id>", methods=["DELETE"])
def delete_goal(goal_id):
    goal = validate_model(Goal, goal_id)

    db.session.delete(goal)
    db.session.commit()

    return jsonify({"details":f'Goal {goal.goal_id} \"{goal.title}\" successfully deleted'}), 200