from flask import Blueprint

from flask import Blueprint, jsonify, abort, make_response, request
from app import db
from app.models.task import Task

tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")

@tasks_bp.route("", methods=["POST"])
def create_task():
    request_body = request.get_json()
    new_task = Task(title=request_body["title"],
                    description=request_body["description"],
                    completed_at=request_body["completed_at"])
    db.session.add(new_task)
    db.session.commit()
# replacing make_response(f...) with jsonify to debug
    return {"task":{
        "id": new_task.task_id,
        "title": new_task.title,
        "description": new_task.description,
        "is_complete": (new_task.completed_at != None)}}, 201

@tasks_bp.route("", methods=['GET'])
def handle_tasks():

    tasks = Task.query.all()
    tasks_response = [Task.to_dict(task) for task in tasks]
    return jsonify(tasks_response), 200

def validate_task(task_id):
    try:
        task_id = int(task_id)
    except:
        abort(make_response({"message":f"task {task_id} invalid"}, 400))

    task = Task.query.get(task_id)
    
    if task is None:
        abort(make_response({"message":f"task {task_id} not found"}, 404))
    
    return task

@tasks_bp.route("/<task_id>", methods=["GET"])
def handle_task(task_id):
    task = validate_task(task_id)
    # may not need line below, has worked for others as it's already
    # returned in validate_task
    Task.query.get(task_id)

    return {
        "task_id": task.id,
        "title": task.title,
        "description": task.description,
        "completed_at": task.completed_at
    }

# @tasks_bp.route("/<task_id>", methods=["GET"])
# def single_task(task_id):
#     task = validate_task(task_id)
#     Task.query.get(task_id)

#     return {
#         "task_id": task.id,
#         "name": task.name,
#         "description": task.description,
#         "completed_at": task.completed_at
#     }

@tasks_bp.route("/<task_id>", methods=["PUT"])
def update_task(task_id):
    task = validate_task(task_id)
    request_body = request.get_json()

    task.name = request_body["name"]
    task.description = request_body["description"]
    task.completed_at = request_body["completed_at"]

    db.session.commit()

    return make_response(f"Task #{task_id} successfully updated")

@tasks_bp.route("/<task_id>", methods=["DELETE"])
def delete_task(task_id):
    task = validate_task(task_id)
    db.session.delete(task)
    db.session.commit()

    return make_response(f"Task #{task_id} successfully deleted")