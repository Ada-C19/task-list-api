from app import db
from app.models.task import Task
from flask import Blueprint, jsonify, make_response, abort, request

tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")

def validate_task(task_id):
    try:
        task_id = int(task_id)
    except:
        message = f"task {task_id} not found"
        abort(make_response({"message": message}, 400))

    task = Task.query.get(task_id)

    if not task:
        abort(make_response({"message":f"task {task_id} not found"}, 404))
    return task



@tasks_bp.route("", methods =["POST"])
def create_task():
    request_body = request.get_json()

    if "description" not in request_body or "title" not in request_body:
        abort(make_response({"details": "Invalid data"}, 400))

    new_task = Task.from_dict(request_body)
    
    db.session.add(new_task)
    db.session.commit()
    
    return make_response({"task": new_task.make_dict()}, 201)
    
@tasks_bp.route("", methods =["GET"])
def get_tasks_data():
    title_query = request.args.get("title")

    if title_query:
        tasks = Task.query.filter_by(title=title_query)
    else:
        tasks = Task.query.all()

    tasks_response = []
    for task in tasks:
        tasks_response.append(task.make_dict())
    return jsonify(tasks_response), 200



@tasks_bp.route("/<task_id>", methods =["GET"])
def get_task_data(task_id):
    task = validate_task(task_id)
    return make_response({"task": task.make_dict()}, 200)

@tasks_bp.route("/<task_id>", methods =["PUT"])
def update_task(task_id):
    task = validate_task(task_id)
    request_body = request.get_json()
    
    task.title = request_body["title"]
    task.description = request_body["description"]

    db.session.commit()

    return make_response({"task": task.make_dict()}, 200)

@tasks_bp.route("/<task_id>", methods =["DELETE"])
def delete_task(task_id):
    task = validate_task(task_id)

    db.session.delete(task)
    db.session.commit()

    message = {f"details": 'Task 1 "Go on my daily walk 🏞" successfully deleted'}
    return make_response(jsonify(message)), 200

