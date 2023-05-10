from flask import Blueprint, jsonify, abort, make_response, request
import datetime
from app.models.task import Task
from app.routes.helper_funcs import get_valid_item_by_id
from app import db

# All routes for tasks start with "/tasks" URL prefix
tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")


@tasks_bp.route("", methods=['POST'])
def create_task():
    request_body = request.get_json()

    if "title" not in request_body or "description" not in request_body:
        return {
            "details": "Invalid data"
        }, 400
    new_task = Task.from_dict(request_body)

    db.session.add(new_task)
    db.session.commit()

    return {
        "task": new_task.to_dict()
    }, 201


@tasks_bp.route("", methods=["GET"])
def handle_get_tasks_request():
    sort_query = request.args.get("sort")

    if sort_query:
        if sort_query == "asc":
            tasks = Task.query.order_by(Task.title.asc())
        elif sort_query == "desc":
            tasks = Task.query.order_by(Task.title.desc())
    else:
        tasks = Task.query.all()
    
    task_response = []
    for task in tasks:
        task_response.append(task.to_dict())

    return jsonify(task_response), 200


@tasks_bp.route("/<task_id>", methods=["GET"])
def handle_get_single_task(task_id):
    task = get_valid_item_by_id(Task, task_id)

    return {
        "task": task.to_dict()
    }, 200


@tasks_bp.route("/<task_id>", methods=["PUT"])
def update_one_task(task_id):
    request_body = request.get_json()
    if "title" not in request_body or "description" not in request_body:
        return {
            "details": "Invalid data"
        }, 400
    task_to_update = get_valid_item_by_id(Task, task_id)
    
    task_to_update.title = request_body["title"]
    task_to_update.description = request_body["description"]

    db.session.commit()
    
    return {
        "task": task_to_update.to_dict()
    }, 200


@tasks_bp.route("/<task_id>", methods=["DELETE"])
def delete_one_task(task_id):
    task_to_delete = get_valid_item_by_id(Task, task_id)

    db.session.delete(task_to_delete)
    db.session.commit()

    return {'details': f'Task {task_to_delete.id} "{task_to_delete.title}" successfully deleted'}, 200


@tasks_bp.route("/<task_id>/mark_complete", methods=["PATCH"])
def mark_task_as_completed(task_id):
    updated_task=get_valid_item_by_id(Task, task_id)
    updated_task.completed_at = datetime.datetime.utcnow()
    db.session.commit()

    return {
        "task": updated_task.to_dict()
    }


@tasks_bp.route("/<task_id>/mark_incomplete", methods=["PATCH"])
def mark_task_as_incomplete(task_id):
    updated_task=get_valid_item_by_id(Task, task_id)
    updated_task.completed_at = None
    db.session.commit()

    return {
        "task": updated_task.to_dict()
    }