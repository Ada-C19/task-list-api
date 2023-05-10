from flask import Blueprint, jsonify, request, abort, make_response
from app import db
from app.models.task import Task
import datetime

task_bp = Blueprint("tasks", __name__, url_prefix="/tasks")

def validate_item(model, item_id):
    try:
        item_id = int(item_id)
    except ValueError:
        return abort(make_response({"details": "Invalid data"}, 400))
    
    return model.query.get_or_404(item_id)


@task_bp.route("", methods=["POST"])
def create_task():
    request_body = request.get_json()
    if "title" not in request_body or "description" not in request_body:
        abort(make_response({"details": "Invalid data"}, 400))
    new_task = Task.from_dict(request_body)

    db.session.add(new_task)
    db.session.commit()

    return {"task": new_task.to_dict()}, 201

@task_bp.route("", methods=["GET"])
def get_tasks():
    response = []
    sort_query = request.args.get("sort")

    if sort_query is None:
        all_tasks = Task.query.all()
    elif sort_query == "asc":
        all_tasks = Task.query.order_by(Task.title).all()
    elif sort_query == "desc":
        all_tasks = Task.query.order_by(Task.title.desc()).all()

    for task in all_tasks:
        response.append(task.to_dict())

    return jsonify(response), 200

@task_bp.route("/<task_id>", methods=["GET"])
def get_one_task(task_id):
    task = validate_item(Task, task_id)

    return {"task": task.to_dict()}, 200

@task_bp.route("/<task_id>", methods=["PUT"])
def update_task(task_id):
    task = validate_item(Task, task_id)

    request_data = request.get_json()

    task.title = request_data["title"]
    task.description = request_data["description"]
    if "completed_at" in request_data:
        task.completed_at = request_data["completed_at"]

    db.session.commit()

    return {"task": task.to_dict()}, 200

@task_bp.route("/<task_id>", methods=["DELETE"])
def delete_task(task_id):
    task = validate_item(Task, task_id)

    db.session.delete(task)
    db.session.commit()

    return {"details": f'Task {task_id} "{task.title}" successfully deleted'}, 200


@task_bp.route("/<task_id>/mark_complete", methods=["PATCH"])
def update_task_completed_at(task_id):
    task = validate_item(Task, task_id)

    task.completed_at = datetime.date.today()

    db.session.commit()

    return {"task": task.to_dict()}, 200

@task_bp.route("/<task_id>/mark_incomplete", methods=["PATCH"])
def update_task_incompleted_at(task_id):
    task = validate_item(Task, task_id)

    task.completed_at = None

    db.session.commit()

    return {"task": task.to_dict()}, 200