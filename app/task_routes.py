from app import db
from flask import Blueprint
from app.models.task import Task
from flask import Blueprint, jsonify, abort, make_response, request

tasks_bp = Blueprint("tasks_bp", __name__, url_prefix="/tasks")

def validate_task(task_id):
    try:
        task_id = int(task_id)
    except:
        abort(make_response({"message": f"task {task_id} is invalid"}, 400))

    task = Task.query.get(task_id)
    
    if not task:
        abort(make_response({"message": f"task {task_id} not found"}, 404))
    
    return task

@tasks_bp.route("", methods=["POST"])
def create_task():
    request_body = request.get_json()
    
    if "description" not in request_body:
        abort(make_response({"details": "Invalid data"}, 400))
    
    new_task = Task(title=request_body["title"],
                    description=request_body["description"])
    
    
    db.session.add(new_task)
    db.session.commit()
    
    return {
        "task": {
            "id": new_task.task_id,
            "title": new_task.title,
            "description": new_task.description,
            "is_complete": new_task.is_complete
        }
    }, 201
    
    # return make_response(jsonify(f"Task {new_task.title} successfully created"), 201)

@tasks_bp.route("", methods=["GET"])
def get_tasks():
    tasks = Task.query.all()
    
    tasks_response = []
    for task in tasks:
        tasks_response.append(task.to_dict())
        
    return jsonify(tasks_response)

@tasks_bp.route("/<task_id>", methods=["GET"])
def get_one_task(task_id):
    task = validate_task(task_id)
    
    return task.to_dict()

@tasks_bp.route("/<task_id>", methods=["PUT"])
def update_task(task_id):
    task = validate_task(task_id)
    
    request_body = request.get_json()
    
    if "title" not in request_body or "description" not in request_body or "completed at" not in request_body:
        abort(make_response({"details": f"Invalid data"}, 400))
    
    task.title = request_body["title"]
    task.description = request_body["description"]
    
    db.session.commit()
    
    return task.to_dict()

@tasks_bp.route("/<task_id>", methods=["DELETE"])
def delete_task(task_id):
    task = validate_task(task_id)
    
    db.session.delete(task)
    db.session.commit()
    
    return make_response({"details": f'Task {task.task_id} "{task.title}" successfully deleted'})