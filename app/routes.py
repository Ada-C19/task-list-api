from flask import Blueprint, request, make_response, request, abort, jsonify 
from app import db
from app.models.task import Task
from app.models.goal import Goal
# from sqlalchemy import asc, desc
from datetime import datetime
#to call slack api?:
from dotenv import load_dotenv
import requests 
import os
load_dotenv()

# Blueprints:
tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")
goals_bp = Blueprint("goals", __name__, url_prefix="/goals")

@tasks_bp.route("", methods=["POST"])
def add_task():
    request_body = request.get_json()
    # if "title" not in request_body or "description" not in request_body :
    if not "title" in request_body or not "description" in request_body:
        return make_response({"details": "Invalid data"}, 400)
        # abort(make_response({"details": "Invalid data"}, 400))

    #Replacing this with the from_dict in task.py
    # new_task = Task(
    #         title= request_body["title"],
    #         description= request_body['description'],
    #         completed_at= request_body['completed_at']
    #     )
    new_task = Task.from_dict(request_body)

    
    db.session.add(new_task)
    db.session.commit()

    return {"task": new_task.to_dict()}, 201

@tasks_bp.route("", methods=["GET"])
def get_all_tasks():
    tasks_response = []

    ### Creating the query Params######
    sort_query = request.args.get("sort")
    if sort_query == "asc":
        total_tasks = Task.query.order_by(Task.title.asc()).all()
    elif sort_query == "desc":
        total_tasks = Task.query.order_by(Task.title.desc()).all()
    else:
    ####End of Query#############
        total_tasks = Task.query.all()
    
    for task in total_tasks:
        # tasks_response.append({
        #     "id": task.task_id,
        #     "title": task.title,
        #     "description": task.description,
        #     "is_complete": False
        # })
        tasks_response.append(task.to_dict())
    return jsonify(tasks_response), 200

@tasks_bp.route("/<task_id>", methods=['GET'])
def read_one_task(task_id):
    # task = Task.query.get(task_id)
    # task = validate_item(task_id)
    task = validate_model(Task, task_id)

    # is_complete = False
    # if task.completed_at:
        # is_complete = True

    # return {"task":{
    #     "id": task.task_id, 
    #     "title": task.title,
    #     "description": task.description,
    #     # "is_complete": False
    #     "is_complete": is_complete
    # }
    # }, 200
    return {"task": task.to_dict()}, 200

@tasks_bp.route("/<task_id>", methods=["PUT"])
def update_task(task_id):
    # task = Task.query.get(task_id)
    # task = validate_item(task_id)
    task = validate_model(Task, task_id)

    request_body = request.get_json()

    task.title = request_body["title"]
    task.description = request_body["description"]


    db.session.commit()

    is_complete = False
    if task.completed_at:
        is_complete = True

    return {"task":{
        "id": task.task_id, 
        "title": task.title,
        "description": task.description,
        # "is_complete": False,
        "is_complete": is_complete
    }
    }, 200

######GET CLARIFICATION ON THE RETURN MESSAGE
@tasks_bp.route("/<task_id>", methods=["DELETE"])
def delete_task(task_id):
    # task = Task.query.get(task_id)
    # task = validate_item(task_id)
    task = validate_model(Task, task_id)

    db.session.delete(task)
    db.session.commit()

# return {
#   "details": "Task 1 \"Go on my daily walk 🏞\" successfully deleted"
# },
#make response returnse a status code 200
# return make_response({
#     "details": "Task {task.task_id}"
# })

    # return make_response(f"Task {task.task_id} successfully deleted")
    return {
        "details": f'Task {task_id} \"{task.title}\" successfully deleted'
    }, 200
    
# Working validation
# def validate_item(task_id):
#     try:
#         task_id = int(task_id)
#     except:
#         abort(make_response({"message": f"invalid task_id: {task_id}"}, 400))
    
#     task = Task.query.get(task_id)

#     if not task:
#         abort(make_response({"message": f"task {task_id} not found"}, 404))

#     return task

def validate_model(cls, model_id):
    try:
        model_id = int(model_id)
    except:
        abort(make_response({"message": f"{cls.__name__} {model_id} invalid"}, 400))
    
    model = cls.query.get(model_id)

    if not model:
        abort(make_response({"message": f"{cls.__name__} {model_id} not found"}, 404))

    return model

@tasks_bp.route("/<task_id>/mark_complete", methods=["PATCH"])
def mark_complete_task(task_id):
    # task = validate_item(task_id)
    task = validate_model(Task, task_id)

    task.completed_at = datetime.now()

    db.session.commit()

    is_complete = True

    # Calling the Slack API
    ana_bot = {
        "token": os.environ.get("SLACKBOT_TOKEN_API"),
        "channel": "task-notifications",
        "text": f"Someone just completed the task {task.title} :clap:"
    }

    requests.post(url="https://slack.com/api/chat.postMessage", data = ana_bot)
    # End of Slack API call

    return {"task":{
        "id": task.task_id, 
        "title": task.title,
        "description": task.description,
        "is_complete": is_complete
    }
    }, 200

@tasks_bp.route("/<task_id>/mark_incomplete", methods=["PATCH"])
def mark_incomplete_task(task_id):
    # task = validate_item(task_id)
    task = validate_model(Task, task_id)

    task.completed_at = None

    db.session.commit()

    is_complete = False 

    return {"task":{
        "id": task.task_id, 
        "title": task.title,
        "description": task.description,
        "is_complete": is_complete
    }
    }, 200

# CRUD for Goals
# @goals_bp.route("", methods=["POST"])
# def add_goal():
#     request_body = request.get_json()
#     new_goal = 