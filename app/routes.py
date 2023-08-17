from flask import abort, Blueprint, jsonify, make_response, request
from sqlalchemy import desc, asc
from app import db
from app.models.task import Task
from datetime import datetime, timezone


task_bp = Blueprint("task", __name__, url_prefix="/tasks")


@task_bp.route("", methods=["GET"])
def get_all_tasks():

    sort_query = request.args.get("sort")
    if sort_query == "asc":
        tasks = Task.query.order_by(asc(Task.title))
    elif sort_query == "desc":
        tasks = Task.query.order_by(desc(Task.title))
    else:
        tasks = Task.query.all()

    response = []
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
    try:
        new_task = Task(
            title=request_body["title"],
            description=request_body["description"]
        )
    except KeyError:
        return {"details": "Invalid data"}, 400
    
    db.session.add(new_task)
    db.session.commit()

    return {"task": new_task.to_dict()}, 201


@task_bp.route("/<task_id>", methods=["PUT"])
def update_one_task(task_id):
    task = Task.query.get_or_404(task_id)
    request_body = request.get_json()

    task.title = request_body["title"]
    task.description = request_body["description"]

    db.session.commit()

    return {"task": task.to_dict()}, 200


@task_bp.route("/<task_id>/mark_complete", methods=["PATCH"])
def mark_complete_one_task(task_id):
    task = Task.query.get_or_404(task_id)

    task.completed_at = datetime.now(timezone.utc)

    db.session.commit()

    return {"task": task.to_dict()}, 200


@task_bp.route("/<task_id>/mark_incomplete", methods=["PATCH"])
def mark_incomplete_one_task(task_id):
    task = Task.query.get_or_404(task_id)

    task.completed_at = None

    db.session.commit()

    return {"task": task.to_dict()}, 200


@task_bp.route("/<task_id>", methods=["DELETE"])
def delete_one_task(task_id):
    task = Task.query.get_or_404(task_id)

    db.session.delete(task)
    db.session.commit()

    return {"details": (f'Task {task.task_id} "{task.title}" '
                        'successfully deleted')}, 200