from flask import Blueprint, make_response, request, jsonify, abort
from app import db
from app.models.task import Task

tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")

@tasks_bp.route("", methods=["POST"])
def create_task():
    request_body = request.get_json()
    new_task = Task(
        title = request_body["title"],
        description = request_body["description"]
        #completed_at = request_body["completed_at"]
        
    )
    
    response = {}
    response["task"] = new_task

    db.session.add(new_task)
    db.session.commit()

    if new_task.completed_at is None:
        is_complete = False
    else:
        is_complete = True

    return {"task":new_task.to_dict()}, 201

@tasks_bp.route("", methods=["GET"])
def get_all_tasks():
    response = []
    name_query = request.args.get("title")

    if name_query is None:
        all_tasks = Task.query.all()
    else:
        all_tasks = Task.query.filter_by(title=name_query)

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