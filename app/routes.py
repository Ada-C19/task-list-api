from flask import Blueprint, make_response, request, jsonify, abort
from app import db
from app.models.task import Task
from datetime import datetime

tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")

@tasks_bp.route("", methods=["POST"])
def create_task():
    request_body = request.get_json()
    if "title" not in request_body or "description" not in request_body:
        return {"details": "Invalid data"}, 400
    # should I have to do the next if check?
    if "completed_at" in request_body:
        new_task = Task(
            title = request_body["title"],
            description = request_body["description"],
            completed_at = request_body["completed_at"]
        )
    else:
        new_task = Task(
            title = request_body["title"],
            description = request_body["description"]
        )

    db.session.add(new_task)
    db.session.commit()

    return {"task":new_task.to_dict()}, 201

@tasks_bp.route("", methods=["GET"])
def get_all_tasks():
    response = []
    sort_query = request.args.get("sort")

    if sort_query is None:
        all_tasks = Task.query.all()
    elif sort_query == "asc":
        all_tasks = Task.query.order_by(Task.title.asc())
    else:
        all_tasks = Task.query.order_by(Task.title.desc())

    for task in all_tasks: 
        response.append(task.to_dict())

    return jsonify(response), 200

@tasks_bp.route("/<task_id>", methods=["GET"])
def get_one_task(task_id):
    task = validate_task(task_id)
    
    return {"task": task.to_dict()}, 200

def validate_task(task_id):
    try:
        task_id = int(task_id)
    except ValueError:
        return abort(make_response({"details": "Invalid Data"}, 400))

    if Task.query.get(task_id) is None:
        return abort(make_response({"details": "id not found"}, 404))

    return Task.query.get(task_id)

@tasks_bp.route("/<task_id>", methods=["PUT"])
def update_task(task_id):
    task = validate_task(task_id)
    request_body = request.get_json()

    task.title = request_body["title"]
    task.description = request_body["description"]

    db.session.commit()

    return {"task": task.to_dict()}, 200

@tasks_bp.route("/<task_id>", methods=["DELETE"])
def delete_task(task_id):
    task = validate_task(task_id)
    title = task.title
    db.session.delete(task)
    db.session.commit()

    return {"details": f'Task {task_id} "{title}" successfully deleted'}, 200

@tasks_bp.route("/<task_id>/mark_complete", methods=["PATCH"])
def mark_complete(task_id):
    task = validate_task(task_id)

    task.completed_at = datetime.utcnow()

    
    db.session.commit()
    
    return {"task": task.to_dict()}, 200

@tasks_bp.route("/<task_id>/mark_incomplete", methods=["PATCH"])
def mark_incomplete(task_id):
    task = validate_task(task_id)

    task.completed_at = None
    
    db.session.commit()
    
    return {"task": task.to_dict()}, 200