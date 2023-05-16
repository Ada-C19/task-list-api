from app import db
from flask import Blueprint, jsonify, request, make_response, abort
from app.models.task import Task
from app.models.goal import Goal
from sqlalchemy import text
import datetime
import requests
import os


def post_slack_message(task_title):
    slack_url = "https://slack.com/api/chat.postMessage"
    channel_id = "task-notifications"
    slack_message = f"Someone just completed the task {task_title}"
    headers = dict(
        Authorization = os.environ.get("SLACK_AUTH")
    )
    data = dict(
        channel = channel_id,
        text = slack_message
    )
    response = requests.post(slack_url, headers=headers, data=data)
    return response


tasks_bp = Blueprint("tasks_bp", __name__, url_prefix="/tasks")


@tasks_bp.route("", methods = ["POST"])
def create_task():
    request_body = request.get_json()
    if "title" not in request_body or "description" not in request_body:
# test will not pass if "completed_at" added to the guard clause. Looking over project directions and test, is this intentional?
        return make_response({ "details": "Invalid data"}, 400)
    
    new_task = Task.from_dict(request_body)

    db.session.add(new_task)
    db.session.commit()

    response = {"task" : new_task.to_dict()}
    
    # return
    return make_response(jsonify(response), 201)

@tasks_bp.route("", methods = ["GET"])
def read_all_tasks():
    tasks = Task.query.all()

    sort_query = request.args.get("sort")
    if sort_query == "asc":
        tasks = Task.query.order_by(Task.title.asc()).all()
    elif sort_query == "desc":
        tasks = Task.query.order_by(Task.title.desc()).all()

    tasks_response = []
    if not tasks:
        return jsonify(tasks_response)
    for task in tasks:
        tasks_response.append(
            {
            "id": task.id,
            "title": task.title,
            "description": task.description,
            "is_complete": False
            }
            )
    return jsonify(tasks_response)
    
@tasks_bp.route("/<task_id>", methods =["GET"])
def read_one_task(task_id):
    try:
        task_id = int(task_id)
    except:
        abort(make_response({"message":f"task {task_id} invalid"}, 400))
    
    tasks = Task.query.all()
    for task in tasks:
        if task.id == task_id:
            task_dict = task.to_dict()
            if task.goal_id:
                task_dict["goal_id"] = int(task.goal_id)
            return make_response(jsonify({"task" : task_dict}))
        
    abort(make_response({"message":f"task {task_id} not found"}, 404))

@tasks_bp.route("/<task_id>", methods=["PUT"])
def update_task(task_id):
    request_body = request.get_json()
    try: 
        task_id = int(task_id)
    except:
        abort(make_response({"message":f"task {task_id} invalid"}, 400))
       
    task = Task.query.get(task_id)
    if not task:
        abort(make_response({"message":f"Task {task_id} not found"}, 404))  

    task.title = request_body["title"]
    task.description = request_body["description"]

    db.session.commit()

    return make_response(jsonify({"task" : task.to_dict()}))


@tasks_bp.route("/<task_id>", methods=["DELETE"])
def delete_task(task_id):
    task = Task.query.get(task_id)

    if not task:
        abort(make_response({"message":f"Task {task_id} not found"}, 404))         

    db.session.delete(task)
    db.session.commit()

    response= (f"Task {task_id} \"{task.title}\" successfully deleted")

    return make_response(jsonify({"details": response}))


@tasks_bp.route("/<task_id>/mark_complete", methods=["PATCH"])
def mark_complete(task_id):

    try: 
        task_id = int(task_id)
    except:
        abort(make_response({"message":f"task {task_id} invalid"}, 400))
       
    task = Task.query.get(task_id)
    if not task:
        abort(make_response({"message":f"Task {task_id} not found"}, 404)) 
    
    task.completed_at = datetime.datetime.today()
    task_dict = task.to_dict()
    task_dict["is_complete"] = True

    db.session.commit()

    post_slack_message(task.title)

    return make_response(jsonify({"task" : task_dict}))


@tasks_bp.route("/<task_id>/mark_incomplete", methods=["PATCH"])
def mark_incomplete_incomplete(task_id): 
    request_body = request.get_json()
    try: 
        task_id = int(task_id)
    except:
        abort(make_response({"message":f"task {task_id} invalid"}, 400))
       
    task = Task.query.get(task_id)
    if not task:
        abort(make_response({"message":f"Task {task_id} not found"}, 404)) 

    task = Task.query.get(task_id)

    task.completed_at = None

    db.session.commit()

    task_dict = task.to_dict()
    task_dict["is_complete"] = False

    return make_response(jsonify({"task" : task_dict}))
