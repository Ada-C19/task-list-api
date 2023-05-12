from app import db
from app.models.task import Task

from flask import Blueprint, jsonify, abort, make_response, request
from sqlalchemy import desc
from sqlalchemy import asc 
from datetime import date

tasks_bp = Blueprint("tasks_bp", __name__, url_prefix="/tasks")


def validate_model(cls, id):
    try:
        id = int(id)
    except:
        abort(make_response({"message":f"{cls.__name__} {id} invalid"}, 400))

    data = cls.query.get(id)

    if not data:
        abort(make_response({"message":f"{cls.__name__} {id} not found"}, 404))

    return data

#POST METHOD, CREATE NEW ROW OF DATA
@tasks_bp.route("", methods=["POST"],strict_slashes=False)
def create_tasks():
    request_body = request.get_json()

    if "description" not in request_body or "title" not in request_body:
        return make_response(jsonify({"details": "Invalid data"}), 400)
    new_task= Task.from_dict(request_body)

    
    db.session.add(new_task)
    db.session.commit()

    return make_response(jsonify({"task": new_task.to_dict()}), 201)

#PUT METHOD, UPDATE
@tasks_bp.route("/<task_id>", methods=["PUT"])
def update_task(task_id):
    task = validate_model(Task, task_id)

    request_body = request.get_json()

    task.title = request_body["title"]
    task.description = request_body["description"]

    db.session.commit()

    return make_response(jsonify({"task": task.to_dict()}), 200)

#DELETE METHOD
@tasks_bp.route("/<task_id>", methods=["DELETE"])
def delete_task(task_id):
    task = validate_model(Task, task_id)

    db.session.delete(task)
    db.session.commit()

    return make_response(jsonify({"details": f"Task {task.task_id} \"{task.title}\" successfully deleted"}), 200)

# GET ALL TASKS
@tasks_bp.route("", methods=["GET"])
def handle_task():
    
    tasks = Task.query.all()

    sort_order = request.args.get("sort")

    if sort_order=="desc":
        tasks = Task.query.order_by(desc(Task.title))
    elif sort_order=="asc":
        tasks = Task.query.order_by(asc(Task.title))

    tasks_response = []
    for task in tasks:
        tasks_response.append(task.to_dict())


    return jsonify(tasks_response)


# GET ONE TASK
@tasks_bp.route("/<task_id>", methods = ["GET"])
def get_one_task(task_id):

    task = validate_model(Task, task_id)

    if task.goal_id:
        return {"task": task.to_dict_with_gold_id()}
    return {"task": task.to_dict()}

# PATCH
@tasks_bp.route("/<task_id>/mark_incomplete", methods = ["PATCH"])
def patch_incompleted(task_id):

    task = validate_model(Task, task_id)
    if task.completed_at:
        task.completed_at = None
        db.session.commit()
    return {"task": task.to_dict()}

# PATCH
@tasks_bp.route("/<task_id>/mark_complete", methods = ["PATCH"])
def patch_completed(task_id):

    task = validate_model(Task, task_id)
    if not task.completed_at:
        task.completed_at = date.today()
        db.session.commit()
    return {"task": task.to_dict()}

