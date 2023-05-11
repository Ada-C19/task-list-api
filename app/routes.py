from app import db
from app.models.task import Task
from app.models.goal import Goal
from datetime import datetime
from flask import Blueprint, jsonify, make_response, request, abort
from dotenv import load_dotenv
import os
import requests

load_dotenv()
API_TOKEN = os.environ.get("API_TOKEN")

task_bp = Blueprint("task", __name__, url_prefix="/tasks")
goal_bp = Blueprint("goal", __name__, url_prefix="/goals")

# wave 1 routes
@task_bp.route("", methods=["POST"])
def create_task():
    request_body = request.get_json()
    try:
        new_task = Task(title = request_body["title"],
                        description = request_body["description"])
        
        db.session.add(new_task)
        db.session.commit()

        message  = {
            "task": new_task.to_dict()
        }
        return make_response(message, 201)
    except KeyError as e:
        abort(make_response({"details": "Invalid data"}, 400))

@task_bp.route("", methods=["GET"])
def read_all_tasks():
    sort_query = request.args.get("sort")
    if sort_query == "asc":
        tasks = Task.query.order_by(Task.title)
    elif sort_query == "desc":
        tasks = Task.query.order_by(Task.title.desc())
    else:
        tasks = Task.query.all()

    tasks_response = [task.to_dict() for task in tasks]
    return jsonify(tasks_response)

@task_bp.route("/<task_id>", methods=["GET"])
def get_one_task(task_id):
    task = validate_model(Task, task_id)
    message  = {
            "task": task.to_dict()
        }
    return make_response(message, 200)

@task_bp.route("/<task_id>", methods=["PUT"])
def update_task(task_id):
    task = validate_model(Task, task_id)
    request_body = request.get_json()

    task.title = request_body["title"]
    task.description = request_body["description"]

    db.session.commit()

    message  = {
            "task": task.to_dict()
        }

    return make_response(message, 200)
    
def validate_model(cls, model_id):
    try:
        model_id = int(model_id)
    except:
        abort(make_response({"message":f"{cls.__name__.lower()} {model_id} invalid"}, 400))

    model = cls.query.get(model_id)
    if not model:
        abort(make_response({"message":f"{cls.__name__.lower()} {model_id} not found"}, 404))

    return model
    

@task_bp.route("/<task_id>", methods=["DELETE"])
def delete_task(task_id):
    task = validate_model(Task, task_id)
    
    db.session.delete(task)
    db.session.commit()

    message  = {
            "details": f"Task {task.task_id} \"{task.title}\" successfully deleted"
        }

    return make_response(message, 200)

# wave 3
@task_bp.route("/<task_id>/mark_complete", methods=["PATCH"])
def mark_task_complete(task_id):
    task = validate_model(Task, task_id)

    task.completed_at = datetime.now()

    message  = {
            "task": task.to_dict()
        }
    
    db.session.commit()
    post_to_slack(task.title)
    return make_response(message, 200)

@task_bp.route("/<task_id>/mark_incomplete", methods=["PATCH"])
def mark_task_incomplete(task_id):
    task = validate_model(Task, task_id)

    task.completed_at = None

    message  = {
            "task": task.to_dict()
        }
    
    db.session.commit()
    
    return make_response(message, 200)

# badabingbadabot helper function
def post_to_slack(task_title):
    url = "https://slack.com/api/chat.postMessage"
    headers = {"Authorization": f"Bearer {API_TOKEN}"}
    data = {
        "channel": "api-test-channel",
        "text": f"Someone just completed the task {task_title}"
        }
    response = requests.post(url, headers=headers, data=data)
    return response

# goals routes - wave 5
@goal_bp.route("", methods=["POST"])
def create_goal():
    request_body = request.get_json()
    try:
        new_goal = Goal(title=request_body["title"])
        
        db.session.add(new_goal)
        db.session.commit()

        message  = {
            "goal": new_goal.to_dict()
        }
        return make_response(message, 201)
    except KeyError as e:
        abort(make_response({"details": "Invalid data"}, 400))

@goal_bp.route("", methods=["GET"])
def get_goals():    
    goals = Goal.query.all()
    goals_response = [goal.to_dict() for goal in goals]
    return jsonify(goals_response) 

@goal_bp.route("/<goal_id>", methods=["GET"])
def get_one_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    message  = {
        "goal": goal.to_dict()
        }
    return make_response(message, 200)

@goal_bp.route("/<goal_id>", methods=["PUT"])
def update_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    request_body = request.get_json()

    goal.title = request_body["title"]

    db.session.commit()

    message  = {
        "goal": goal.to_dict()
        }
    return make_response(message, 200)

@goal_bp.route("/<goal_id>", methods=["DELETE"])
def delete_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    
    db.session.delete(goal)
    db.session.commit()

    message  = {
            "details": f"Goal {goal.goal_id} \"{goal.title}\" successfully deleted"
        }

    return make_response(message, 200)

# wave 6 nested routes
@goal_bp.route("/<goal_id>/tasks", methods=["POST"])
def create_tasks_for_goal_assignment(goal_id):
    request_body = request.get_json()
    goal = validate_model(Goal, goal_id)
    task_list = request_body.get("task_ids")

    tasks = []
    for task_id in task_list:
        task = validate_model(Task, task_id)
        task.goal = goal 
        tasks.append(task_id)

    db.session.commit()

    message = {
        "id": goal.goal_id,
        "task_ids": tasks
        }

    return make_response(message, 200)

@goal_bp.route("/<goal_id>/tasks", methods=["GET"])
def get_tasks_of_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    task_list = []
    for task_obj in goal.tasks:
        task = validate_model(Task, task_obj.task_id)
        task_list.append(task.to_dict())

    message = {
        "id": goal.goal_id,
        "title": goal.title,
        "tasks": task_list
    }

    return make_response(message, 200)