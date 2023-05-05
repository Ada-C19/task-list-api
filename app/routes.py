from flask import Blueprint, jsonify, request, make_response, abort
from app import db
from app.models.task import Task


task_bp = Blueprint("task", __name__,url_prefix = "/tasks")

# create a task
@task_bp.route("", methods = ["POST"])
def get_task():
    response_body = request.get_json()
    if "title" not in response_body or "description" not in response_body:
        return jsonify({ "details": "Invalid data"}), 400
    
    new_task = Task(
        title = response_body["title"],
        description = response_body["description"],
        completed_at = response_body.get("completed_at", None)
    )
    db.session.add(new_task)
    db.session.commit() 

    return jsonify({"task":{
            "id": new_task.task_id,
            "title": new_task.title,
            "description": new_task.description,
            "is_complete": False
    }
    }), 201

# get all tasks
@task_bp.route("", methods = ["GET"])
def get_all_tasks():
    response = []
    tasks = Task.query.all()
    for task in tasks:
        response.append({
            "id": task.task_id,
            "title":task.title,
            "description": task.description,
            "is_complete": False
    })
        # response.append(task.to_dict())
    return jsonify(response), 200


# get one task
@task_bp.route("/<task_id>", methods = ["GET"])
def get_one_task(task_id):
    tasks = validate_task(task_id)

    return jsonify({"task":{
            "id": tasks.task_id,
            "title": tasks.title,
            "description": tasks.description,
            "is_complete": False}
            }), 200


# get update
@task_bp.route("/<task_id>", methods=["PUT"])
def update_task(task_id):
    tasks = validate_task(task_id)
    request_data = request.get_json()
    
    tasks.title = request_data["title"]
    tasks.description = request_data["description"]
    tasks.completed_at = request_data.get("completed_at", None)

    db.session.commit()

    return jsonify({"task":{
            "id": tasks.task_id,
            "title": tasks.title,
            "description": tasks.description,
            "is_complete": False}
            }), 200


# 


# helper function
def validate_task(task_id):
    try:
        task_id_num = int(task_id)
    except ValueError:
        return abort(make_response({"msg": "id is invalide input"}, 400))
    
    # return Task.query.get_or_404(task_id_num)

    task = Task.query.get(task_id_num)
    if task is None:
        abort(make_response({"msg": "Task not found"}, 404))
    return task

    
    