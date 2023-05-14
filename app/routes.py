from flask import Blueprint, jsonify, abort, make_response, request
from app.models.task import Task
from app import db

tasks_bp = Blueprint("tasks_bp", __name__, url_prefix="/tasks")


def validate_model(cls, model_id):
    try:
        model_id = int(model_id)
    except:
        abort(make_response({"message":f"task {model_id} invalid"}, 400))

    task = cls.query.get(model_id)

    if not task:
        abort(make_response({"message":f"task {model_id} not found"}, 404))

    return task


@tasks_bp.route("", methods=["POST"])
def create_task():
    response_body = request.get_json()
    new_task = Task(title="Research APIs",
                    description="Look for youtube videos and examples",
                    is_complete=False)
    
    db.session.add(new_task)
    db.session.commit()


@tasks_bp.route("", methods=["GET"])
def read_all_tasks():
    tasks = Task.query.get.all()
    tasks_response = []

    for task in tasks:
        tasks_response.append(task.to_dict())
    return jsonify(tasks_response)

@tasks_bp.route("/<task_id>", methods=["GET"])
def read_one_task(task_id):
    task = validate_model(Task, task_id)
    return task.to_dict()

@tasks_bp.route("/<task_id>", methods=["PUT"])
def update_task(task_id):
    task = validate_model(Task, task_id)
    request_body = request.get_json()

    task.name = request_body["name"]
    task.description = request_body["description"]

    db.session.commit()
    return make_response(f"Task #{task.id} successfully updated", 200)

@tasks_bp.route("/<task_id>", methods=["DELETE"])
def delete_task(task_id):
    task = validate_model(Task, task_id)

    db.session.delete(task)
    db.session.commit()

    return make_response(f"Task #{task.id} successfully deleted!", 200)