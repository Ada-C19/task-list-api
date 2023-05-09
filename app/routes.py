from flask import Blueprint,jsonify, request, make_response, abort
from app import db
from app.models.task import Task
from app.helper import validate_model

tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")

@tasks_bp.route("", methods=["POST"])
def create_task():

    request_body = request.get_json()
    
    try:
        new_task = Task.from_dict(request_body)
        
        db.session.add(new_task)
        db.session.commit()

        return make_response(jsonify({"task": new_task.to_dict()}), 201)

    except KeyError as error:
        abort(make_response(jsonify({"details": "Invalid data"}), 400))
        
@tasks_bp.route("", methods=["GET"])
def get_all_tasks():
    task_query = Task.query

    sort_query = request.args.get("sort")
    if sort_query == "asc":
        task_query = task_query.order_by(Task.title.asc())
    else:
        task_query = task_query.order_by(Task.title.desc())

    tasks = task_query.all()
    tasks_response = [task.to_dict() for task in tasks]
    return jsonify(tasks_response)

@tasks_bp.route("/<task_id>", methods=["GET"])
def get_one_task(task_id):
    task = validate_model(Task, task_id)

    return jsonify({"task":task.to_dict()})

@tasks_bp.route("/<task_id>", methods=["PUT"])
def update_task(task_id):
    task = validate_model(Task, task_id)

    request_body = request.get_json()

    try:
        task.title = request_body["title"]
        task.description = request_body["description"]

        db.session.commit()

        return jsonify({"task":task.to_dict()})

    except KeyError as error:
        abort(make_response(jsonify({"message":f"Task {task_id} not found"}), 404))

@tasks_bp.route("/<task_id>", methods=["DELETE"])
def delete_task(task_id):
    task = validate_model(Task, task_id)

    try:
        db.session.delete(task)
        db.session.commit()

        return jsonify({"details": "Task 1 \"Go on my daily walk 🏞\" successfully deleted"})
    
    except KeyError as error:
        abort(make_response(jsonify({"message":f"Task {task_id} not found"}), 404))