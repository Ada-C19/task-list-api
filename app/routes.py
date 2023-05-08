from flask import Blueprint, request, jsonify, abort, make_response
from app.models.task import Task
from app import db
from helper import validate_model
from sqlalchemy import asc, desc
from datetime import datetime

tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")

# POST


@tasks_bp.route("", methods=["POST"])
def create_task():
    book_data = request.get_json()

    try:
        new_task = Task.from_dict(book_data)
        db.session.add(new_task)
        db.session.commit()

        message = {"task": new_task.to_dict()}
        return make_response(jsonify(message), 201)

    except KeyError:
        message = {"details": "Invalid data"}
        abort(make_response(jsonify(message), 400))


# GET
@tasks_bp.route("", methods=["GET"])
def get_all_tasks():
    sort_query = request.args.get("sort")

    if sort_query == "asc":
        all_tasks = Task.query.order_by(asc("title")).all()
    elif sort_query == "desc":
        all_tasks = Task.query.order_by(desc("title")).all()
    else:
        all_tasks = Task.query.all()

    tasks_response = [task.to_dict() for task in all_tasks]
    return make_response(jsonify(tasks_response), 200)


@tasks_bp.route("/<task_id>", methods=["GET"])
def get_one_task(task_id):
    task = validate_model(Task, task_id)

    response = {"task": task.to_dict()}
    return (jsonify(response), 200)


# PUT
@tasks_bp.route("/<task_id>", methods=["PUT"])
def update_task(task_id):
    task_to_update = validate_model(Task, task_id)
    response = request.get_json()

    task_to_update.title = response["title"]
    task_to_update.description = response["description"]
    db.session.commit()

    message = {"task": task_to_update.to_dict()}
    return make_response(jsonify(message), 200)


# DELETE
@tasks_bp.route("/<task_id>", methods=["DELETE"])
def delete_task(task_id):
    task_to_delete = validate_model(Task, task_id)
    db.session.delete(task_to_delete)
    db.session.commit()

    message = {
        "details": f'Task {task_id} "{task_to_delete.title}" successfully deleted'}
    return (jsonify(message), 200)


# PATCH
@tasks_bp.route("/<task_id>/mark_complete", methods=["PATCH"])
def mark_complete(task_id):
    task_to_mark = validate_model(Task, task_id)

    task_to_mark.completed_at = datetime.now()
    db.session.commit()

    message = {"task": task_to_mark.to_dict()}
    return make_response(jsonify(message), 200)


@tasks_bp.route("/<task_id>/mark_incomplete", methods=["PATCH"])
def mark_incomplete(task_id):
    task_to_mark = validate_model(Task, task_id)

    task_to_mark.completed_at = None
    db.session.commit()

    message = {"task": task_to_mark.to_dict()}
    return make_response(jsonify(message), 200)
