from app import db
from app.models.task import Task
from flask import Blueprint, jsonify, abort, make_response, request

tasks_bp = Blueprint("tasks", __name__, url_prefix = "/tasks")

def validate_model(cls, model_id):
    try:
        model_id = int(model_id)
    except:
        abort(make_response({"message":f"{cls.__name__} {model_id} invalid"}, 400))

    model = cls.query.get(model_id)

    if not model:
        abort(make_response({"message":f"{cls.__name__} {model_id} not found"}, 404))

    return model


# Gets all Tasks and returns 200
@tasks_bp.route("", methods = ["GET"])
def handle_tasks():

    task_response = []
    tasks = Task.query.all()
    for task in tasks:
        task_response.append(task.to_dict())
    
    return jsonify(task_response), 200

# Gets one task by task_id and returns 200 if found
@tasks_bp.route("/<task_id>", methods = ["GET"])
def handle_task(task_id):
    task = validate_model(Task, task_id)
    
    response_body = task.as_task_dict()

    return jsonify(response_body), 200


# Creates a Task and returns 201 
@tasks_bp.route("", methods = ["POST"])
def create_task():
    request_body = request.get_json()

    if "title" not in request_body or "description" not in request_body:
        return make_response(jsonify({"details" : "Invalid data"}), 400)

    
    new_task = Task.from_dict(request_body)

    db.session.add(new_task)
    db.session.commit()

    response_body = new_task.as_task_dict()

    return make_response(response_body, 201)

# Updates task by task_id and returns 200 
@tasks_bp.route("/<task_id>", methods = ["PUT"])
def update_task(task_id):
    task = validate_model(Task, task_id)

    request_body = request.get_json()

    task.title = request_body["title"]
    task.description = request_body["description"]

    db.session.commit()

    response_body = task.as_task_dict()

    return make_response(jsonify(response_body), 200)

# Deletes a task by task_id and returns 200 
@tasks_bp.route("/<task_id>", methods = ["DELETE"])
def delete_task(task_id):
    task = validate_model(Task, task_id) 

    db.session.delete(task)
    db.session.commit()

    return make_response(jsonify({"details": f"Task {task_id} \"{task.title}\" successfully deleted"}), 200)