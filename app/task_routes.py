from app import db
from datetime import datetime
from app.models.task import Task
from app.helper import validate_model, post_slack
from flask import Blueprint, jsonify, abort, make_response, request


tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")

@tasks_bp.route("", methods=["POST"])
def create_task():
    request_body = request.get_json()
    try:
        new_task = Task.from_dict(request_body)
        db.session.add(new_task)
        db.session.commit()
        return make_response(jsonify({"task": new_task.validate_complete()}), 201)
    
    except KeyError as error:
        abort(make_response({"details": "Invalid data"}, 400))


@tasks_bp.route("", methods=["GET"])
def read_all_tasks():
    sort_query = request.args.get("sort")
    if sort_query == "asc":
        tasks = Task.query.order_by(Task.title.asc())
    elif sort_query == "desc":
        tasks = Task.query.order_by(Task.title.desc())
    else:
        tasks = Task.query.all()
        tasks_response = []
        for task in tasks:
            tasks_response.append(task.validate_complete())
        return jsonify(tasks_response)
    
    tasks_response = [task.validate_complete() for task in tasks]
    return jsonify(tasks_response)

@tasks_bp.route("/<task_id>", methods=["GET"])
def read_one_task(task_id):
    task = validate_model(Task, task_id)
    return jsonify({"task": task.validate_complete()})

@tasks_bp.route("/<task_id>", methods=["PUT"])
def update_task(task_id):
    task = validate_model(Task, task_id)
    # task.validate_complete()
    request_body = request.get_json()

    task.title = request_body["title"]
    task.description = request_body["description"]
    # task.completed_at = request_body["completed_at"]

    db.session.commit()
    return make_response(jsonify({"task": task.validate_complete()}), 200)

@tasks_bp.route("<task_id>/mark_complete", methods=["PATCH"])
def patch_complete_task(task_id):
    task = validate_model(Task, task_id)
    if not task.completed_at:
        task.completed_at = datetime.now().isoformat()

    db.session.commit()
    post_slack(task.title)
    return make_response(jsonify({"task": task.validate_complete()}), 200)

@tasks_bp.route("<task_id>/mark_incomplete", methods=["PATCH"])
def patch_incomplete_task(task_id):
    task = validate_model(Task, task_id)
    task.completed_at = None
    db.session.commit()
    

    return make_response(jsonify({"task": task.validate_complete()}), 200)

@tasks_bp.route("/<task_id>", methods=["DELETE"])
def delete_task(task_id):
    task = validate_model(Task, task_id)

    db.session.delete(task)
    db.session.commit()

    return make_response({"details": f"Task {task.task_id} \"{task.title}\" successfully deleted"}, 200)