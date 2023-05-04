from app import db
from app.models.task import Task
from flask import Blueprint
from flask import Blueprint, jsonify, abort, make_response, request


tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")

def validate_model(cls, model_id):
    try:
        model_id = int(model_id)
    except:
        abort(make_response({"message":f"{cls.__name__.lower()} {model_id} invalid"}, 400))
    
    item = cls.query.get(model_id)
    
    if not item:
        abort(make_response({"message":f"{cls.__name__.lower()} {model_id} not found"}, 404))
    
    return item

@tasks_bp.route("", methods=["GET"])
def read_all_tasks():
    tasks = Task.query.all()

    tasks_response = [task.to_dict() for task in tasks]

    return jsonify(tasks_response), 200

@tasks_bp.route("/<task_id>", methods=["GET"])
def get_task(task_id):
    task = validate_model(Task, task_id)
    return {"task": task.to_dict()}, 200

@tasks_bp.route("", methods=["POST"])
def create_task():
    request_body = request.get_json()
    try:
        new_task = Task.from_dict(request_body)
    except KeyError:
        return {
        "details": "Invalid data"
        }, 400

    db.session.add(new_task)
    db.session.commit()

    return {
        "task": new_task.to_dict()
    }, 201

@tasks_bp.route("/<task_id>", methods=["PUT"])
def update_task(task_id):
    task_to_update = validate_model(Task, task_id)

    request_body = request.get_json()
    for key, value in request_body.items():
        if key == "title":
            task_to_update.title = value
        elif key == "description":
            task_to_update.description = value
        elif key == "is_complete":
            task_to_update.is_complete = value
    
    db.session.commit()

    return {
        "task": task_to_update.to_dict()
    }, 200

@tasks_bp.route("/<task_id>", methods=["DELETE"])
def delete_task(task_id):
    task_to_delete = validate_model(Task, task_id)

    db.session.delete(task_to_delete)
    db.session.commit()

    return {
        "details": f'Task {task_to_delete.id} "{task_to_delete.title}" successfully deleted'
    }, 200
