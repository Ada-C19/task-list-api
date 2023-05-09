from app import db
from flask import Blueprint, request, make_response, jsonify
from app.models.task import Task
from .routes_helpers import validate_model
from sqlalchemy import asc, desc

task_bp = Blueprint("tasks", __name__, url_prefix="/tasks")


@task_bp.route("", methods=["POST"])
def create_task():
    request_body = request.get_json()
    new_task = Task.from_dict(request_body)

    db.session.add(new_task)
    db.session.commit()

    return make_response(jsonify({"task": new_task.to_dict()}), 201)


@task_bp.route("", methods=["GET"])
def get_all_tasks():
    # tasks = Task.query.all()

    task_query = Task.query

    sort_query = request.args.get("sort")

    if sort_query == "asc":
        task_query = task_query.order_by(asc(Task.title))
    elif sort_query == "desc":
        task_query = task_query.order_by(desc(Task.title))
    
    tasks_response = [task.to_dict() for task in task_query]
    return jsonify(tasks_response)


@task_bp.route("/<task_id>", methods=["GET"])
def get_one_task(task_id):
    task = validate_model(Task, task_id)

    return jsonify({"task": task.to_dict()})


@task_bp.route("/<task_id>", methods=["PUT"])
def update_task(task_id):
    task = validate_model(Task, task_id)

    request_body = request.get_json()
    task.update_from_dict(request_body)

    db.session.commit()

    return make_response(jsonify({"task": task.to_dict()}), 200)


@task_bp.route("/<task_id>", methods=["DELETE"])
def delete_task(task_id):
    task = validate_model(Task, task_id)

    db.session.delete(task)
    db.session.commit()

    return make_response(jsonify({"details": f"Task {task.task_id} \"{task.title}\" successfully deleted"}))
