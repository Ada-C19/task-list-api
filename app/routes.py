from flask import abort, Blueprint, jsonify, make_response, request
from app import db
from app.models.task import Task
from datetime import datetime, date

task_bp = Blueprint("tasks", __name__, url_prefix="/tasks")

@task_bp.route("", methods = ["GET"])
def get_tasks():
    response = []
    title_sort_query = request.args.get("sort")

    if title_sort_query is None:
        all_tasks = Task.query.all()
    elif "asc" in title_sort_query: 
        all_tasks = Task.query.order_by(Task.title.asc()).all()
    elif "desc" in title_sort_query:
        all_tasks = Task.query.order_by(Task.title.desc()).all()

    for task in all_tasks:
        response.append(task.to_dict())
    return jsonify(response), 200


@task_bp.route("", methods = ["POST"])
def create_new_task():
    request_body = request.get_json()
    try:
        new_task = Task(
            title = request_body["title"],
            description = request_body["description"]
        )
        db.session.add(new_task)
        db.session.commit()

        result = new_task.to_dict()
        return {"task": new_task.to_dict()}, 201
    except:
        return abort(make_response({"details": "Invalid data"}, 400))


@task_bp.route("/<task_id>", methods = ["GET"])
def get_task_by_id(task_id):
    task = validate_task_id(task_id)
    return {"task": task.to_dict()}, 200


@task_bp.route("/<task_id>", methods = ["PUT"])
def update_one_task(task_id):
    updated_task = validate_task_id(task_id)

    request_body = request.get_json()
    updated_task.title = request_body["title"],
    updated_task.description = request_body["description"]

    db.session.commit()
    return {"task": updated_task.to_dict()}, 200

@task_bp.route("/<task_id>", methods = ["DELETE"])
def delete_one_task(task_id):
    task = validate_task_id(task_id)
    
    db.session.delete(task)
    db.session.commit()

    return {"details": f'Task {task_id} "{task.title}" successfully deleted'}, 200

def validate_task_id(task_id):
    try:
        valid_task_id = int(task_id)
    except:
        return abort(make_response({"message": f"invalid id: {task_id}"}, 400))
    
    return Task.query.get_or_404(valid_task_id)
#passes wave one

@task_bp.route("/<task_id>/mark_complete", methods = ["PATCH"])
def mark_task_complete(task_id):
    updated_task = validate_task_id(task_id)

    updated_task.completed_at = datetime.now()
    db.session.commit()
    return {"task": updated_task.to_dict()}, 200

@task_bp.route("/<task_id>/mark_incomplete", methods = ["PATCH"])
def mark_task_incomplete(task_id):
    updated_task = validate_task_id(task_id)

    updated_task.completed_at = None
    db.session.commit()
    return {"task": updated_task.to_dict()}, 200
