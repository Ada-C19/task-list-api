from app import db
from flask import Blueprint, request, make_response, jsonify, abort
from app.models.task import Task
import datetime, requests, json, os


tasks_bp = Blueprint("tasks_bp", __name__, url_prefix="/tasks")

# HELPER FUNCTION
def validate_model(cls, model_id):
    try:
        model_id = int(model_id)
    except: 
        abort(make_response({"message":f"task {model_id} invalid"}, 400))
    
    model = cls.query.get(model_id)

    if not model:
        abort(make_response({"message":f"task {model_id} not found"}, 404))

    return model

def slack_api(task):

    url = "https://slack.com/api/chat.postMessage"
    token = os.environ.get("SLACKBOT_TOKEN_API")

    headers = {"Authorization": f"Bearer {token}"}
    params = {"channel": "#api-test-channel", "text": f"Someone just completed the task {task.title}"}


    response = requests.post(url, headers=headers, params=params)
    return response.json

# CREATES NEW TASKS
@tasks_bp.route("", methods=["POST"])
def create_new_task():
    try: 
        request_body = request.get_json()
        new_task = Task.from_dict(request_body)
    
    except:
        return make_response({"details": "Invalid data"}), 400


    db.session.add(new_task)
    db.session.commit()

    return make_response({"task":new_task.to_dict()}), 201


# READS ALL TASKS
@tasks_bp.route("", methods=["GET"])
def read_all_tasks():
    
    sort_param = request.args.get("sort")

    if sort_param == "asc":
        tasks = Task.query.order_by(Task.title.asc()).all()
        
    elif sort_param == "desc":
        tasks = Task.query.order_by(Task.title.desc()).all()
    
    else:
        tasks = Task.query.all()

    tasks_response = []
    
    for task in tasks:
        tasks_response.append(task.to_dict())

    return jsonify(tasks_response), 200

# READS ONE TASK
@tasks_bp.route("/<task_id>", methods=["GET"])
def read_one_task(task_id):
    task = validate_model(Task, task_id)
    
    return {"task": task.to_dict()}, 200
    

# UPDATES ONE TASK
@tasks_bp.route("/<task_id>", methods=["PUT"])
def update_one_task(task_id):
    task = validate_model(Task, task_id)

    request_body = request.get_json()

    task.title = request_body["title"]
    task.description = request_body["description"]

    db.session.commit()

    return make_response({"task": task.to_dict()}), 200


# UPDATES ALL FIELDS OF TASK
@tasks_bp.route("/<task_id>/mark_complete", methods=["PATCH"])
def update_mark_complete(task_id):
    task = validate_model(Task, task_id)
    slack_message = slack_api(task)

    task.completed_at = datetime.datetime.now()
    
    db.session.commit()

    return make_response({"task": task.to_dict()}), 200

@tasks_bp.route("/<task_id>/mark_incomplete", methods=["PATCH"])
def update_mark_incomplete(task_id):
    task = validate_model(Task, task_id)

    task.completed_at = None
    db.session.commit()
    return make_response({"task": task.to_dict()}), 200

# DELETES ONE TASK
@tasks_bp.route("/<task_id>", methods=["DELETE"])
def delete_one_task(task_id):
    task = validate_model(Task, task_id)

    db.session.delete(task)
    db.session.commit()

    return make_response(jsonify({"details": f"Task {task.task_id} \"{task.title}\" successfully deleted"}))
                         
