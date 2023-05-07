from flask import Blueprint, request, make_response, jsonify, abort 
from app import db
from app.models.task import Task
from app.routes_helpers import validate_model
from sqlalchemy import desc


tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")


@tasks_bp.route("", methods=["POST"])
def create_task():
    request_body = request.get_json()

    if not request_body.get("title") or not request_body.get("description"):
        abort(make_response({"details": "Invalid data"}, 400))

    task = Task.from_dict(request_body)

    db.session.add(task)
    db.session.commit()

    return make_response(task.to_dict(), 201)


@tasks_bp.route("", methods=["GET"])
def read_all_tasks():
    sort_query = request.args.get("sort")

    if sort_query == "asc":
        tasks = Task.query.order_by(Task.title.asc()).all()
    elif sort_query == "desc":
        tasks = Task.query.order_by(Task.title.desc()).all()
    else:
        tasks = Task.query.all()
   
    tasks_response = [task.to_dict()["task"] for task in tasks]
   
    return make_response(jsonify(tasks_response), 200)


@tasks_bp.route("/<task_id>", methods=["GET"])
def get_one_task(task_id):
    task = validate_model(Task, task_id)

    return make_response(task.to_dict(), 200)
 

@tasks_bp.route("/<task_id>", methods=["PUT"])
def update_one_task(task_id):
    task = validate_model(Task, task_id)
 
    request_body = request.get_json()

    for attr, value in request_body.items():
        setattr(task, attr, value)

    db.session.add(task)
    db.session.commit()

    return make_response(task.to_dict(), 200)


@tasks_bp.route("/<task_id>", methods=["DELETE"])
def delete_one_task(task_id):
    task = validate_model(Task, task_id)

    db.session.delete(task)
    db.session.commit()

    return make_response(jsonify({"details": f"Task {task_id} \"{task.title}\" successfully deleted"}), 200)