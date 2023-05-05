from flask import Blueprint, jsonify, request, make_response, abort
from app import db
from app.models.goal import Goal
from app.models.task import Task
from datetime import datetime

task_bp = Blueprint("tasks", __name__, url_prefix="/tasks")

def validate_task(task_id):
    try:
        task_id = int(task_id)
    except ValueError:
        return abort(make_response({"details": "Invalid data"}, 400))
    
    task = Task.query.get(task_id)

    if not task:
        return abort(make_response({"details": f"id {task_id} not found"}, 404))
    
    return task
    

@task_bp.route("", methods=["POST"])
def add_tasks():
    request_body = request.get_json()
    
    if "title" not in request_body or "description" not in request_body:
        return {f"details": "Invalid data"}, 400


    new_task = Task(
        title = request_body["title"],
        description = request_body["description"],
        completed_at = None
        # completed_at = request_body["completed_at"] 
    )

    db.session.add(new_task)
    db.session.commit()

    return make_response(jsonify({"task": new_task.to_dict()}), 201)


@task_bp.route("", methods=["GET"])
def get_tasks():
    response = []
    
    title_query = request.args.get("title")
    if title_query is None:
        all_tasks = Task.query.all()
    else:
        all_tasks = Task.query.filter_by(title=title_query)
    
    for task in all_tasks:
        response.append(task.to_dict())

    return make_response(jsonify(response), 200)


@task_bp.route("/<task_id>", methods=["GET"])
def get_one_task(task_id):
    task = validate_task(task_id)

    return make_response(jsonify({"task": task.to_dict()}), 200)


@task_bp.route("/<task_id>", methods=["PUT"])
def update_task(task_id):
    task = validate_task(task_id)

    request_body = request.get_json()

    # if not task.title or not task.description or not task.completed:
    #     return {f"details": "Invalid data"}, 404

    task.title = request_body["title"]
    task.description = request_body["description"]
    task.completed_at = None
    
    # datetime.utcnow()

    db.session.commit()

    return make_response(jsonify({"task": task.to_dict()}), 200)

@task_bp.route("/<task_id>", methods=["DELETE"])
def delete_task(task_id):
    task = validate_task(task_id)

    db.session.delete(task)

    db.session.commit()

    return {"details": f"Task {task_id} \"{task.title}\" successfully deleted"}, 200