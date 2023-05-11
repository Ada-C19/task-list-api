from app import db
from app.models.task import Task
from datetime import datetime
from flask import Blueprint, jsonify, make_response, request, abort
from app.helper_functions import validate_model, post_to_slack

task_bp = Blueprint("task", __name__, url_prefix="/tasks")

@task_bp.route("", methods=["POST"])
def create_task():
    request_body = request.get_json()
    try:
        new_task = Task.from_dict(request_body)
        
        db.session.add(new_task)
        db.session.commit()

        message  = {
            "task": new_task.to_dict()
        }
        return make_response(message, 201)
    except KeyError as e:
        abort(make_response({"details": "Invalid data"}, 400))

@task_bp.route("", methods=["GET"])
def read_all_tasks():
    sort_query = request.args.get("sort")
    if sort_query == "asc":
        tasks = Task.query.order_by(Task.title)
    elif sort_query == "desc":
        tasks = Task.query.order_by(Task.title.desc())
    else:
        tasks = Task.query.all()

    tasks_response = [task.to_dict() for task in tasks]
    return jsonify(tasks_response)

@task_bp.route("/<task_id>", methods=["GET"])
def get_one_task(task_id):
    task = validate_model(Task, task_id)
    message  = {
            "task": task.to_dict()
        }
    return make_response(message, 200)

@task_bp.route("/<task_id>", methods=["PUT"])
def update_task(task_id):
    task = validate_model(Task, task_id)
    request_body = request.get_json()

    task.title = request_body["title"]
    task.description = request_body["description"]

    db.session.commit()

    message  = {
            "task": task.to_dict()
        }

    return make_response(message, 200)
    

@task_bp.route("/<task_id>", methods=["DELETE"])
def delete_task(task_id):
    task = validate_model(Task, task_id)
    
    db.session.delete(task)
    db.session.commit()

    message  = {
            "details": f"Task {task.task_id} \"{task.title}\" successfully deleted"
        }

    return make_response(message, 200)

@task_bp.route("/<task_id>/mark_complete", methods=["PATCH"])
def mark_task_complete(task_id):
    task = validate_model(Task, task_id)

    task.completed_at = datetime.now()

    message  = {
            "task": task.to_dict()
        }
    
    db.session.commit()
    post_to_slack(task.title)
    return make_response(message, 200)

@task_bp.route("/<task_id>/mark_incomplete", methods=["PATCH"])
def mark_task_incomplete(task_id):
    task = validate_model(Task, task_id)

    task.completed_at = None

    message  = {
            "task": task.to_dict()
        }
    
    db.session.commit()
    
    return make_response(message, 200)
