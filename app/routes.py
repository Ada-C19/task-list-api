from flask import Blueprint, request, jsonify, make_response, abort
from app import db
from app.models.task import Task

task_bp = Blueprint("tasks", __name__, url_prefix="/tasks")

@task_bp.route("", methods=["POST"])
def add_task():
    request_body = request.get_json()

    if not "title" in request_body or not "description" in request_body or not "completed" in request_body:
        abort(make_response({"details": "Invalid data"},400))

    new_task = Task(
        title = request_body["title"],
        description = request_body["description"],
        completed_at = request_body["completed_at"]
    )
    

    db.session.add(new_task)
    db.session.commit()

    return {"task": new_task.to_result()}, 201


@task_bp.route("", methods=["GET"])
def get_tasks():
    response = []
    all_tasks = Task.query.all()

    for task in all_tasks:
        response.append(task.to_result())

    return jsonify(response), 200 


@task_bp.route("/<task_id>", methods=["GET"])
def get_one_task(task_id):
    one_task = validate_task(task_id)

    return make_response({"task": one_task.to_result()})

@task_bp.route("/<task_id>", methods=["PUT"])
def update_task(task_id):
    task = validate_task(task_id)

    request_body = request.get_json()

    task.title = request_body["title"]
    task.description = request_body["description"]

    db.session.commit()

    return make_response({"task": task.to_result()})

@task_bp.route("/<task_id>", methods=["DELETE"])
def delete_task(task_id):
    task = validate_task(task_id)

    db.session.delete(task)
    db.session.commit()

    return make_response({"details": f"Task {task_id} successfully deleted"})

def validate_task(task_id):
    try:
        task_id= int(task_id)
    except ValueError:
        abort(make_response({"message": f"invalid id: {task_id}"}, 400))
    
    task = Task.query.get(task_id)

    if not task:
        abort(make_response({"message": f"Task {task_id} not found."}, 404))

    return task.query.get(task_id)