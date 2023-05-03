from flask import abort, Blueprint, jsonify, make_response, request
from app import db
from app.models.task import Task


task_bp = Blueprint("task", __name__, url_prefix="/tasks")


@task_bp.route("", methods=["GET"])
def get_all_tasks():
    response = []
    tasks = Task.query.all()

    for task in tasks:
        task_dict = {
            "id": task.task_id,
            "title": task.title,
            "description": task.description,
            "is_complete": False
        }
        if task.completed_at is not None:
            task_dict["is_complete"] = True

        response.append(task_dict)

    return jsonify(response), 200


@task_bp.route("/<task_id>", methods=["GET"])
def get_one_task(task_id):
    task = Task.query.get_or_404(task_id)
    task_dict = {
        "id": task.task_id,
        "title": task.title,
        "description": task.description,
        "is_complete": False
    }
    if task.completed_at is not None:
        task_dict["is_complete"] = True

    return {"task": task_dict}, 200