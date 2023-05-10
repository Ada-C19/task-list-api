from app import db
from app.models.task import Task
from flask import Blueprint, jsonify, make_response, abort, request

tasks_bp = Blueprint("tasks", __name__, url_prefix = "/tasks")

@tasks_bp.route("", methods=["POST"])
def create_task():
    request_body = request.get_json()

    task = Task(
        title = request_body["title"],
        description = request_body["description"],
    )

    db.session.add(task)
    db.session.commit()

    return make_response(
        {
            "task": {
                "id": task.task_id,
                "title": task.title,
                "description": task.description,
                "is_complete": False
            }
        }, 201
    )

@tasks_bp.route("", methods=["GET"])
def read_tasks():
    tasks_response = []
    tasks = Task.query.all()

    for task in tasks:
        tasks_response.append(
            {
                "id": task.task_id,
                "title": task.title,
                "description": task.description,
                "is_complete": False
            }
        ), 200

    return jsonify(tasks_response)

@tasks_bp.route("/<task_id>", methods=["GET"])
def read_one_saved_task(task_id):
    task = validate_task(task_id)

    return {
        "task": {
            "id": task.task_id,
            "title": task.title,
            "description": task.description,
            "is_complete": False
        }
    }

@tasks_bp.route("/<task_id>", methods=["PUT"])
def update_task(task_id):
    task = validate_task(task_id)

    request_body = request.get_json()

    task.title = request_body["title"]
    task.description = request_body["description"]

    db.session.commit()

    return make_response(
        {
            "task": {
                "id": task.task_id,
                "title": task.title,
                "description": task.description,
                "is_complete": False
            }
        }, 200
    )

@tasks_bp.route("/<task_id>", methods=["DELETE"])
def delete_task(task_id):
    task = validate_task(task_id)

    db.session.delete(task)
    db.session.commit()

    return make_response(
        {
            "details": f"Task {task.task_id} \"{task.title}\" successfully deleted"
        }, 200
    )

def validate_task(task_id):
    task = Task.query.get(task_id)

    if not task:
        abort(make_response(
            {
                "details": "Invalid data"
            }, 404
        ))
    return task
   