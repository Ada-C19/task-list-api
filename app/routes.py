from flask import Blueprint, jsonify, request, abort, make_response
from app import db
from app.models.task import Task
from app.models.goal import Goal
from datetime import datetime


# BLUEPRINTS #
task_bp = Blueprint("tasks", __name__, url_prefix = "/tasks")
goal_bp = Blueprint("goals", __name__, url_prefix = "/goals")

# HELPER FUNCTIONS #
def validate_model(cls, model_id):
    # makes sure the data type is an integer
    try: 
        model_id = int(model_id)
    except ValueError:
        abort(make_response({"message": f"{model_id} is not a valid type. A {(type(model_id))} data type was provided. Must be a valid integer data type."},400))
    
    model = cls.query.get(model_id)

    if not model:
        abort(make_response({"message" : f"{cls.__name__} {model_id} does not exist"},404))
    
    return model

# POST METHOD - create a task 
@task_bp.route("", methods = ["POST"])
def create_task():
    request_body = request.get_json()

    try:
        new_task = Task.from_dict(request_body)
    except:
        return jsonify({"details": "Invalid data"}),400
    
    db.session.add(new_task)
    db.session.commit()

    return jsonify({
        "task": {
            "id": new_task.task_id,
            "title": new_task.title,
            "description": new_task.description,
            "is_complete": new_task.is_complete
            }
    }), 201

# GET METHOD - read all task
@task_bp.route("", methods = ["GET"])
def get_all_tasks():
    tasks_response = []

    tasks = Task.query.all()

    for task in tasks:
        tasks_response.append(task.to_dict())

# https://www.programiz.com/python-programming/methods/list/sort
    sort_query = request.args.get("sort")
    if sort_query == "asc":
        tasks_response.sort(key=lambda x: x.get('title'))
    elif sort_query == "desc":
        tasks_response.sort(key=lambda x: x.get('title'), reverse=True)

    return jsonify(tasks_response)



# GET METHOD - read a task by task id
@task_bp.route("/<task_id>", methods = ["GET"])
def get_by_task_id(task_id):
    task = validate_model(Task, task_id)

    return {
        "task": task.to_dict()
        }, 200


# PUT METHOD - update a task by id
@task_bp.route("/<task_id>", methods = ["PUT"])
def update_task(task_id):
    task = validate_model(Task,task_id)

    request_body = request.get_json()

    task.title = request_body["title"]
    task.description = request_body["description"]

    db.session.commit()

    return jsonify({
        "task": {
            "id": task.task_id,
            "title": task.title,
            "description": task.description,
            "is_complete": task.is_complete
            }
        }), 200

# DELETE METHOD - delete a task by id
@task_bp.route("/<task_id>", methods=["DELETE"])
def delete_task(task_id):
    task = validate_model(Task, task_id)

    db.session.delete(task)
    db.session.commit()

    return { "details": f'Task {task_id} "{task.title}" successfully deleted'}


## WAVE 3 - Creating Custom Endpoints 
# PUT METHOD - update is_complete to true
@task_bp.route("/<task_id>/mark_complete", methods = ["PATCH"])
def mark_complete(task_id):
    task = validate_model(Task, task_id)

    task.is_complete = True
    task.completed_at = datetime.utcnow()

    db.session.commit()
    slack_bot_notification(task)

    return {
        "task": task.to_dict()
        }, 200

# PUT METHOD - update is_complete to false
@task_bp.route("/<task_id>/mark_incomplete", methods = ["PATCH"])
def mark_incomplete(task_id):
    task = validate_model(Task, task_id)

    task.is_complete = False
    task.completed_at = None

    db.session.commit()

    return {
        "task": task.to_dict()
        }, 200

# slack bot task completed notification
# https://www.mechanicalgirl.com/post/building-simple-slack-app-using-flask/
# https://api.slack.com/methods/chat.postMessage/test
# https://realpython.com/getting-started-with-the-slack-api-using-python-and-flask/
# https://stackoverflow.com/questions/41546883/what-is-the-use-of-python-dotenv
# https://slack.dev/python-slack-sdk/web/index.html
# https://github.com/SlackAPI/python-slack-sdk

def slack_bot_notification(task):
    from dotenv import load_dotenv
    import os
    
    load_dotenv()
    slack_token= os.environ.get("SLACK_API_KEY")

    from slack_sdk import WebClient
    client = WebClient(token=slack_token)
    # print(slack_token)

    response = client.chat_postMessage(
        channel="C056SCXBCJ3",
        text = f"Someone just completed the task {task.title}" 
        )