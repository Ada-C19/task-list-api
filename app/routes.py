from app import db
from flask import Blueprint, request, make_response, jsonify
from app.models.task import Task
from .routes_helpers import validate_model, change_null_value


tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")

@tasks_bp.route("", methods=["POST"])
def create_tasks():
    request_body = request.get_json()
    new_task = Task.from_dict(request_body)

    db.session.add(new_task)
    db.session.commit()

    new_task = new_task.to_dict()
    new_task = change_null_value(new_task)
    
    return make_response({"task":new_task}, 201)

@tasks_bp.route("/<task_id>", methods=["GET"])
def handle_task(task_id):
    task = validate_model(Task, task_id)
    task = task.to_dict()
    task = change_null_value(task)
    return make_response({"task":task}, 200)

@tasks_bp.route("", methods=["GET"])
def handle_tasks():
    tasks = Task.query.all()
    tasks_response = [Task.to_dict(task) for task in tasks]

    if not tasks_response: 
        return make_response(jsonify(tasks_response),200)
    else: 
        change_null_value(tasks_response[0])
        return make_response(jsonify(tasks_response),200)

@tasks_bp.route("/<id>", methods=["PUT"])
def update_task(id):
    task = validate_model(Task, id)
    request_body = request.get_json()

    task.title = request_body['title'],
    task.description=request_body['description']
    
    db.session.commit()

    task = task.to_dict()
    change_null_value(task)

    return make_response({"task":task}, 200)

@tasks_bp.route("/<id>", methods=["DELETE"])
def delete_task(id):
    task = validate_model(Task, id)

    db.session.delete(task)
    db.session.commit()

    return make_response({"details":f'Task 1 "{task.title}" successfully deleted'}, 200)