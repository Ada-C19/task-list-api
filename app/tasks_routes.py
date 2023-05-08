from app import db
from flask import Blueprint, request, make_response, jsonify
from app.models.task import Task
from .routes_helpers import validate_model, slack_call
from datetime import datetime

tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")

# CREATE
@tasks_bp.route("", methods=["POST"])
def create_tasks():
    request_body = request.get_json()
    new_task = Task.from_dict(request_body)

    db.session.add(new_task)
    db.session.commit()

    response_body = dict(task=new_task.to_dict())

    return make_response(jsonify(response_body), 201)
# READ
@tasks_bp.route("/<task_id>", methods=["GET"])
def handle_task(task_id):
    task = validate_model(Task, task_id)
    response_body = dict(task=task.to_dict())
    return make_response(jsonify(response_body), 200)

@tasks_bp.route("", methods=["GET"])
def handle_tasks():
    if request.args.get("sort") == "asc":
        tasks = Task.query.order_by(Task.title.asc()).all()
    elif request.args.get("sort") == "desc":
        tasks = Task.query.order_by(Task.title.desc()).all()
    else:
        tasks = Task.query.all()
    response_body = [Task.to_dict(task) for task in tasks]

    return make_response(jsonify(response_body),200)

# UPDATE
@tasks_bp.route("/<id>", methods=["PUT"])
def update_task(id):
    task = validate_model(Task, id)
    request_body = request.get_json()

    task.title = request_body['title'],
    task.description = request_body['description']
    
    db.session.commit()

    response_body = dict(task=task.to_dict())

    return make_response(jsonify(response_body), 200)


@tasks_bp.route("/<id>/mark_complete", methods=["PATCH"])
def mark_complete(id):
    task = validate_model(Task, id)

    task.completed_at=datetime.utcnow()
    
    db.session.commit()

    response_body = dict(task=task.to_dict())

    # Slack API call
    slack_call(response_body['task'])
    
    return make_response(jsonify(response_body), 200)

@tasks_bp.route("/<id>/mark_incomplete", methods=["PATCH"])
def mark_incomplete(id):
    task = validate_model(Task, id)

    task.completed_at=None
    
    db.session.commit()

    response_body = dict(task=task.to_dict())

    return make_response(jsonify(response_body), 200)

# DELETE
@tasks_bp.route("/<id>", methods=["DELETE"])
def delete_task(id):
    task = validate_model(Task, id)

    db.session.delete(task)
    db.session.commit()

    response_body = dict(details=f'Task {task.task_id} "{task.title}" successfully deleted')

    return make_response(jsonify(response_body), 200)