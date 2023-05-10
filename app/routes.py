from app import db
from app.models.task import Task
from flask import Blueprint, jsonify, abort, make_response, request

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
    new_task = Task.from_dict(request_body)
    db.session.add(new_task)
    db.session.commit()
    
    response = {"task": new_task.to_dict()}

    return make_response((jsonify(response)), 201)