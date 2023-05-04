from flask import abort, Blueprint, jsonify, make_response, request
from app import db
from app.models.task import Task


task_bp = Blueprint("task", __name__, url_prefix="/tasks")


@task_bp.route("", methods=["GET"])
def get_all_tasks():
    response = []
    tasks = Task.query.all()

    for task in tasks:
        response.append(task.to_dict())

    return jsonify(response), 200


@task_bp.route("/<task_id>", methods=["GET"])
def get_one_task(task_id):
    task = Task.query.get_or_404(task_id)
    return {"task": task.to_dict()}, 200


@task_bp.route("", methods=["POST"])
def create_new_task():
    request_body = request.get_json()
    new_task = Task(
        title=request_body["title"],
        description=request_body["description"]
    )
    db.session.add(new_task)
    db.session.commit()

    return {"task": new_task.to_dict()}, 201