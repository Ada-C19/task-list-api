from flask import Blueprint, jsonify, request, abort, make_response 
from app import db 
from app.models.task import Task 
from datetime import datetime

tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")
@tasks_bp.route("", methods=["POST"])
def add_task():
    request_body = request.get_json()

    if "description" not in request_body\
        or "title" not in request_body:
        return jsonify({"details": "Invalid data"}), 400
    
    new_task = Task(title=request_body["title"], description=request_body["description"])

    db.session.add(new_task)
    db.session.commit()

    is_complete = True if new_task.completed_at else False

    
    return {
        "task":
            {
            "id": new_task.id,
            "title": new_task.title,
            "description": new_task.description,
            "is_complete": is_complete
            }
    }, 201

@tasks_bp.route("", methods=["GET"])
def get_tasks():
    response = []
    sort_query = request.args.get("sort")
    if sort_query is None:
        all_tasks = Task.query.all()

    elif sort_query == "asc":
        all_tasks = Task.query.order_by(Task.title.asc())
    else:
        all_tasks = Task.query.order_by(Task.title.desc())
    
    for task in all_tasks:
        response.append(task.to_dict()["task"])
    
    return jsonify(response), 200

@tasks_bp.route("<task_id>", methods=["GET"])
def get_task_by_id(task_id):
    task = Task.query.get_or_404(task_id)
    response = task.to_dict()
    return jsonify(response), 200

@tasks_bp.route("<task_id>", methods=["PUT"])
def update_task(task_id):
    task = Task.query.get_or_404(task_id)

    request_data = request.get_json()

    task.title = request_data["title"]
    task.description = request_data["description"]

    db.session.commit()
    response = task.to_dict()
    return jsonify(response), 200

@tasks_bp.route("<task_id>", methods=["DELETE"])
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)

    db.session.delete(task)
    db.session.commit()

    return {"details": f'Task {task_id} "{task.title}" successfully deleted'}, 200

@tasks_bp.route("<task_id>/mark_complete", methods=["PATCH"])
def mark_task_complete(task_id):
    task = Task.query.get_or_404(task_id)
    request_data = request.get_json()

    task.completed_at = datetime.utcnow()
    db.session.commit()

    response = task.to_dict()
    return jsonify(response), 200

@tasks_bp.route("<task_id>/mark_incomplete", methods=["PATCH"])
def mark_task_incomplete(task_id):
    task = Task.query.get_or_404(task_id)
    request_data = request.get_json()

    task.completed_at = None
    db.session.commit()

    response = task.to_dict()
    return jsonify(response), 200

