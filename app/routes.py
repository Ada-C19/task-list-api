from flask import Blueprint
from os import abort
from app import db
from app.models.task import Task
from flask import Blueprint, jsonify, abort, make_response, request

tasks_bp = Blueprint("tasks_bp", __name__, url_prefix="/tasks")

def validate_task(task_id):
    try:
        task_id = int(task_id)
    except:
        abort(make_response({"message":f"task {task_id} invalid"}, 400))

    task = Task.query.get(task_id)

    if not task:
        abort(make_response({"message":f"task {task_id} not found"}, 404))

    return task

@tasks_bp.route("/task", methods=["POST"])
def create_task():
    request_body = request.get_json()
    new_task = Task(title=request_body["title"],
                    description=request_body["description"],
                    completed_at=request_body["is_complete"])

    db.session.add(new_task)
    db.session.commit()

    return make_response(f"Task {new_task.title} successfully created", 201)

@tasks_bp.route("/task", methods=["GET"])
def read_all_tasks():
    tasks_response = []
    tasks = Task.query.all()
    for task in tasks:
        tasks_response.append(
            {
                "id": task.id,
                "title": task.title,
                "description": task.description,
                "is_complete": task.completed_at
            }
        )
    return jsonify(tasks_response)

@tasks_bp.route("/<task_id>", methods=["GET"])
def read_one_task(task_id):
    task = validate_task(task_id)
    return {
            "id": task.id,
            "title": task.title,
            "description": task.description,
            "is_complete": task.completed_at
        }

@tasks_bp.route("/<task_id>", methods=["PUT"])
def update_task(task_id):
    task = validate_task(task_id)

    request_body = request.get_json()

    task.title = request_body["title"]
    task.description = request_body["description"]
    task.completed_at = request_body["is_completed"]

    db.session.commit()

    return make_response(f"Task #{task.id} successfully updated")

@tasks_bp.route("/<task_id>", methods=["DELETE"])
def delete_task(task_id):
    task = validate_task(task_id)

    db.session.delete(task)
    db.session.commit()

    return make_response(f"Task #{task.id} successfully deleted")



