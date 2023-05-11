from flask import Blueprint, make_response, request, jsonify, abort
from app.models.task import Task
from app.models.goal import Goal
from app import db
from sqlalchemy import asc, desc
from datetime import datetime, date
import requests
import json
# For Slack Bot
import os
from dotenv import load_dotenv
load_dotenv()
token = os.environ.get("SLACK_BOT_TOKEN")


# Blueprints
tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")
goals_bp = Blueprint("goals", __name__, url_prefix="/goals")


# Helper function: validate model
def validate_model(cls, model_id):
    try:
        model_id = int(model_id)
    except:
        abort(make_response({"message": f"{type(model_id)} is not a valid type"}, 400))

    model = cls.query.get(model_id)

    if not model:
        abort(make_response({"message": f"{cls.__name__} #{model_id} not found"}, 404))
    
    return model


@tasks_bp.route("", methods=["POST"])
def create_task():
    try:
        request_body = request.get_json()
        new_task = Task(
            title = request_body["title"],
            description =  request_body["description"],
            # completed_at = request_body["completed_at"]
        )

        db.session.add(new_task)
        db.session.commit()

        return make_response({
"task": {
    "id": new_task.task_id,
    "title": new_task.title,
    "description": new_task.description,
    "is_complete": bool(new_task.completed_at)
}
}, 201)

    except KeyError as error:
        abort(make_response({"details": "Invalid data"}, 400))
        # abort(make_response(f"{error.__str__()} is missing", 400))


@tasks_bp.route("", methods=["GET"])
def get_all_tasks():
    # this is the query part
    sort_query = request.args.get("sort")
    # if the user typed in 'asc'
    if sort_query == "asc":
        tasks = Task.query.order_by(asc(Task.title)).all()
    elif sort_query == "desc":
        tasks = Task.query.order_by(desc(Task.title)).all()
    else:
        tasks = Task.query.all()
    
    tasks_response = []

    for task in tasks:
        tasks_response.append(
            {
                "id": task.task_id,
                "title": task.title,
                "description": task.description,
                "is_complete": bool(task.completed_at)
            }
        )
    return jsonify(tasks_response)


@tasks_bp.route("/<task_id>", methods=["GET"])
def get_one_task(task_id):
    task = validate_model(Task, task_id)
    return { "task":{
                "id": task.task_id,
                "title": task.title,
                "description": task.description,
                "is_complete": bool(task.completed_at)}
            }


@tasks_bp.route("/<task_id>", methods=["PUT"])
def update_task(task_id):
    task = validate_model(Task, task_id)

    request_body = request.get_json()

    task.title = request_body["title"]
    # if request_body["title"] else task.title
    task.description = request_body["description"] 
    # if request_body["description"] else task.description
    # task.completed_at = request_body["completed_at"] 
    # if request_body["completed_at"] else task.completed_at

    db.session.commit()
    return {"task": {
                "id": task.task_id,
                "title": task.title,
                "description": task.description,
                "is_complete": bool(task.completed_at)}
            }


@tasks_bp.route("/<task_id>", methods=["DELETE"])
def delete_one_task(task_id):
    task = validate_model(Task, task_id)
    db.session.delete(task)
    db.session.commit()
    return make_response({
        "details": f"Task {task.task_id} \"{task.title}\" successfully deleted"
})


# Helper function to send message to Slack
def post_message_to_slack(my_text, blocks = None):
    url = "https://slack.com/api/chat.postMessage"

    payload = json.dumps({
    "channel": "task-notifications",
    "text": my_text
    })
    headers = {
    'Authorization': 'Bearer ' + token,
    'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    print(response.text)


@tasks_bp.route("/<task_id>/mark_complete", methods=["PATCH"])
def mark_off_complete(task_id):
    task = validate_model(Task, task_id)

    time_now = datetime.now()
    todays_date = date.today()
    task.completed_at = todays_date

    db.session.commit()

    # sending message to Slack
    text_to_send = f"Someone just completed the task {task.title}"
    post_message_to_slack(text_to_send)

    return {"task": {
                "id": task.task_id,
                "title": task.title,
                "description": task.description,
                "is_complete": bool(task.completed_at)}
            }        


@tasks_bp.route("/<task_id>/mark_incomplete", methods=["PATCH"])
def mark_incomplete(task_id):
    task = validate_model(Task, task_id)
    task.completed_at = None

    db.session.commit()
    return {"task": {
                "id": task.task_id,
                "title": task.title,
                "description": task.description,
                "is_complete": bool(task.completed_at)}
            }


# goals routes
@goals_bp.route("", methods=["POST"])
def make_new_goal():
    try:
        request_body = request.get_json()
        new_goal = Goal(
            title = request_body["title"]
        )
        db.session.add(new_goal)
        db.session.commit()

        return make_response(
        {"goal": {
            "id": new_goal.goal_id,
            "title": new_goal.title
        }}, 201)

    except KeyError:
        return make_response({"details": "Invalid data"}, 400)



@goals_bp.route("", methods=["GET"])
def get_all_goals():
    goals = Goal.query.all()
    goals_response = []
    for goal in goals:
        goals_response.append({
    "id": goal.goal_id,
    "title": goal.title
        })
    return jsonify(goals_response)


@goals_bp.route("/<goal_id>", methods=["GET"])
def get_one_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    return {
    "goal": {
        "id": goal.goal_id,
        "title": goal.title
    }}


@goals_bp.route("<goal_id>", methods=["PUT"])
def update_goal_title(goal_id):
    goal = validate_model(Goal, goal_id)
    request_body = request.get_json()
    goal.title = request_body["title"]
    return {
    "goal": {
        "id": goal.goal_id,
        "title": goal.title
    }}


@goals_bp.route("/<goal_id>", methods=["DELETE"])
def delete_one_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    db.session.delete(goal)
    db.session.commit()
    return make_response({
        "details": f"Goal {goal.goal_id} \"{goal.title}\" successfully deleted"
})


@goals_bp.route("/<goal_id>/tasks", methods=["POST"])
def assign_tasks_to_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    request_body = request.get_json()
    goal.tasks = request_body["task_ids"]

    db.session.commit()

    return {
    "id": goal.goal_id,
    "task_ids": goal.tasks
    }

