from flask import Blueprint, abort, jsonify, make_response, request
from app import db
from app.models.task import Task


task_bp = Blueprint("tasks", __name__, url_prefix="/tasks")

def validate_task(task_id):
    try:
        task_id = int(task_id)
    except ValueError:
        abort(make_response({"msg": f"Task {task_id} invalid"}, 400))
    
    task = Task.query.get(task_id)

    if not task:
        abort(make_response({"msg": f"Task {task_id} not found"}, 404))

    return task

@task_bp.route("", methods=["POST"])
def add_task():
    request_body = request.get_json()
    try:
        new_task = Task(
            title = request_body["title"],
            description = request_body["description"],
            completed_at = None
        )
    except KeyError:
        return {
            "details": "Invalid data"
        }, 400

    db.session.add(new_task)
    db.session.commit()

    return {"task": new_task.to_dict()}, 201

@task_bp.route("", methods=["GET"])
def get_task():
    response = []

    title_query = request.args.get("title")

    if title_query is None:
        all_tasks = Task.query.all()
    else:
        all_tasks = Task.query.filter_by(title=title_query)

    for task in all_tasks:
        response.append(task.to_dict())

    return (jsonify(response), 200)

@task_bp.route("/<task_id>", methods=["GET"])
def get_one_task(task_id):
    task = validate_task(task_id)

    return {"task":task.to_dict()}, 200

@task_bp.route("/<task_id>", methods=["PUT"])
def update_task(task_id):
    task = validate_task(task_id)

    request_body = request.get_json()

    task.title = request_body["title"]
    task.description = request_body["description"]

    db.session.commit()

    return {"task":task.to_dict()}, 200

@task_bp.route("/<task_id>", methods=["DELETE"])
def delete_task(task_id):
    task = validate_task(task_id)

    db.session.delete(task)
    db.session.commit()

    return {'details': f'Task {task.task_id} "{task.title}" successfully deleted'}, 200