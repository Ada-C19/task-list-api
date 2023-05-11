from flask import Blueprint, jsonify, abort, make_response, request
import requests
from app.models.task import Task
from datetime import datetime
from app import db
import os


tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")

#POST /tasks
@tasks_bp.route("", methods=["POST"])
def create_task():
    try:
        request_body = request.get_json()
        new_task = Task.from_dict(request_body)
    except KeyError as err:
        return make_response({"details": "Invalid data"}, 400)

    db.session.add(new_task)
    db.session.commit()

    return jsonify({"task": new_task.to_dict()}), 201
    

#Validate Model
def validate_model(cls, model_id):
    try:
        model_id = int(model_id)
    except:
        abort(make_response({"details": "Invalid data"}, 400))

    task = cls.query.get(model_id)

    if not task:
        message = {"details": "Invalid data"}
        abort(make_response(message, 404))

    return task


#GET /tasks
@tasks_bp.route("", methods=["GET"])
def get_all_tasks():

    sort_query = request.args.get("sort")

    if sort_query == "asc":
        tasks = Task.query.order_by(Task.title)
    
    elif sort_query == "desc":
        tasks = Task.query.order_by(Task.title.desc())

    else:
        tasks = Task.query.all()
    
    tasks_response = []
    for task in tasks:
        tasks_response.append(task.to_dict())

    return jsonify(tasks_response), 200


#GET /tasks/<id>
@tasks_bp.route("/<model_id>", methods=["GET"])
def get_one_task(model_id):
    task = validate_model(Task, model_id)
    if task:
        return {"task": task.to_dict()}, 200
    
    else:
        return {'details': 'Invalid data'}, 404
    

#PUT /tasks/<id>
@tasks_bp.route("<model_id>", methods=["PUT"])
def update_task(model_id):
    try:
        task = validate_model(Task, model_id)
    except:
        return jsonify({"Message": "Invalid id"}), 404

    request_body = request.get_json()

    task.title = request_body["title"]
    task.description = request_body["description"]

    db.session.commit()

    return jsonify({"task": task.to_dict()}), 200


#DELETE /tasks/<id>
@tasks_bp.route("<model_id>", methods=["DELETE"])
def delete_task(model_id):
    task = validate_model(Task, model_id)

    if task is None:
        return {'details': 'Invalid data'}, 404

    db.session.delete(task)
    db.session.commit()

    message = {"details": f"Task 1 \"{task.title}\" successfully deleted"}
    return make_response(message, 200)


#---------------------------------------------
    
    # Send the message to Slack
    # token = os.environ.get('SLACK_API_TOKEN')
    # message = f"Someone just completed the task {new_task.title} My Beautiful Task"
    # slack_message = {
    #     "text": message,
    #     "channel": "api-test-channel",
    #     "token": token 
    # }
    # response = requests.post("https://slack.com/api/chat.postMessage", data=slack_message)


    # db.session.commit()

    # return jsonify({"task": new_task.to_dict(), "slack_response": response.json()}), 200


@tasks_bp.route("<task_id>/mark_complete", methods=["PATCH"])
def mark_task_complete(task_id):
    try:
        new_task = validate_model(Task, task_id)
    except:
        return jsonify({"Message": "Invalid id"}), 404
    
    new_task.completed_at = datetime.utcnow()

    send_slack_message(new_task)

    db.session.commit()

    return jsonify({"task": new_task.to_dict()}), 200


@tasks_bp.route("<task_id>/mark_incomplete", methods=["PATCH"])
def mark_task_incomplete(task_id):
    try:
        new_task = validate_model(Task, task_id)
    except:
        return jsonify({"Message": "Invalid id"}), 404

    new_task.completed_at = None
    
    db.session.commit()

    return jsonify({"task": new_task.to_dict()}), 200



def send_slack_message(completed_task):
    TOKEN = os.environ['SLACK_API_TOKEN']
    AUTH_HEADERS = {
        "Authorization": f"Bearer {TOKEN}"
    }
    CHANNEL_ID = "C0561UUDX4K"
    SLACK_URL = "https://slack.com/api/chat.postMessage"
    try:
        message = f"Someone just completed the task {completed_task.title}"
        payload = {
            "channel": CHANNEL_ID,
            "text": message
            }
    
        requests.post(SLACK_URL, data = payload, headers = AUTH_HEADERS)
        # r.json()
        # return make_response(r.json(), 201)
    
    except:
        print("There was an error making the call to Slack")



# @tasks_bp.route("<model_id>/mark_complete", methods=["PATCH"])
# def mark_task_complete(model_id):
#     try:
#         new_task = validate_model(Task, model_id)
#     except:
#         return jsonify({"Message": "Invalid id"}), 404

#     new_task.completed_at = datetime.utcnow()

#     db.session.commit()

#     return jsonify({"task": new_task.to_dict()}), 200
