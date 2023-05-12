from app import db
from flask import Blueprint, jsonify, abort, make_response, request
from app.models.task import Task
from app.helpers.helpers import validate_model, send_message
from datetime import datetime
import requests 

task_bp = Blueprint("task_bp", __name__, url_prefix="/tasks")

@task_bp.route("", methods=["POST"])
def create_task():
    request_body = request.get_json()
    try:
        new_task = Task.from_dict(request_body)

        db.session.add(new_task)
        db.session.commit()

        return {"task" : new_task.to_dict()}, 201
    
    except KeyError:
        abort(make_response({"details": "Invalid data"}, 400))

    db.session.add(new_task)
    db.session.commit()



@task_bp.route("", methods=["GET"])
def get_all_tasks():
    sort_query = request.args.get("sort")
    if sort_query:
        if sort_query == "asc":
            tasks = Task.query.order_by(Task.title.asc()).all()
        elif sort_query == "desc":
            tasks = Task.query.order_by(Task.title.desc()).all()
    else:
        tasks = Task.query.all()
    if not tasks:
        return make_response(jsonify([]), 200)

    results = [task.to_dict() for task in tasks]
    return jsonify(results)

@task_bp.route("/<task_id>", methods=["GET"])
def get_task_by_id(task_id):
    task = validate_model(Task, task_id)
    results = {"task" : task.to_dict()}

    return make_response(jsonify(results), 200)

@task_bp.route("/<task_id>", methods=["PUT"])
def update_task(task_id):
    task_data = request.get_json()
    task_to_update = validate_model(Task, task_id)

    task_to_update.title = task_data["title"]
    task_to_update.description = task_data["description"]
    
    

    db.session.commit()
    return {"task": task_to_update.to_dict()}

@task_bp.route("/<task_id>", methods=["DELETE"])
def delete_task(task_id):
    task = validate_model(Task, task_id)

    db.session.delete(task)
    db.session.commit()

    return make_response({"details": f"Task {task_id} \"{task.title}\" successfully deleted"})

@task_bp.route("/<task_id>/mark_complete", methods=["PATCH"])
def mark_complete(task_id):
    task_to_update = validate_model(Task, task_id)

    task_to_update.completed_at = datetime.today()
    

    db.session.commit()
    send_message(task_to_update)
    return {"task" : task_to_update.to_dict()}

@task_bp.route("/<task_id>/mark_incomplete", methods=["PATCH"])
def mark_incomplete(task_id):
    task_to_update = validate_model(Task, task_id)

    task_to_update.completed_at = None
    

    db.session.commit()

    return {"task" : task_to_update.to_dict()}


