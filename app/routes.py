from app import db 
from app.models.task import Task
from flask import Blueprint, jsonify, abort, make_response, request

tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")

#helper functions
def validate_task(task_id):
    try:
        task_id = int(task_id)
    except:
        message= f"task {task_id} invalid"
        abort(make_response({"message":message}, 400))
            
    task = Task.query.get(task_id)
    
    if not task: 
        abort(make_response({"message":f"task {task_id} not found"}, 404))

    return task

#route functions 

#POST /tasks
@tasks_bp.route("", methods=["POST"])
def create_task():
    request_body = request.get_json()
    if ("title" not in request_body or "description" not in request_body):
        abort(make_response({"details": "Invalid data"},400))

    new_task = Task(
        title=request_body["title"],
        description=request_body["description"],
        # completed_at=request_body["completed_at"]
    )

    db.session.add(new_task)
    db.session.commit()

    return jsonify({"task":new_task.to_dict()}),201

#GET /tasks 
@tasks_bp.route("", methods=["GET"])
def get_all_tasks():
    tasks= Task.query.all()
    tasks_response = [task.to_dict() for task in tasks]

    return jsonify(tasks_response)

#GET /tasks/1
@tasks_bp.route("/<task_id>", methods=["GET"])
def get_one_task(task_id):
    task = validate_task(task_id)
    
    return jsonify({"task":task.to_dict()})

#PUT /tasks/1
@tasks_bp.route("/<task_id>", methods=["PUT"])
def update_task(task_id):
    task = validate_task(task_id)
    request_body=request.get_json()
    task.title=request_body["title"]
    task.description=request_body["description"]
    db.session.commit()
    return jsonify({"task":task.to_dict()}),200

#DELETE /tasks/1
@tasks_bp.route("/<task_id>", methods=["DELETE"])
def delete_task(task_id):
    task = validate_task(task_id)
    db.session.delete(task)
    db.session.commit()

    return jsonify({"details": f'Task {task_id} "{task.title}" successfully deleted'}),200




    




