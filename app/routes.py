from app import db
from app.models.task import Task
from flask import Blueprint, jsonify, abort, make_response, request
from sqlalchemy import desc

tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")

def validate_model(cls, model_id):
    try:
        model_id = int(model_id)
    except:
        abort(make_response(jsonify({"message":f"{cls.__name__} {model_id} invalid"}), 400))
    
    model = cls.query.get(model_id)

    if not model:
        abort(make_response(jsonify({"message":f"{cls.__name__} {model_id} not found"}), 404))
    
    return model

@tasks_bp.route("", methods=["GET"])
def get_all_tasks():

    sort_direction = request.args.get("sort")

    if sort_direction == "asc":
        tasks = Task.query.order_by(Task.title)
    elif sort_direction == "desc":
        tasks = Task.query.order_by(Task.title.desc())
    else:
        tasks = Task.query.all()
    
    results = [task.to_dict() for task in tasks]

    return jsonify(results)

@tasks_bp.route("/<task_id>", methods=["GET"])
def get_one_task(task_id):
    task = validate_model(Task, task_id)
    response = {"task": task.to_dict()}

    return jsonify(response)

@tasks_bp.route("", methods=["POST"])
def create_task():
    request_body = request.get_json()
    
    new_task_is_valid = "title" in request_body and "description" in request_body
    if not new_task_is_valid:
        abort(make_response(jsonify({"details":"Invalid data"}), 400))

    new_task = Task.from_dict(request_body)
    db.session.add(new_task)
    db.session.commit()
    
    response = {"task": new_task.to_dict()}

    return make_response((jsonify(response)), 201)

@tasks_bp.route("/<task_id>", methods=["PUT"])
def update_one_task(task_id):    
    task = validate_model(Task, task_id)
    updated_data = request.get_json()

    task.title = updated_data["title"]
    task.description = updated_data["description"]

    db.session.commit()

    response = {"task": task.to_dict()}

    return make_response(response, 200)

@tasks_bp.route("<task_id>", methods=["DELETE"])
def delete_one_task(task_id):
    task_to_delete = validate_model(Task, task_id)
    
    db.session.delete(task_to_delete)
    db.session.commit()

    message = {"details":f"Task {task_id} \"{task_to_delete.title}\" successfully deleted"}
    return make_response(message, 200)